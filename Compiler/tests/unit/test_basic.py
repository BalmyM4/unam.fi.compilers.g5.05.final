import sys
print("Test script starting...", flush=True)
sys.stdout.flush()

try:
    print("Testing basic imports...", flush=True)
    from lexer import lexer
    print("Lexer import successful!", flush=True)
    
    # Test tokenization
    test_code = "int x = 5;"
    lexer.input(test_code)
    
    tokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens.append(tok)
    
    print(f"Tokenized {len(tokens)} tokens from test code", flush=True)
    
    if tokens:
        for i, tok in enumerate(tokens):
            print(f"Token {i+1}: {tok.type} = {tok.value}", flush=True)
    
    print("SUCCESS: Basic test completed!", flush=True)
    
except Exception as e:
    print(f"ERROR: {e}", flush=True)
    import traceback
    traceback.print_exc()
    sys.stdout.flush()
