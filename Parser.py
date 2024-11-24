
class TreeNode:
    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def __str__(self, level=0):
        result = "  " * level + str(self.value) + "\n"
        for child in self.children:
            result += child.__str__(level + 1)
        return result
    
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens  
        self.index = 0        

    def ERROR(self):
        print("LOL")

    def stmt_sequence(self):
        children = [self.statement()]
        
        while self.index < len(self.tokens) and self.tokens[self.index][1] == "SEMICOLON":
            self.index += 1
            children.append(self.statement()) 
                   
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
        node = TreeNode("IF")
        node.add_child(self.exp())
        
        if self.tokens[self.index][1] == "THEN":
            self.index += 1
            for child in self.stmt_sequence():  
                node.add_child(child)
        else:
            self.ERROR()

        if self.tokens[self.index][1] == "ELSE":
            self.index += 1
            for child in self.stmt_sequence():  
                node.add_child(child)

        if self.tokens[self.index][1] == "END":
            self.index += 1
        else:
            self.ERROR()
            
        return node

    def repeat_stmt(self):
        node = TreeNode("REPEAT")
        
        for child in self.stmt_sequence():  
                node.add_child(child)
        
        if self.tokens[self.index][1] == "UNTIL":
            self.index += 1
            node.add_child(self.exp())
        else:
            self.ERROR()
            
        return node

    def assign_stmt(self):
        node = TreeNode(f"ASSIGN({self.tokens[self.index][0]})")
        
        self.index += 1
        if self.tokens[self.index][1] == "ASSIGN":
            self.index += 1
            node.add_child(self.exp())
        else:
            self.ERROR()

        return node

    def read_stmt(self):
        node = TreeNode(f"READ({self.tokens[self.index][0]})")
        self.index += 1
        return node

    def write_stmt(self):
        node = TreeNode("WRITE")
        node.add_child(self.exp())
        return node

    def exp(self):
        temp = self.simple_exp()
        if self.tokens[self.index][1] in {"LESSTHAN","EQUAL"}:
            newtemp = TreeNode(f"OP({self.tokens[self.index][0]})")
            self.index += 1
            newtemp.add_child(temp)
            newtemp.add_child(self.simple_exp())
            temp = newtemp
            
        return temp
            
    def simple_exp(self):
        temp = self.term()  
        while self.tokens[self.index][1] in {"PLUS", "MINUS"}:  
            newtemp = TreeNode(self.tokens[self.index][1]) 
            self.index += 1  
            newtemp.add_child(temp)  
            newtemp.add_child(self.term())  
            temp = newtemp 

        return temp  


    def term(self):
        temp = self.factor()
        while self.tokens[self.index][1] in {"MULT", "DIV"}:  
            newtemp = TreeNode(self.tokens[self.index][1])  
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
            return TreeNode(f"NUMBER({self.tokens[self.index - 1][0]})")
        else:
            self.index += 1
            return TreeNode(f"IDENTIFIER({self.tokens[self.index - 1][0]})")

    def parse(self):
        # self.index = 0
        root = TreeNode("Program")
        while self.index < len(self.tokens):
            for child in self.stmt_sequence():  
                root.add_child(child)
        
        print(root)
        return root


