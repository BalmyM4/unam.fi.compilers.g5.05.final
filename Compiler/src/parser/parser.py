#!/usr/bin/env python3

"""
Parser for C-like Language
Parses tokens into Abstract Syntax Tree (AST)
"""

import ply.yacc as yacc
try:
    from ..lexer.tokens import tokens, precedence
    from .ast_nodes import *
except ImportError:
    import sys, os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lexer'))
    sys.path.append(os.path.dirname(__file__))
    from tokens import tokens, precedence
    from ast_nodes import *

class Parser:
    """Parser for C-like language with complete syntax support"""
    
    tokens = tokens
    precedence = precedence
    
    def __init__(self):
        self.parser = None
        self.build()
    
    # Grammar rules
    
    # Program structure
    def p_program(self, p):
        '''program : translation_unit'''
        p[0] = Program(p[1])
    
    def p_translation_unit(self, p):
        '''translation_unit : external_declaration
                           | translation_unit external_declaration'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[1].append(p[2])
            p[0] = p[1]
    
    def p_external_declaration(self, p):
        '''external_declaration : function_definition
                               | declaration'''
        p[0] = p[1]
    
    # Function definitions
    def p_function_definition(self, p):
        '''function_definition : type_specifier IDENTIFIER LPAREN parameter_list RPAREN compound_statement
                              | type_specifier IDENTIFIER LPAREN RPAREN compound_statement'''
        if len(p) == 6:
            p[0] = FunctionDecl(p[1], p[2], [], p[5])
        else:
            p[0] = FunctionDecl(p[1], p[2], p[4], p[6])
    
    def p_parameter_list(self, p):
        '''parameter_list : parameter_declaration
                         | parameter_list COMMA parameter_declaration'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[1].append(p[3])
            p[0] = p[1]
    
    def p_parameter_declaration(self, p):
        '''parameter_declaration : type_specifier IDENTIFIER
                                | type_specifier'''
        if len(p) == 3:
            p[0] = Parameter(p[1], p[2])
        else:
            p[0] = Parameter(p[1], None)
    
    # Type system
    def p_type_specifier(self, p):
        '''type_specifier : VOID
                         | CHAR
                         | SHORT
                         | INT
                         | LONG
                         | FLOAT
                         | DOUBLE
                         | SIGNED
                         | UNSIGNED
                         | BOOL
                         | signed_type
                         | unsigned_type'''
        p[0] = BasicType(p[1])
    
    def p_signed_type(self, p):
        '''signed_type : SIGNED CHAR
                      | SIGNED SHORT
                      | SIGNED INT
                      | SIGNED LONG'''
        p[0] = f"signed {p[2]}"
    
    def p_unsigned_type(self, p):
        '''unsigned_type : UNSIGNED CHAR
                        | UNSIGNED SHORT  
                        | UNSIGNED INT
                        | UNSIGNED LONG'''
        p[0] = f"unsigned {p[2]}"
    
    # Declarations
    def p_declaration(self, p):
        '''declaration : type_specifier init_declarator_list SEMICOLON'''
        p[0] = VariableDecl(p[1], p[2])
    
    def p_init_declarator_list(self, p):
        '''init_declarator_list : init_declarator
                               | init_declarator_list COMMA init_declarator'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[1].append(p[3])
            p[0] = p[1]
    
    def p_init_declarator(self, p):
        '''init_declarator : declarator
                          | declarator ASSIGN initializer'''
        if len(p) == 2:
            p[0] = Declarator(p[1])
        else:
            p[0] = Declarator(p[1], p[3])
    
    def p_declarator(self, p):
        '''declarator : IDENTIFIER
                     | TIMES declarator
                     | declarator LBRACKET RBRACKET
                     | declarator LBRACKET constant_expression RBRACKET'''
        if len(p) == 2:
            p[0] = p[1]  # Simple identifier
        elif p[1] == '*':
            p[0] = PointerType(p[2])  # Pointer declarator
        elif len(p) == 4:
            p[0] = ArrayType(p[1])  # Array without size
        else:
            p[0] = ArrayType(p[1], p[3])  # Array with size
    
    def p_initializer(self, p):
        '''initializer : assignment_expression
                      | LBRACE initializer_list RBRACE
                      | LBRACE initializer_list COMMA RBRACE'''
        if len(p) == 2:
            p[0] = ExpressionInitializer(p[1])
        else:
            p[0] = InitializerList(p[2])
    
    def p_initializer_list(self, p):
        '''initializer_list : initializer
                           | initializer_list COMMA initializer'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[1].append(p[3])
            p[0] = p[1]
    
    # Statements
    def p_statement(self, p):
        '''statement : compound_statement
                    | expression_statement
                    | selection_statement
                    | iteration_statement
                    | jump_statement
                    | declaration'''
        p[0] = p[1]
    
    def p_compound_statement(self, p):
        '''compound_statement : LBRACE RBRACE
                             | LBRACE statement_list RBRACE'''
        if len(p) == 3:
            p[0] = CompoundStmt([])
        else:
            p[0] = CompoundStmt(p[2])
    
    def p_statement_list(self, p):
        '''statement_list : statement
                         | statement_list statement'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[1].append(p[2])
            p[0] = p[1]
    
    def p_expression_statement(self, p):
        '''expression_statement : SEMICOLON
                               | expression SEMICOLON'''
        if len(p) == 2:
            p[0] = ExpressionStmt(None)
        else:
            p[0] = ExpressionStmt(p[1])
    
    # Selection statements (if-else)
    def p_selection_statement(self, p):
        '''selection_statement : IF LPAREN expression RPAREN statement
                              | IF LPAREN expression RPAREN statement ELSE statement
                              | SWITCH LPAREN expression RPAREN statement'''
        if len(p) == 6:
            if p[1] == 'if':
                p[0] = IfStmt(p[3], p[5])
            else:  # switch
                p[0] = SwitchStmt(p[3], p[5])
        else:  # if-else
            p[0] = IfStmt(p[3], p[5], p[7])
    
    # Iteration statements
    def p_iteration_statement(self, p):
        '''iteration_statement : WHILE LPAREN expression RPAREN statement
                              | FOR LPAREN expression_statement expression_statement RPAREN statement
                              | FOR LPAREN expression_statement expression_statement expression RPAREN statement
                              | DO statement WHILE LPAREN expression RPAREN SEMICOLON'''
        if p[1] == 'while':
            p[0] = WhileStmt(p[3], p[5])
        elif p[1] == 'for':
            if len(p) == 7:
                p[0] = ForStmt(p[3], p[4], None, p[6])
            else:
                p[0] = ForStmt(p[3], p[4], p[5], p[7])
        else:  # do-while
            p[0] = DoWhileStmt(p[2], p[5])
    
    # Jump statements
    def p_jump_statement(self, p):
        '''jump_statement : BREAK SEMICOLON
                         | CONTINUE SEMICOLON
                         | RETURN SEMICOLON
                         | RETURN expression SEMICOLON'''
        if p[1] == 'break':
            p[0] = BreakStmt()
        elif p[1] == 'continue':
            p[0] = ContinueStmt()
        elif len(p) == 3:
            p[0] = ReturnStmt()
        else:
            p[0] = ReturnStmt(p[2])
    
    # Expressions
    def p_expression(self, p):
        '''expression : assignment_expression
                     | expression COMMA assignment_expression'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = BinaryOp(p[1], ',', p[3])
    
    def p_assignment_expression(self, p):
        '''assignment_expression : conditional_expression
                                | unary_expression assignment_operator assignment_expression'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = AssignmentExpr(p[1], p[2], p[3])
    
    def p_assignment_operator(self, p):
        '''assignment_operator : ASSIGN
                              | TIMES_ASSIGN
                              | DIVIDE_ASSIGN
                              | PLUS_ASSIGN
                              | MINUS_ASSIGN'''
        p[0] = p[1]
    
    def p_conditional_expression(self, p):
        '''conditional_expression : logical_or_expression
                                 | logical_or_expression QUESTION expression COLON conditional_expression'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = TernaryOp(p[1], p[3], p[5])
    
    def p_constant_expression(self, p):
        '''constant_expression : conditional_expression'''
        p[0] = p[1]
    
    def p_logical_or_expression(self, p):
        '''logical_or_expression : logical_and_expression
                                | logical_or_expression OR logical_and_expression'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = BinaryOp(p[1], p[2], p[3])
    
    def p_logical_and_expression(self, p):
        '''logical_and_expression : bitwise_or_expression
                                 | logical_and_expression AND bitwise_or_expression'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = BinaryOp(p[1], p[2], p[3])
    
    def p_bitwise_or_expression(self, p):
        '''bitwise_or_expression : bitwise_xor_expression
                                | bitwise_or_expression BITWISE_OR bitwise_xor_expression'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = BinaryOp(p[1], p[2], p[3])
    
    def p_bitwise_xor_expression(self, p):
        '''bitwise_xor_expression : bitwise_and_expression
                                 | bitwise_xor_expression BITWISE_XOR bitwise_and_expression'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = BinaryOp(p[1], p[2], p[3])
    
    def p_bitwise_and_expression(self, p):
        '''bitwise_and_expression : equality_expression
                                 | bitwise_and_expression BITWISE_AND equality_expression'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = BinaryOp(p[1], p[2], p[3])
    
    def p_equality_expression(self, p):
        '''equality_expression : relational_expression
                              | equality_expression EQ relational_expression
                              | equality_expression NE relational_expression'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = BinaryOp(p[1], p[2], p[3])
    
    def p_relational_expression(self, p):
        '''relational_expression : shift_expression
                                | relational_expression LT shift_expression
                                | relational_expression GT shift_expression
                                | relational_expression LE shift_expression
                                | relational_expression GE shift_expression'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = BinaryOp(p[1], p[2], p[3])
    
    def p_shift_expression(self, p):
        '''shift_expression : additive_expression
                           | shift_expression LSHIFT additive_expression
                           | shift_expression RSHIFT additive_expression'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = BinaryOp(p[1], p[2], p[3])
    
    def p_additive_expression(self, p):
        '''additive_expression : multiplicative_expression
                              | additive_expression PLUS multiplicative_expression
                              | additive_expression MINUS multiplicative_expression'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = BinaryOp(p[1], p[2], p[3])
    
    def p_multiplicative_expression(self, p):
        '''multiplicative_expression : cast_expression
                                    | multiplicative_expression TIMES cast_expression
                                    | multiplicative_expression DIVIDE cast_expression
                                    | multiplicative_expression MODULO cast_expression'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = BinaryOp(p[1], p[2], p[3])
    
    def p_cast_expression(self, p):
        '''cast_expression : unary_expression
                          | LPAREN type_specifier RPAREN cast_expression'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = CastExpr(p[2], p[4])
    
    def p_unary_expression(self, p):
        '''unary_expression : postfix_expression
                           | INCREMENT unary_expression
                           | DECREMENT unary_expression
                           | unary_operator cast_expression
                           | SIZEOF unary_expression
                           | SIZEOF LPAREN type_specifier RPAREN'''
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 3:
            if p[1] in ['++', '--']:
                p[0] = UnaryOp(p[1], p[2], prefix=True)
            elif p[1] == 'sizeof':
                p[0] = SizeofExpr(p[2])
            else:
                p[0] = UnaryOp(p[1], p[2])
        else:  # sizeof(type)
            p[0] = SizeofExpr(p[3])
    
    def p_unary_operator(self, p):
        '''unary_operator : BITWISE_AND
                         | TIMES
                         | PLUS
                         | MINUS
                         | BITWISE_NOT
                         | NOT'''
        p[0] = p[1]
    
    def p_postfix_expression(self, p):
        '''postfix_expression : primary_expression
                             | postfix_expression LBRACKET expression RBRACKET
                             | postfix_expression LPAREN RPAREN
                             | postfix_expression LPAREN argument_expression_list RPAREN
                             | postfix_expression DOT IDENTIFIER
                             | postfix_expression ARROW IDENTIFIER
                             | postfix_expression INCREMENT
                             | postfix_expression DECREMENT'''
        if len(p) == 2:
            p[0] = p[1]
        elif p[2] == '[':
            p[0] = ArrayAccess(p[1], p[3])
        elif p[2] == '(':
            if len(p) == 4:
                p[0] = FunctionCall(p[1], [])
            else:
                p[0] = FunctionCall(p[1], p[3])
        elif p[2] == '.':
            p[0] = MemberAccess(p[1], p[3], is_pointer=False)
        elif p[2] == '->':
            p[0] = MemberAccess(p[1], p[3], is_pointer=True)
        else:  # ++ or --
            p[0] = UnaryOp(p[2], p[1], prefix=False)
    
    def p_primary_expression(self, p):
        '''primary_expression : IDENTIFIER
                             | constant
                             | STRING_LITERAL
                             | LPAREN expression RPAREN'''
        if len(p) == 2:
            if isinstance(p[1], str) and p[1].isalpha():
                p[0] = Identifier(p[1])
            elif isinstance(p[1], str) and p[1].startswith('"'):
                p[0] = StringLiteral(p[1])
            else:
                p[0] = p[1]
        else:
            p[0] = p[2]  # Parenthesized expression
    
    def p_argument_expression_list(self, p):
        '''argument_expression_list : assignment_expression
                                   | argument_expression_list COMMA assignment_expression'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[1].append(p[3])
            p[0] = p[1]
    
    def p_constant(self, p):
        '''constant : NUMBER
                   | FLOAT_NUM
                   | CHAR_LITERAL'''
        if isinstance(p[1], int):
            p[0] = IntegerLiteral(p[1])
        elif isinstance(p[1], float):
            p[0] = FloatLiteral(p[1])
        else:
            p[0] = CharLiteral(p[1])
    
    def p_error(self, p):
        if p:
            print(f"Syntax error at token {p.type} ('{p.value}') at line {p.lineno}")
        else:
            print("Syntax error at EOF")
    
    def build(self, **kwargs):
        """Build the parser"""
        self.parser = yacc.yacc(module=self, **kwargs)
        return self.parser
    
    def parse(self, input_text, lexer):
        """Parse input text using the given lexer"""
        return self.parser.parse(input_text, lexer=lexer.lexer)

def build_parser():
    """Factory function to build and return a parser"""
    return Parser()

if __name__ == "__main__":
    # Test the parser
    from ..lexer.lexer import build_lexer
    
    parser = build_parser()
    lexer = build_lexer()
    
    test_code = '''
    int factorial(int n) {
        if (n <= 1) {
            return 1;
        } else {
            return n * factorial(n - 1);
        }
    }
    
    int main() {
        int result = factorial(5);
        printf("Factorial of 5 is %d\\n", result);
        return 0;
    }
    '''
    
    print("Testing parser:")
    print("=" * 50)
    try:
        ast = parser.parse(test_code, lexer)
        print("SUCCESS - Parsing successful!")
        print(f"AST: {ast}")
    except Exception as e:
        print(f"ERROR - Parsing failed: {e}")
