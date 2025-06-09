#!/usr/bin/env python3

"""
Token definitions for the C-like language compiler
Defines all tokens that the lexer can recognize
"""

# Reserved words/keywords
reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'do': 'DO',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'return': 'RETURN',
    'switch': 'SWITCH',
    'case': 'CASE',
    'default': 'DEFAULT',
    
    # Data types
    'int': 'INT',
    'float': 'FLOAT', 
    'double': 'DOUBLE',
    'char': 'CHAR',
    'void': 'VOID',
    'short': 'SHORT',
    'long': 'LONG',
    'unsigned': 'UNSIGNED',
    'signed': 'SIGNED',
    'bool': 'BOOL',
    
    # Storage classes
    'static': 'STATIC',
    'extern': 'EXTERN',
    'auto': 'AUTO',
    'register': 'REGISTER',
    'const': 'CONST',
    'volatile': 'VOLATILE',
    
    # Built-in functions
    'printf': 'PRINTF',
    'scanf': 'SCANF',
    'malloc': 'MALLOC',
    'free': 'FREE',
    'sizeof': 'SIZEOF',
}

# Token list - includes reserved words and other tokens
tokens = (
    # Literals
    'IDENTIFIER', 'NUMBER', 'FLOAT_NUM', 'CHAR_LITERAL', 'STRING_LITERAL',
    
    # Arithmetic operators
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MODULO',
    'INCREMENT', 'DECREMENT',
    
    # Assignment operators
    'ASSIGN', 'PLUS_ASSIGN', 'MINUS_ASSIGN', 'TIMES_ASSIGN', 'DIVIDE_ASSIGN',
    
    # Comparison operators  
    'EQ', 'NE', 'LT', 'LE', 'GT', 'GE',
    
    # Logical operators
    'AND', 'OR', 'NOT',
    
    # Bitwise operators
    'BITWISE_AND', 'BITWISE_OR', 'BITWISE_XOR', 'BITWISE_NOT', 'LSHIFT', 'RSHIFT',
    
    # Punctuation
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'LBRACKET', 'RBRACKET',
    'SEMICOLON', 'COMMA', 'DOT', 'ARROW',
      # Other operators
    'QUESTION', 'COLON', 'ADDRESS', 'DEREFERENCE',
) + tuple(reserved.values())

# Token precedence and associativity
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'BITWISE_OR'),
    ('left', 'BITWISE_XOR'),
    ('left', 'BITWISE_AND'),
    ('left', 'EQ', 'NE'),
    ('left', 'LT', 'LE', 'GT', 'GE'),
    ('left', 'LSHIFT', 'RSHIFT'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MODULO'),
    ('right', 'NOT', 'BITWISE_NOT', 'ADDRESS', 'DEREFERENCE'),
    ('left', 'INCREMENT', 'DECREMENT'),
    ('left', 'DOT', 'ARROW'),
    ('left', 'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET'),
)
