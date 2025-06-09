import ply.yacc as yacc
from lexer import tokens

class ASTNode:
    pass

class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements

class FunctionDef(ASTNode):
    def __init__(self, return_type, name, params, body):
        self.return_type = return_type
        self.name = name
        self.params = params
        self.body = body

class VarDecl(ASTNode):
    def __init__(self, var_type, name, init_value=None):
        self.var_type = var_type
        self.name = name
        self.init_value = init_value

class Assignment(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class IfStmt(ASTNode):
    def __init__(self, condition, then_stmt, else_stmt=None):
        self.condition = condition
        self.then_stmt = then_stmt
        self.else_stmt = else_stmt

class ForStmt(ASTNode):
    def __init__(self, init, condition, update, body):
        self.init = init
        self.condition = condition
        self.update = update
        self.body = body

class ReturnStmt(ASTNode):
    def __init__(self, value=None):
        self.value = value

class Block(ASTNode):
    def __init__(self, statements):
        self.statements = statements

class BinaryOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Identifier(ASTNode):
    def __init__(self, name):
        self.name = name

class Number(ASTNode):
    def __init__(self, value):
        self.value = value

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQ', 'NE'),
    ('left', 'LT', 'GT'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

def p_program(p):
    '''program : statement_list'''
    p[0] = Program(p[1])

def p_statement_list(p):
    '''statement_list : statement_list statement
                     | statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_statement(p):
    '''statement : function_def
                | var_decl SEMICOLON
                | assignment SEMICOLON
                | if_stmt
                | for_stmt
                | return_stmt SEMICOLON
                | expression_stmt SEMICOLON
                | block'''
    p[0] = p[1]

def p_function_def(p):
    '''function_def : INT IDENTIFIER LPAREN param_list RPAREN block
                   | VOID IDENTIFIER LPAREN param_list RPAREN block
                   | INT IDENTIFIER LPAREN RPAREN block
                   | VOID IDENTIFIER LPAREN RPAREN block'''
    if len(p) == 7:
        p[0] = FunctionDef(p[1], p[2], p[4], p[6])
    else:
        p[0] = FunctionDef(p[1], p[2], [], p[5])

def p_param_list(p):
    '''param_list : param_list COMMA param
                 | param
                 | empty'''
    if len(p) == 2:
        p[0] = [p[1]] if p[1] else []
    else:
        p[0] = p[1] + [p[3]]

def p_param(p):
    '''param : INT IDENTIFIER'''
    p[0] = VarDecl(p[1], p[2])

def p_var_decl(p):
    '''var_decl : INT IDENTIFIER
               | INT IDENTIFIER ASSIGN expression'''
    if len(p) == 3:
        p[0] = VarDecl(p[1], p[2])
    else:
        p[0] = VarDecl(p[1], p[2], p[4])

def p_assignment(p):
    '''assignment : IDENTIFIER ASSIGN expression'''
    p[0] = Assignment(p[1], p[3])

def p_if_stmt(p):
    '''if_stmt : IF LPAREN expression RPAREN statement
              | IF LPAREN expression RPAREN statement ELSE statement'''
    if len(p) == 6:
        p[0] = IfStmt(p[3], p[5])
    else:
        p[0] = IfStmt(p[3], p[5], p[7])

def p_for_stmt(p):
    '''for_stmt : FOR LPAREN assignment SEMICOLON expression SEMICOLON assignment RPAREN statement'''
    p[0] = ForStmt(p[3], p[5], p[7], p[9])

def p_return_stmt(p):
    '''return_stmt : RETURN
                  | RETURN expression'''
    if len(p) == 2:
        p[0] = ReturnStmt()
    else:
        p[0] = ReturnStmt(p[2])

def p_expression_stmt(p):
    '''expression_stmt : expression'''
    p[0] = p[1]

def p_block(p):
    '''block : LBRACE statement_list RBRACE
            | LBRACE RBRACE'''
    if len(p) == 4:
        p[0] = Block(p[2])
    else:
        p[0] = Block([])

def p_expression_binop(p):
    '''expression : expression PLUS expression
                 | expression MINUS expression
                 | expression TIMES expression
                 | expression DIVIDE expression
                 | expression EQ expression
                 | expression NE expression
                 | expression LT expression
                 | expression GT expression
                 | expression AND expression
                 | expression OR expression'''
    p[0] = BinaryOp(p[1], p[2], p[3])

def p_expression_group(p):
    '''expression : LPAREN expression RPAREN'''
    p[0] = p[2]

def p_expression_identifier(p):
    '''expression : IDENTIFIER'''
    p[0] = Identifier(p[1])

def p_expression_number(p):
    '''expression : NUMBER'''
    p[0] = Number(p[1])

def p_empty(p):
    '''empty :'''
    pass

def p_error(p):
    if p:
        print(f"Syntax error at token {p.type} ('{p.value}') at line {p.lineno}")
    else:
        print("Syntax error at EOF")

def build_parser():
    return yacc.yacc()

def parse(input_data):
    from lexer import build_lexer
    lexer = build_lexer()
    parser = build_parser()
    return parser.parse(input_data, lexer=lexer)
