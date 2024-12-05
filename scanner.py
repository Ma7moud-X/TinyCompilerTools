import re
from PyQt5.QtWidgets import QMessageBox
import sys
import matplotlib.pyplot as plt

class Scanner:
    SYMBOLS = {
        "+": "PLUS",
        "-": "MINUS",
        "*": "MULT",
        "/": "DIV",
        "(": "OPENBRACKET",
        ")": "CLOSEBRACKET",
        "<": "LESSTHAN",
        "=": "EQUAL",
        ";": "SEMICOLON",
        ":=": "ASSIGN",
        "{": "OPENBRACE",
        "}": "CLOSEBRACE",
        # ">": "GREATERTHAN",
    }
    SYMBOLS_PATTERN = "|".join(re.escape(s) for s in SYMBOLS)
    KEYWORDS = {
        "if": "IF",
        "then": "THEN",
        "else": "ELSE",
        "end": "END",
        "repeat": "REPEAT",
        "until": "UNTIL",
        "read": "READ",
        "write": "WRITE",
    }
    
    def ERROR(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(message)
        msg.setWindowTitle("Scanning Error")
        msg.setStandardButtons(QMessageBox.Retry | QMessageBox.Close)
        
        retval = msg.exec_()
        
        if retval == QMessageBox.Retry and self.gui:
            plt.close('all')
            raise Exception("Retry requested")
        elif retval == QMessageBox.Close:
            plt.close('all')
            sys.exit()  # Exit program

    def __init__(self, fpath: str, gui = None) -> None:
        self.fpath = fpath
        self.gui = gui

    def identify(self, text: str) -> str:
        """
        determine token type
        """
        if re.match(r"^[a-zA-Z][a-zA-Z]*$", text):
            return "IDENTIFIER"
        elif re.match(r"^\d+$", text):
            return "NUMBER"
        else:
            return "INVALID"

    def split_symbols(self, text: str) -> str:
        """
        puts spaces around operators
        """
        return re.sub(f"({self.SYMBOLS_PATTERN})", r" \1 ", text)

    def scan_string(self, input_string):
        tokens = []
        lines = input_string.split('\n')
        for line in lines:
            line = line.strip()
            tokens.extend(self.split_symbols(line).strip().split())
        try:
            P_tokens = self.process_tokens(tokens)
            if len(P_tokens) == 0:
                self.ERROR("Error Scanning File: No tokens found")
            return P_tokens, False
        except Exception as e:
            return None, True
    
    def scan_file(self):
        with open(self.fpath, "r") as file:
            text = file.read()

        return self.scan_string(text)

    def process_tokens(self, tokens: list[str]):
        i, sz = 0, len(tokens)
        P_tokens = []
        while i < sz:
            if tokens[i] in self.KEYWORDS:
                # print(f"{tokens[i]} : {self.KEYWORDS[tokens[i]]}")
                P_tokens.append((tokens[i],self.KEYWORDS[tokens[i]]))
            elif tokens[i] in self.SYMBOLS:
                if tokens[i] == "{":
                    temp = -1
                    try:
                        temp = tokens.index("}", i + 1)
                    except:
                        self.ERROR("Error Scanning File: No matching closing brace was found for one of the open braces")


                    i = temp + 1
                    continue
                elif tokens[i] == "}":
                    self.ERROR("Error Scanning File: No matching opening brace was found for one of the closing braces")

                # print(f"{tokens[i]} : {self.SYMBOLS[tokens[i]]}")
                P_tokens.append((tokens[i],self.SYMBOLS[tokens[i]]))
            else:
                temp = re.findall(r'[A-Za-z]+|\d+|[^A-Za-z0-9]', tokens[i])                # print(temp)
                
                for t_token in temp:
                    x = self.identify(t_token)
                    if x == "IDENTIFIER":
                        # print(f"{t_token} : IDENTIFIER")
                        P_tokens.append((t_token,'IDENTIFIER'))
                    elif x == "NUMBER":
                        # print(f"{t_token} : NUMBER")
                        P_tokens.append((t_token,'NUMBER'))
                    else:
                        self.ERROR("Error Scanning File: Invalid token")

            i += 1
        return P_tokens
