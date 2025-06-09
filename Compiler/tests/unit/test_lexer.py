#!/usr/bin/env python3

import ply.lex as lex
from keywords import keywords

# Test lexer functionality
def test_lexer():
    # Different classification of tokens
    tokens = (
        'IF', 'ELSE', 'WHILE', 'FOR', 'RETURN',
        'INT', 'FLOAT', 'CHAR', 'VOID', 'MAIN', 'PRINTF', 'SCANF',
        'IDENTIFIER', 'NUMBER', 'STRING',
        'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MODULO',
        'ASSIGN', 'EQ', 'NE', 'LT', 'LE', 'GT', 'GE',
        'AND', 'OR', 'NOT',
        'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
        'SEMICOLON', 'COMMA',
    )

    # Define a rule so we can track line numbers
    def t_newline(t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # Token rules for simple tokens
    t_PLUS     = r'\+'
    t_MINUS    = r'-'
    t_TIMES    = r'\*'
    t_DIVIDE   = r'/'
    t_MODULO   = r'%'
    t_EQ       = r'=='
    t_NE       = r'!='
    t_LE       = r'<='
    t_GE       = r'>='
    t_LT       = r'<'
    t_GT       = r'>'
    t_AND      = r'&&'
    t_OR       = r'\|\|'
    t_NOT      = r'!'
    t_ASSIGN   = r'='
    t_LPAREN   = r'\('
    t_RPAREN   = r'\)'
    t_LBRACE   = r'\{'
    t_RBRACE   = r'\}'
    t_SEMICOLON = r';'
    t_COMMA    = r','

    # function for checking if it is reserved keyword or identifier
    def t_IDENTIFIER(t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        # if it can not be found in keyword dictionary it is an identifier
        t.type = keywords.get(t.value, 'IDENTIFIER')
        return t

    # function for identifying numbers
    def t_NUMBER(t):
        r'\d+(\.\d+)?'
        if '.' in t.value:
            t.value = float(t.value)
        else:
            t.value = int(t.value)
        return t

    # function for identifying string literals
    def t_STRING(t):
        r'"([^"\\\\]|\\\\.)*"'
        t.value = t.value[1:-1]  # Remove quotes
        return t

    # function for handling errors
    def t_error(t):
        print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
        t.lexer.skip(1)

    t_ignore = ' \t'
    t_ignore_COMMENT = r'//.*'

    # Build lexer
    lexer = lex.lex()
    
    # Test with simple code
    test_code = '''
    int main() {
        int x = 10;
        if (x > 5) {
            x = x + 1;
        }
        return x;
    }
    '''
    
    lexer.input(test_code)
    
    print("Testing lexer:")
    tokens_list = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens_list.append(tok)
        print(f"{tok.type:<12} {str(tok.value):<10} line {tok.lineno}")
    
    print(f"\nTotal tokens: {len(tokens_list)}")
    return True

if __name__ == "__main__":
    test_lexer()
