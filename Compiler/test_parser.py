#!/usr/bin/env python3

# Simple test to check parser functionality
def test_parser():
    try:
        from src.lexer.tokens import tokens
        print("PASS - Lexer tokens imported")
        
        import ply.yacc as yacc
        print("PASS - PLY yacc imported")
        
        # Simple test rule
        def p_test(p):
            '''test : INT IDENTIFIER ASSIGN NUMBER SEMICOLON'''
            p[0] = "test_rule"
        
        def p_error(p):
            if p:
                print(f"Syntax error at token {p.type}")
            else:
                print("Syntax error at EOF")
        
        parser = yacc.yacc()
        print("PASS - Parser built successfully")
        
        return True
        
    except Exception as e:
        print(f"FAIL - Parser test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_parser()
