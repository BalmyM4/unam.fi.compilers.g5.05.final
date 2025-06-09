#!/usr/bin/env python3

# Simple test to check lexer functionality
def test_simple():
    try:
        from lexer import lexer, tokens
        print("Lexer import successful")
        print(f"Tokens defined: {len(tokens)}")
        
        # Test with simple input
        test_input = "int x = 5;"
        lexer.input(test_input)
        
        token_list = []
        while True:
            tok = lexer.token()
            if not tok:
                break
            token_list.append(tok)
            print(f"Token: {tok.type} = '{tok.value}'")
        
        print(f"Lexer test passed with {len(token_list)} tokens")
        return True
        
    except Exception as e:
        print(f"Lexer test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_simple()
