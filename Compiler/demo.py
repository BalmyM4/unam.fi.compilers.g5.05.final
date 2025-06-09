#!/usr/bin/env python3

"""
C-like Language Compiler Demo
============================

This script demonstrates the complete compiler pipeline for a C-like language
that supports if-else statements, variable declarations, and basic arithmetic.

Compiler Components:
1. Lexer (lexer.py) - Tokenizes input source code
2. Parser (parser.py) - Creates Abstract Syntax Tree (AST)
3. Semantic Analyzer (semantic_analyzer.py) - Checks for semantic errors
4. Code Generator (code_generator.py) - Generates assembly code
"""

import os
from compiler import Compiler

def demo_compiler():
    print("=" * 60)
    print("C-like Language Compiler Demonstration")
    print("=" * 60)
    print()
    
    # Test cases
    test_cases = [
        ("Test 1: Simple if-else", "tests/samples/test1.c"),
        ("Test 2: Nested if statements", "tests/samples/test2.c"), 
        ("Test 3: Complex expressions", "tests/samples/test3.c"),
        ("Test 4: Error detection", "tests/samples/test4_error.c")
    ]
    
    compiler = Compiler()
    
    for test_name, test_file in test_cases:
        print(f"{test_name}")
        print("-" * len(test_name))
        
        if os.path.exists(test_file):
            try:
                with open(test_file, 'r') as f:
                    source = f.read()
                
                print("Source code:")
                print(source)
                print()
                
                output_file = test_file.replace('.c', '.asm')
                success = compiler.compile(source, output_file)
                
                if success:
                    print(f"SUCCESS - Compilation successful! Output: {output_file}")
                else:
                    print("FAILED - Compilation failed!")
            except Exception as e:
                print(f"ERROR - Error processing {test_file}: {e}")
        else:
            print(f"ERROR - Test file {test_file} not found!")
        
        print()
        print("=" * 60)
        print()

if __name__ == "__main__":
    demo_compiler()
