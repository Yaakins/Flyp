from enum import Enum

class TokenType(Enum):
    eq = 1
    id = 2
    semi = 3
    int_lit = 4
    _exit = 5
    open_paren = 6
    close_paren = 7
    plus = 8
    mul = 9
    slash = 10
    minus = 11
    _if = 12
    open_curly = 13
    close_curly = 14
    check_eq = 15
    _while = 16
    _print = 17
    check_sup = 18
    check_inf = 19
    str_lit = 20
    endl = 21

def bin_prec(typ):
    match typ:
        case TokenType.plus:
            return 0
        case TokenType.minus:
            return 0
        case TokenType.check_eq:
            return 0
        case TokenType.check_sup:
            return 0
        case TokenType.slash:
            return 1
        case TokenType.mul:
            return 1
    
def comparator(stmt):
    if isinstance(stmt.var.var, NodeBoolExprEqu):
        return 'je'
    elif isinstance(stmt.var.var, NodeBoolExprSup):
        return 'jg'

class NodeProg:
    stmts = []

class NodeStmt: ...

class NodeStmtExit: ...

class NodeStmtAs: ...

class NodeTerm: ...

class NodeTermIntLit: ...

class NodeTermStrLit: ...

class NodeTermId: ...

class NodeTermParen: ...

class NodeExpr: ...

class NodeBinExpr: ...

class NodeBinExprAdd: ...

class NodeBinExprMinus: ...

class NodeBinExprMulti: ...

class NodeBinExprDiv: ...

class NodeBoolExpr: ...

class NodeBoolExprEqu: ...

class NodeBoolExprSup: ...

class NodeStmtIf: ...

class NodeStmtWhile: ...

class NodeStmtPrint: ...

