import os
from tokenization import Tokenizer
from parsing import Parser
from generation import Generator 
from tokens import * 

class Compiler():
    def __init__(self, file):
        with open(file) as f:
            self.text = f.read()
        self.tokenizer = Tokenizer()
        self.parser = Parser()
        self.generator = Generator()
    
    def compile(self):
        tokenized = self.tokenizer.tokenize(self.text)
        parsed = self.parser.parse_prog(tokenized)
        #print([stmt.var.value.value for stmt in parsed.stmts if isinstance(stmt.var, NodeStmtPrint)])
        self.generator.gen_prog(parsed)
        output = "global _start\n" + self.generator.labels["_start"]["content"] + "    jmp _exit\n"

        for label in self.generator.labels:
            if label+":" not in output and label != "_start":
                output += "\n"+self.generator.labels[label]["content"]
                output += f"    jmp {self.generator.labels[label]['end']}"

        output += "\n_exit:\n    mov rax, 60\n    mov rdi, 0\n    syscall"

        with open("compiled.asm", "w") as f:
            f.write(output)
        os.system("nasm -felf64 ./compiled.asm")

if __name__ == "__main__":
    compiler = Compiler("./selfmade/test.flyp")
    compiler.compile()
