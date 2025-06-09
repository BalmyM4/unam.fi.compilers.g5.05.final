#!/usr/bin/env python3

"""
Lexical Analyzer for C-like Language
Tokenizes C-like source code for compilation
"""

import ply.lex as lex
try:
    from .tokens import tokens, reserved
except ImportError:
    from tokens import tokens, reserved

class Lexer:
    """Lexer for C-like language with comprehensive token support"""
    
    # Include tokens from tokens.py
    tokens = tokens
    
    def __init__(self):
        self.lexer = None
        self.build()
    
    # Token rules for complex operators (order matters!)
    t_PLUS_ASSIGN   = r'\+='
    t_MINUS_ASSIGN  = r'-='
    t_TIMES_ASSIGN  = r'\*='
    t_DIVIDE_ASSIGN = r'/='
    t_INCREMENT     = r'\+\+'
    t_DECREMENT     = r'--'
    
    # Comparison operators
    t_EQ       = r'=='
    t_NE       = r'!='
    t_LE       = r'<='
    t_GE       = r'>='
    t_LT       = r'<'
    t_GT       = r'>'
    
    # Logical operators  
    t_AND      = r'&&'
    t_OR       = r'\|\|'
    t_NOT      = r'!'
    
    # Bitwise operators
    t_BITWISE_AND = r'&'
    t_BITWISE_OR  = r'\|'
    t_BITWISE_XOR = r'\^'
    t_BITWISE_NOT = r'~'
    t_LSHIFT      = r'<<'
    t_RSHIFT      = r'>>'
    
    # Arithmetic operators
    t_PLUS     = r'\+'
    t_MINUS    = r'-'
    t_TIMES    = r'\*'
    t_DIVIDE   = r'/'
    t_MODULO   = r'%'
    t_ASSIGN   = r'='
    
    # Punctuation
    t_LPAREN   = r'\('
    t_RPAREN   = r'\)'
    t_LBRACE   = r'\{'
    t_RBRACE   = r'\}'
    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'
    t_SEMICOLON = r';'
    t_COMMA    = r','
    t_DOT      = r'\.'
    t_ARROW    = r'->'
    t_QUESTION = r'\?'
    t_COLON    = r':'
    
    # Address and dereference (same as bitwise operators in different contexts)
    t_ADDRESS     = t_BITWISE_AND  # &
    t_DEREFERENCE = t_TIMES        # *
    
    def t_FLOAT_NUM(self, t):
        r'''
        \d+\.\d+([eE][+-]?\d+)?[fFlL]? |
        \d+[eE][+-]?\d+[fFlL]? |
        \.\d+([eE][+-]?\d+)?[fFlL]?
        '''
        # Handle floating point numbers with optional suffixes
        value = t.value.rstrip('fFlL')
        try:
            t.value = float(value)
        except ValueError:
            print(f"Invalid float literal '{t.value}' at line {t.lineno}")
            t.value = 0.0
        return t
    
    def t_NUMBER(self, t):
        r'''
        0[xX][0-9a-fA-F]+[uUlL]* |
        0[0-7]+[uUlL]* |
        \d+[uUlL]*
        '''
        # Handle integers (decimal, octal, hexadecimal) with optional suffixes
        value = t.value.rstrip('uUlL')
        try:
            if value.startswith('0x') or value.startswith('0X'):
                t.value = int(value, 16)  # Hexadecimal
            elif value.startswith('0') and len(value) > 1:
                t.value = int(value, 8)   # Octal
            else:
                t.value = int(value, 10)  # Decimal
        except ValueError:
            print(f"Invalid number literal '{t.value}' at line {t.lineno}")
            t.value = 0
        return t
    
    def t_CHAR_LITERAL(self, t):
        r"'([^'\\\\]|\\\\.|\\\\[0-7]{1,3}|\\\\x[0-9a-fA-F]{1,2})'"
        # Handle character literals including escape sequences
        char_content = t.value[1:-1]  # Remove quotes
        
        if len(char_content) == 1:
            t.value = ord(char_content)
        elif char_content.startswith('\\'):
            # Handle escape sequences
            escape_map = {
                'n': ord('\n'), 't': ord('\t'), 'r': ord('\r'),
                'b': ord('\b'), 'f': ord('\f'), 'v': ord('\v'),
                'a': ord('\a'), '0': 0, '\\': ord('\\'),
                '\'': ord('\''), '\"': ord('\"')
            }
            
            if len(char_content) == 2 and char_content[1] in escape_map:
                t.value = escape_map[char_content[1]]
            elif char_content[1:].isdigit():  # Octal escape
                t.value = int(char_content[1:], 8)
            elif char_content.startswith('\\x'):  # Hex escape
                t.value = int(char_content[2:], 16)
            else:
                print(f"Invalid escape sequence '{char_content}' at line {t.lineno}")
                t.value = 0
        else:
            print(f"Invalid character literal '{t.value}' at line {t.lineno}")
            t.value = 0
        
        return t
    
    def t_STRING_LITERAL(self, t):
        r'"([^"\\\\]|\\\\.|\\\\[0-7]{1,3}|\\\\x[0-9a-fA-F]{1,2})*"'        # Handle string literals with escape sequences
        t.value = t.value[1:-1]  # Remove quotes
        # TODO: Process escape sequences in strings
        return t
    
    def t_IDENTIFIER(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        # Check if it's a reserved word
        t.type = reserved.get(t.value, 'IDENTIFIER')
        return t
    
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)
        # Don't return newline token - treat as whitespace
        pass
    
    def t_COMMENT_SINGLE(self, t):
        r'//.*'
        pass  # Ignore single-line comments
    
    def t_COMMENT_MULTI(self, t):
        r'/\*(.|\n)*?\*/'
        # Count newlines in multi-line comments
        t.lexer.lineno += t.value.count('\n')
        pass  # Ignore multi-line comments
    
    def t_PREPROCESSOR(self, t):
        r'\#.*'
        pass  # Ignore preprocessor directives for now
    
    # Ignored characters (spaces and tabs)
    t_ignore = ' \t'
    
    def t_error(self, t):
        print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
        t.lexer.skip(1)
    
    def build(self, **kwargs):
        """Build the lexer"""
        self.lexer = lex.lex(module=self, **kwargs)
        return self.lexer
    
    def test(self, data):
        """Test the lexer with input data"""
        self.lexer.input(data)
        tokens = []
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            tokens.append(tok)
        return tokens
    
    def tokenize(self, data):
        """Tokenize input data and return list of tokens"""
        return self.test(data)

def build_lexer():
    """Factory function to build and return a lexer"""
    return Lexer()

if __name__ == "__main__":
    # Test the lexer
    lexer = build_lexer()
    
    test_code = '''
    int main() {
        float x = 3.14f;
        double y = 2.71828;
        char c = 'A';
        unsigned int count = 0xFF;
        
        printf("Hello, %s!\\n", "World");
        
        if (x > 0.0) {
            count++;
            return factorial(5);
        }
        
        return 0;
    }
    '''
    
    print("Testing lexer:")
    print("=" * 50)
    tokens = lexer.tokenize(test_code)
    
    for i, token in enumerate(tokens):
        print(f"{i+1:2}: {token.type:15} {repr(token.value):20} (line {token.lineno})")
