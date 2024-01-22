from tokens import *

class Tokenizer:
    def __init__(self):
        self.text = None
        self.index = 0
        self.line_count = 1
    
    def tokenize(self, text):
        self.text = text
        buf = ""
        tokens = []
        while self.peek():
            if self.peek() == "/" and self.peek(1) == "*":
                self.consume()
                self.consume()
                while not (self.peek() == "*" and self.peek(1) == "/"):
                    self.consume()
                self.consume()
                self.consume()
            elif self.peek() == "#":
                while self.peek() != "\n":
                    self.consume()
            elif self.peek() == '"':
                self.consume()
                buf = ""
                while self.peek() and self.peek() != '"':
                    buf += self.consume()
                self.consume()
                tokens.append((TokenType.str_lit, self.line_count, buf))
                buf = ""
            elif self.peek().isalpha():
                buf += self.consume()
                while self.peek() and self.peek().isalnum():
                    buf += self.consume()
                if buf == "exit":
                    tokens.append((TokenType._exit, self.line_count))
                    buf = ""
                elif buf == "if":
                    tokens.append((TokenType._if, self.line_count))
                    buf = ""
                elif buf == "while":
                    tokens.append((TokenType._while, self.line_count))
                    buf = ""
                elif buf == "print":
                    tokens.append((TokenType._print, self.line_count))
                    buf = ""
                else:
                    tokens.append((TokenType.id, self.line_count, buf))
                    buf =""
            elif self.peek().isdigit():
                buf = self.consume()
                while self.peek() and self.peek().isnumeric():
                    buf += self.consume()
                tokens.append((TokenType.int_lit, self.line_count, buf))
                buf = ""
            elif self.peek() == ";":
                self.consume()
                tokens.append((TokenType.semi, self.line_count,))
            elif self.peek() == " ":
                self.consume()
            elif self.peek() == "=" and self.peek(1) == "=":
                tokens.append((TokenType.check_eq, self.line_count))
                self.consume()
                self.consume()
            elif self.peek() == ">":
                tokens.append((TokenType.check_sup, self.line_count))
                self.consume()
            elif self.peek() == "<":
                tokens.append((TokenType.check_inf, self.line_count))
                self.consume()
            elif self.peek() == "=":
                self.consume()
                tokens.append((TokenType.eq, self.line_count))
            elif self.peek() == "\n":
                self.line_count += 1
                self.consume()
            elif self.peek() == "(":
                self.consume()
                tokens.append((TokenType.open_paren, self.line_count,))
            elif self.peek() == ")":
                self.consume()
                tokens.append((TokenType.close_paren, self.line_count,))
            elif self.peek() == "+":
                self.consume()
                tokens.append((TokenType.plus, self.line_count))
            elif self.peek() == "-":
                self.consume()
                tokens.append((TokenType.minus, self.line_count))
            elif self.peek() == "/":
                self.consume()
                tokens.append((TokenType.slash, self.line_count))
            elif self.peek() == "*":
                self.consume()
                tokens.append((TokenType.mul, self.line_count))   
            elif  self.peek() == "{":
                self.consume()
                tokens.append((TokenType.open_curly, self.line_count))
            elif self.peek() == "}":
                self.consume()
                tokens.append((TokenType.close_curly, self.line_count))
            elif self.peek() == "&":
                self.consume()
                tokens.append((TokenType.endl, self.line_count))
            else:
                print(self.peek())
                print(f"Invalid statement, at line {self.line_count}")
                exit()
        self._index = 0
        return tokens

    def peek(self, offset = 0):
        if self.index+offset < len(self.text):
            return self.text[self.index+offset]
    
    def consume(self):
        self.index += 1
        return self.peek(-1) 