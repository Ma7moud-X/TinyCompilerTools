from PyQt5.QtWidgets import QMessageBox
import matplotlib.pyplot as plt
import sys

class TreeNode:
    def __init__(self, value, index, edge=True, shape='s'):
        self.value = value
        self.children = []
        self.sibling = None
        self.index = index
        self.edge = edge
        self.shape = shape

    def add_child(self, child):
        self.children.append(child)
        
    def add_sibling(self, s):
        self.sibling = s

    def __str__(self, level=0):
        result = "  " * level + str(self.value) + "\n"
        for child in self.children:
            result += child.__str__(level + 1)
        if self.sibling:
            result += self.sibling.__str__(level)
        return result

class Parser:
    def __init__(self, tokens, gui=None):
        self.tokens = tokens  
        self.index = 0   
        self.edge = True
        self.gui = gui     

    def ERROR(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(f"Token Number {self.index} caused a problem")
        msg.setWindowTitle("Parsing Error")
        msg.setStandardButtons(QMessageBox.Retry | QMessageBox.Close)
        
        retval = msg.exec_()
        
        if retval == QMessageBox.Retry and self.gui:
            plt.close('all')
            raise Exception("Retry requested")
        elif retval == QMessageBox.Close:
            plt.close('all')
            sys.exit()  # Exit program

    def stmt_sequence(self):
        self.edge = True
        children = self.statement()
        temp = children
        while self.index < len(self.tokens) and self.tokens[self.index][1] == "SEMICOLON":
            self.index += 1
            self.edge = False
            ch = self.statement()
            self.edge = True
            if ch:
                temp.add_sibling(ch)
                temp = ch
       
        return children

    def statement(self):
        self.index += 1
        curr = self.tokens[self.index - 1][1]
        
        match curr:
            case "IF":
                return self.if_stmt()
            case "REPEAT":
                return self.repeat_stmt()
            case "IDENTIFIER":
                self.index -= 1
                return self.assign_stmt()
            case "READ":
                return self.read_stmt()
            case "WRITE":
                return self.write_stmt()
            case _:
                self.ERROR()

    def if_stmt(self):
        node = TreeNode("if", self.index, self.edge)
        node.add_child(self.exp())
        
        if self.tokens[self.index][1] == "THEN":
            self.index += 1
            node.add_child(self.stmt_sequence())
        else:
            self.ERROR()

        if self.tokens[self.index][1] == "ELSE":
            self.index += 1
            node.add_child(self.stmt_sequence())


        if self.tokens[self.index][1] == "END":
            self.index += 1
        else:
            self.ERROR()
            
        return node

    def repeat_stmt(self):
        node = TreeNode("repeat", self.index, self.edge)
        
        node.add_child(self.stmt_sequence())
        
        if self.tokens[self.index][1] == "UNTIL":
            self.index += 1
            node.add_child(self.exp())
        else:
            self.ERROR()
            
        return node

    def assign_stmt(self):
        node = TreeNode(f"assign({self.tokens[self.index][0]})", self.index, self.edge)
        
        self.index += 1
        if self.tokens[self.index][1] == "ASSIGN":
            self.index += 1
            node.add_child(self.exp())
        else:
            self.ERROR()

        return node

    def read_stmt(self):
        node = TreeNode(f"read({self.tokens[self.index][0]})", self.index, self.edge)
        self.index += 1
        return node

    def write_stmt(self):
        node = TreeNode("write", self.index, self.edge)
        node.add_child(self.exp())
        return node

    def exp(self):
        temp = self.simple_exp()
        if self.tokens[self.index][1] in {"LESSTHAN","EQUAL"}:
            newtemp = TreeNode(f"OP({self.tokens[self.index][0]})", self.index, shape = 'o')
            self.index += 1
            newtemp.add_child(temp)
            newtemp.add_child(self.simple_exp())
            temp = newtemp
            
        return temp
            
    def simple_exp(self):
        temp = self.term()  
        while self.tokens[self.index][1] in {"PLUS", "MINUS"}:  
            newtemp = TreeNode(f"OP({self.tokens[self.index][0]})", self.index, shape = 'o')
            self.index += 1  
            newtemp.add_child(temp)  
            newtemp.add_child(self.term())  
            temp = newtemp 

        return temp  

    def term(self):
        temp = self.factor()
        while self.tokens[self.index][1] in {"MULT", "DIV"}:  
            newtemp = TreeNode(f"OP({self.tokens[self.index][0]})", self.index, shape = 'o')
            self.index += 1  
            newtemp.add_child(temp)  
            newtemp.add_child(self.factor()) 
            temp = newtemp  
            
        return temp     

    def factor(self):
        if self.tokens[self.index][1] == "OPENBRACKET":
            self.index += 1
            node = self.exp()
            if self.tokens[self.index][1] != "CLOSEBRACKET":
                self.ERROR()
            self.index += 1
            return node
        elif self.tokens[self.index][1] == "NUMBER":
            self.index += 1
            return TreeNode(f"const({self.tokens[self.index - 1][0]})", self.index, shape = 'o')
        else:
            self.index += 1
            return TreeNode(f"id({self.tokens[self.index - 1][0]})", self.index, shape = 'o')

    def parse(self):
        try:
            root = TreeNode("Program",-1, self.edge)
            root.add_child(self.stmt_sequence())
            if self.index != len(self.tokens):
                self.ERROR()
            # print(root)
            return root, False
        except Exception as e:
            if str(e) == "Retry requested":
                return None, True
            else:
                try:
                    self.ERROR()
                except:
                    return None, True


# input_filepath = './test.txt'
# output_filepath = './output.txt'
# p = Scanner(input_filepath, output_filepath)
# tokens = p.scan_file()

# parser = Parser(tokens)
# parser.parse()