#!/usr/bin/env python3

# Simple test to check parser functionality
def test_parser():
    try:        from lexer import tokens
        print("Lexer tokens imported successfully")

        import ply.yacc as yacc
        print("PLY yacc imported successfully")

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
        print("Parser built successfully")
        
        return True
        
    except Exception as e:
        print("Parser test failed:", e)
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_parser()
