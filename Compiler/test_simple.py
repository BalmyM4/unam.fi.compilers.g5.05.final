#!/usr/bin/env python3

# Simple test to check lexer functionality
def test_simple():
    try:
        from src.lexer.lexer import build_lexer
        from src.lexer.tokens import tokens
        print("PASS - Lexer import successful")
        print(f"Tokens defined: {len(tokens)}")
          # Build lexer instance
        lexer = build_lexer()
        
        # Test with simple input
        test_input = "int x = 5;"
        token_list = list(lexer.tokenize(test_input))
        
        for tok in token_list:
            print(f"Token: {tok.type} = '{tok.value}'")
        
        print(f"PASS - Lexer test passed with {len(token_list)} tokens")
        return True
        
    except Exception as e:
        print(f"FAIL - Lexer test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_simple()
