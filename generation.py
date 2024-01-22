from tokens import *

class Generator():
    def __init__(self):
        self.output = ""
        self.vars = {}
        self.scopes = []
        self.stack_size = 0
        self.labels = {"_start":{"content":"_start:\n", "end":"_exit"}}
    
    def gen_term(self, term, dest):
        term = term.value
        if isinstance(term, NodeTermIntLit):
            self.labels[dest]["content"] += f"    mov rax, {term.value[2]}\n"
            self.push("rax", dest)
        
        elif isinstance(term, NodeTermId):
            if term.value[2] not in self.vars:
                print(f" Undeclared identifier: {term.value[2]}")
                exit()
            offset = f"QWORD [rsp + {(self.stack_size - self.vars[term.value[2]] - 1) * 8}]"
            self.push(offset, dest)
        
        elif isinstance(term, NodeTermParen):
            self.gen_expr(term.value, dest)
    
    def gen_assign(self, stmt, dest):
        if stmt.id_name not in self.vars:
            self.vars[stmt.id_name] =  self.stack_size
        self.gen_expr(stmt.expr, dest)
        self.pop("rax", dest)
        self.labels[dest]["content"] += f"    mov [rsp + {(self.stack_size - self.vars[stmt.id_name] - 1) * 8}], rax\n"

    def gen_bin_expr(self, expr, dest):
        expr = expr.var
        
        if isinstance(expr, NodeBinExprAdd):
            self.gen_expr(expr.rhs, dest)
            self.gen_expr(expr.lhs, dest)
            self.pop("rax", dest)
            self.pop("rbx", dest)
            self.labels[dest]["content"] += "    add rax, rbx\n"
            self.push("rax", dest)
        
        elif isinstance(expr, NodeBinExprMinus):
            self.gen_expr(expr.rhs, dest)
            self.gen_expr(expr.lhs, dest)
            self.pop("rax", dest)
            self.pop("rbx", dest)
            self.labels[dest]["content"] += f"    sub rax, rbx\n"
            self.push("rax", dest)
        
        elif isinstance(expr, NodeBinExprMulti):
            self.gen_expr(expr.rhs, dest)
            self.gen_expr(expr.lhs, dest)
            self.pop("rax", dest)
            self.pop("rbx", dest)
            self.labels[dest]["content"] += f"    mul rbx\n"
            self.push("rax", dest)
        
        elif isinstance(expr, NodeBinExprDiv):
            self.gen_expr(expr.rhs, dest)
            self.gen_expr(expr.lhs, dest)
            self.pop("rax", dest)
            self.pop("rbx", dest)
            self.labels[dest]["content"] += f"    div rbx\n"
            self.push("rax", dest)
    
    def gen_expr(self, expr, dest):
        if isinstance(expr.var, NodeTerm):
            self.gen_term(expr.var, dest)

        elif isinstance(expr.var, NodeBinExpr):
            self.gen_bin_expr(expr.var, dest)
        
        elif isinstance(expr.var, NodeBoolExpr):
            self.gen_expr(expr.var.var.rhs, dest)
            self.gen_expr(expr.var.var.lhs, dest)
    
    def gen_if_pred(self, stmt, dest):
        self.gen_expr(stmt.expr, dest)
        self.pop("rax", dest)
        self.pop("rbx", dest)
        created_label = f"label{len(self.labels)}"

        self.labels[dest]["content"] += f"    cmp rax, rbx\n"
        self.labels[dest]["content"] += f"    je {created_label}\n"
        self.labels[dest]["content"] += f"    jmp end_{created_label}\n"
        
        self.labels[created_label] = {"content": f"{created_label}:\n", "end": f"end_{created_label}"}
        self.labels[f"end_{created_label}"] = {"content": f"\nend_{created_label}:\n", "end": "_exit"}

        self.gen_scope(stmt, created_label)
        self.gen_prog(stmt.end, f"end_{created_label}")[1]
        return f"end_{created_label}"
    
    def gen_while_pred(self, stmt, dest):
        self.gen_expr(stmt.expr, dest)
        self.pop("rax", dest)
        self.pop("rbx", dest)
        created_label = f"label{len(self.labels)}"
        
        self.labels[dest]["content"] += f"    cmp rax, rbx\n"
        self.labels[dest]["content"] += f"    {comparator(stmt.expr)} {created_label}\n"
        self.labels[dest]["content"] += f"    jmp end_{created_label}\n"
        
        self.labels[created_label] = {"content": f"{created_label}:\n", "end": f"end_{created_label}"}
        self.labels[f"end_{created_label}"] = {"content": f"\nend_{created_label}:\n", "end": "_exit"}

        after = self.gen_scope(stmt, created_label)
        self.gen_expr(stmt.expr, created_label)
        self.pop("rax", created_label)
        self.pop("rbx", created_label)
        self.labels[created_label]["content"] += f"    cmp rax, rbx\n"
        self.labels[created_label]["content"] += f"    {comparator(stmt.expr)} {created_label}\n"
        self.labels[created_label]["content"] += f"    jmp end_{created_label}\n"

        self.gen_expr(stmt.expr, after)
        self.pop("rax", after)
        self.pop("rbx", after)
        self.labels[after]["content"] += f"    cmp rax, rbx\n"
        self.labels[after]["content"] += f"    {comparator(stmt.expr)} {created_label}\n"
        self.labels[after]["content"] += f"    jmp end_{created_label}\n"
        self.gen_prog(stmt.end, f"end_{created_label}")[1]
        return f"end_{created_label}"

    def gen_scope(self, stmt, dest):
        after = dest
        self.begin_scope()
        for n in stmt.stmts:
            returned = self.gen_stmt(n, after)
            if returned:
                after = returned
        self.end_scope(after)
        return after

    def gen_print(self, stmt, dest):
        self.labels[dest]["content"] += f"    mov rax, 1\n"
        self.labels[dest]["content"] += f"    mov rdi, 1\n"
        self.labels[dest]["content"] += f"    mov rdx, 1\n"
        printable = stmt.value.value
        if stmt.endl:
            self.labels[dest]["content"] += f"    mov rbx, 10\n"
            self.push("rbx", dest)
        for i in range(len(printable)-1, -1, -1):
            self.labels[dest]["content"] += f"    mov rbx, {ord(printable[i])}\n"
            self.push("rbx", dest)
        for char in printable:
            self.labels[dest]["content"] += f"    mov rsi, rsp\n"
            self.pop("rbx", dest)
            self.labels[dest]["content"] += f"    syscall\n"
        if stmt.endl:
            self.labels[dest]["content"] += f"    mov rsi, rsp\n"
            self.pop("rbx", dest)
            self.labels[dest]["content"] += f"    syscall\n"

    def gen_stmt(self, stmt, dest):
        end = None
        if isinstance(stmt.var, NodeStmtExit):
            self.gen_expr(stmt.var.expr, dest)
            self.labels[dest]["content"] += "    mov rax, 60\n"
            self.pop("rdi", dest)
            self.labels[dest]["content"] += "    syscall\n"
        
        elif isinstance(stmt.var, NodeStmtAs):
            if stmt.var.id_name in self.vars:
                self.gen_expr(stmt.var.expr, dest)
                self.pop("rax", dest)
                self.labels[dest]["content"] += f"    mov [rsp + {(self.stack_size - self.vars[stmt.var.id_name] - 1)*8}], rax\n"
                return
            self.vars[stmt.var.id_name] =  self.stack_size
            self.gen_expr(stmt.var.expr, dest)

        elif isinstance(stmt.var, NodeStmtIf):
            end = self.gen_if_pred(stmt.var, dest)
        
        elif isinstance(stmt.var, NodeStmtWhile):
            end = self.gen_while_pred(stmt.var, dest)
        
        elif isinstance(stmt.var, NodeStmtPrint):
            self.gen_print(stmt.var, dest)

        else:
            print("Unrecognised Node")
            exit()
        return end


    def gen_prog(self, parsed, dest = "_start"):
        end = dest
        for i in range(len(parsed.stmts)):
            after = self.gen_stmt(parsed.stmts[i], end)
            if after:
                end = after
        return end

    def push(self, reg, dest):
        self.labels[dest]["content"] += f"    push {reg}\n"
        self.stack_size += 1
    
    def pop(self, reg, dest):
        self.labels[dest]["content"] += f"    pop {reg}\n"
        self.stack_size -= 1

    def begin_scope(self):
        self.scopes.append(self.stack_size)
    
    def end_scope(self, dest):
        pop_count = len(self.vars) - self.scopes[-1]
        self.stack_size -= pop_count
        if pop_count != 0:
            self.labels[dest]["content"] += f"    add rsp, {pop_count * 8}\n"
        
        for i in range(pop_count):
            self.vars.popitem()
        
        self.scopes.pop(-1)