#!/usr/bin/env python3

print("Testing PLY functionality...")

import ply.lex as lex

# Simple tokens
tokens = ('NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN')

# Token rules
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = ' \t'

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

print("Building lexer...")
lexer = lex.lex()

print("Testing tokenization...")
test_data = "3 + 4 * 10"
lexer.input(test_data)

print(f"Input: {test_data}")
print("Tokens:")
while True:
    tok = lexer.token()
    if not tok:
        break
    print(f"  {tok}")

print("PLY test completed successfully!")
