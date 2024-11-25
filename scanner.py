import re
import os

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

    def __init__(slef):
        pass
        
    def __init__(self, fpath: str, opath: str) -> None:
        self.fpath = fpath
        self.opath = opath

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

    def scan_file(self):
        with open(self.fpath, "r") as file:
            text = file.readlines()

        with open(self.opath, "w") as output_file:
            tokens = []
            for line in text:
                line = line.strip()
                tokens.extend(self.split_symbols(line).strip().split())
            P_tokens = self.process_tokens(tokens, output_file)
        return P_tokens

    def process_tokens(self, tokens: list[str], output_file):
        i, sz = 0, len(tokens)
        P_tokens = []
        while i < sz:
            if tokens[i] in self.KEYWORDS:
                # print(f"{tokens[i]} : {self.KEYWORDS[tokens[i]]}")
                P_tokens.append((tokens[i],self.KEYWORDS[tokens[i]]))
                output_file.write(f"{tokens[i]} : {self.KEYWORDS[tokens[i]]}\n")
            elif tokens[i] in self.SYMBOLS:
                if tokens[i] == "{":
                    temp = -1
                    try:
                        temp = tokens.index("}", i + 1)
                    except:
                        print("Error Scanning File: No matching closing brace was found for one of the open braces")
                        if os.path.exists("./output.txt"):
                            os.remove("./output.txt")

                        exit()

                    # print(" ".join(tokens[i : temp + 1]) + " : Comment")
                    # output_file.write(
                    #     " ".join(tokens[i : temp + 1]) + " : Comment\n"
                    # )
                    i = temp + 1
                    continue

                # print(f"{tokens[i]} : {self.SYMBOLS[tokens[i]]}")
                P_tokens.append((tokens[i],self.SYMBOLS[tokens[i]]))
                output_file.write(f"{tokens[i]} : {self.SYMBOLS[tokens[i]]}\n")

            else:
                x = self.identify(tokens[i])
                if x == "IDENTIFIER":
                    # print(f"{tokens[i]} : IDENTIFIER")
                    P_tokens.append((tokens[i],'IDENTIFIER'))
                    output_file.write(f"{tokens[i]} : IDENTIFIER\n")
                elif x == "NUMBER":
                    # print(f"{tokens[i]} : NUMBER")
                    P_tokens.append((tokens[i],'NUMBER'))
                    output_file.write(f"{tokens[i]} : NUMBER\n")
                else:
                    print("Error Scanning File: Invalid token")
                    if os.path.exists("./output.txt"):
                        os.remove("./output.txt")

                    exit()

            i += 1
        return P_tokens

        # print("")
        output_file.write("\n")
