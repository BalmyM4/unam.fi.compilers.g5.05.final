#!/usr/bin/env python3

from lexer import lexer

def debug_lexer(filename):
    try:
        with open(filename, 'r') as f:
            content = f.read()
        
        print(f"File content ({len(content)} chars):")
        print(repr(content[:100]))
        print()
        
        lexer.input(content)
        
        tokens = []
        while True:
            tok = lexer.token()
            if not tok:
                break
            tokens.append(tok)
            print(f"Token: {tok.type} = '{tok.value}' (line {tok.lineno})")
        
        print(f"\nTotal tokens: {len(tokens)}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_lexer("test_simple_nested.c")
