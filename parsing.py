from tokens import *

class Parser:
    def __init__(self):
        self.tokenized = []
        self.index = 0
        self.prog_count = 0
    
    def parse_term(self):
        int_lit = self.try_consume(TokenType.int_lit)
        if int_lit:
            int_lit_term = NodeTermIntLit()
            int_lit_term.value = int_lit
            term = NodeTerm()
            term.value = int_lit_term
            return term
        
        identifier = self.try_consume(TokenType.id)
        if identifier:
            id_term = NodeTermId()
            id_term.value = identifier
            term = NodeTerm()
            term.value = id_term
            return term
    
        open_paren = self.try_consume(TokenType.open_paren)
        if open_paren:
            expr = self.parse_expr()
            if not expr:
                print("Expected expression")
                exit()
            self.try_consume(TokenType.close_paren)
            term_paren = NodeTermParen()
            term_paren.value = expr
            term = NodeTerm()
            term.value = term_paren
            return term

    def parse_expr(self, min_prec = 0):
        term_lhs = self.parse_term()
        if not term_lhs:
            return
        expr_lhs = NodeExpr()
        expr_lhs.var = term_lhs

        while True:
            curr_tok = self.peek()
            if curr_tok:
                prec = bin_prec(curr_tok[0])
                if prec is None or prec < min_prec:
                    break
            else:
                break

            op = self.consume()
            next_min_prec = prec + 1
            expr_rhs = self.parse_expr(next_min_prec)
            if not expr_lhs:
                print("Unable to parse expression")
                exit()
            
            expr = NodeBinExpr()
            expr_lhs2 = NodeExpr()

            if op[0] == TokenType.plus:
                add = NodeBinExprAdd()
                expr_lhs2.var = expr_lhs.var
                add.lhs = expr_lhs2
                add.rhs = expr_rhs
                expr.var = add

            elif op[0] == TokenType.mul:
                multi = NodeBinExprMulti()
                expr_lhs2.var = expr_lhs.var
                multi.lhs = expr_lhs2
                multi.rhs = expr_rhs
                expr.var = multi
            
            elif op[0] == TokenType.minus:
                sub = NodeBinExprMinus()
                expr_lhs2.var = expr_lhs.var
                sub.lhs = expr_lhs2
                sub.rhs = expr_rhs
                expr.var = sub
            
            elif op[0] == TokenType.slash:
                div = NodeBinExprDiv()
                expr_lhs2.var = expr_lhs.var
                div.lhs = expr_lhs2
                div.rhs = expr_rhs
                expr.var = div
            elif op[0] == TokenType.check_eq:
                equal = NodeBoolExprEqu()
                expr_lhs2.var = expr_lhs.var
                equal.lhs = expr_lhs2
                equal.rhs = expr_rhs
                expr = NodeBoolExpr()
                expr.var = equal
            elif op[0] == TokenType.check_sup:
                sup = NodeBoolExprSup()
                expr_lhs2.var = expr_lhs.var
                sup.lhs = expr_lhs2
                sup.rhs = expr_rhs
                expr = NodeBoolExpr()
                expr.var = sup
            

            else:
                print("Invalid operand")
                exit()
            expr_lhs.var = expr

        return expr_lhs

    def parse_stmt(self):
        stmt = NodeStmt()
        if self.peek() and self.peek(1) and self.peek()[0] == TokenType._exit and self.peek(1)[0] == TokenType.open_paren:
            self.consume()
            self.consume()
            stmt_exit = NodeStmtExit()
            node_expr = self.parse_expr()
            if node_expr:
                stmt_exit.expr = node_expr
            else:
                self.error_expected("expression", self.peek()[1])
            self.try_consume_err(TokenType.close_paren)
            self.try_consume_err(TokenType.semi)
            stmt.var = stmt_exit
            return stmt
        
        elif self.peek() and self.peek(1) and self.peek()[0] == TokenType.id and self.peek(1)[0] == TokenType.eq:
            identifier = self.consume()[2]
            self.consume()
            stmt_as = NodeStmtAs()
            expr = self.parse_expr()
            if expr:
                stmt_as.id_name = identifier
                stmt_as.expr = expr
            else:
                self.error_expected("expression", self.peek()[1])
            self.try_consume_err(TokenType.semi)
            stmt.var = stmt_as
            return stmt

        
        elif self.peek() and self.peek()[0] == TokenType._if:
            self.consume()
            expr = self.parse_expr()
            stmt_if = NodeStmtIf()
            if expr:
                stmt_if.expr = expr
                stmt_if.stmts = self.parse_scope()
            else:
                self.error_expected("expression", self.peek()[1])
            self.try_consume_err(TokenType.semi)

            nexts = self.tokenized[self.index:]
            stmt_if.end = self.parse_prog(nexts)
            stmt.var = stmt_if
            return stmt


        elif self.peek() and self.peek()[0] == TokenType._while:
            self.consume()
            expr = self.parse_expr()
            stmt_loop = NodeStmtWhile()
            if expr:
                stmt_loop.expr = expr
                stmt_loop.stmts = self.parse_scope()
            else:
                self.error_expected("expression", self.peek()[1])
            self.try_consume_err(TokenType.semi)

            nexts = self.tokenized[self.index:]
            stmt_loop.end = self.parse_prog(nexts)
            stmt.var = stmt_loop
            return stmt

        elif self.peek() and self.peek(1) and self.peek(2) and self.peek()[0] == TokenType._print and self.peek(1)[0] == TokenType.open_paren and self.peek(2)[0] == TokenType.str_lit:
            self.consume()
            self.consume()
            value = NodeTermStrLit
            value.value = self.consume()[2]
            stmt_print = NodeStmtPrint()
            stmt_print.value = value
            if self.peek()[0] == TokenType.endl:
                stmt_print.endl = True
                self.consume()
            else:
                stmt_print.endl = False

            stmt = NodeStmt()
            stmt.var = stmt_print
            self.try_consume_err(TokenType.close_paren)
            self.try_consume_err(TokenType.semi)

            return stmt

    def parse_scope(self):
        self.try_consume_err(TokenType.open_curly)
        stmts = []
        stmt = self.parse_stmt()
        while stmt is not None:
            stmts.append(stmt)
            stmt = self.parse_stmt()
        self.try_consume_err(TokenType.close_curly)
        return stmts

    def parse_prog(self, tokenized):
        self.tokenized = tokenized
        self.index = 0
        prog = NodeProg()
        while self.peek():
            stmt = self.parse_stmt()
            if stmt is not None:
                prog.stmts = prog.stmts + [stmt]
            else:
                break
            print([stmt.var.value.value for stmt in prog.stmts if isinstance(stmt.var, NodeStmtPrint)])
        return prog   

    def try_consume(self, typ):
        if self.peek() and self.peek()[0] == typ:
            return self.consume()
    
    def try_consume_err(self, typ):
        if self.peek() and self.peek()[0] == typ:
            return self.consume()
        self.error_expected(typ.name, self.peek(-1)[1])

    def error_expected(self, msg, line):
        print(f"[Parsing error]: {msg} expected at line {line}")
        exit()

    def peek(self, offset = 0):
        if self.index+offset < len(self.tokenized):
            return self.tokenized[self.index+offset]
    
    def consume(self):
        self.index += 1
        return self.peek(-1) 
