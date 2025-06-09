#!/usr/bin/env python3

import sys
import os

print("Starting simple test...")

# Add the project root to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, project_root)

print(f"Current directory: {current_dir}")
print(f"Project root: {project_root}")
print(f"Python path: {sys.path[:3]}")

try:
    print("Importing tokens...")
    from src.lexer.tokens import TokenType
    print("Tokens imported successfully")

    print("Importing lexer...")
    from src.lexer.lexer import Lexer
    print("Lexer imported successfully")

    # Test basic tokenization
    lexer = Lexer()
    print("Lexer created successfully")

    test_code = "int x = 42;"
    print(f"Tokenizing: {test_code}")

    tokens = list(lexer.tokenize(test_code))
    print(f"Generated {len(tokens)} tokens:")
    for i, token in enumerate(tokens):
        print(f"  {i+1}: {token}")

    print("=== LEXER TEST SUCCESSFUL ===")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
