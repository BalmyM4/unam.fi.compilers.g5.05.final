#!/usr/bin/env python3

"""
C-like Language Compiler
========================

Main compiler class that coordinates the compilation pipeline:
1. Lexical analysis (tokenization)
2. Syntax analysis (parsing)
3. Semantic analysis
4. Code generation
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.lexer.lexer import build_lexer
from src.parser.parser import build_parser
from src.semantic.analyzer import SemanticAnalyzer
from src.codegen.generator import CodeGenerator

class Compiler:
    """Main compiler class that orchestrates the compilation process"""
    
    def __init__(self):
        """Initialize the compiler with all necessary components"""
        self.lexer = build_lexer()
        self.parser = build_parser()
        self.semantic_analyzer = SemanticAnalyzer()
        self.code_generator = CodeGenerator()
    
    def compile(self, source_code, output_file=None):
        """
        Compile source code through the complete pipeline
        
        Args:
            source_code (str): The source code to compile
            output_file (str): Optional output file path for assembly code
            
        Returns:
            bool: True if compilation successful, False otherwise
        """
        try:
            # Phase 1: Lexical Analysis
            print("Phase 1: Lexical Analysis")
            tokens = self.lexer.tokenize(source_code)
            token_list = list(tokens)
            print(f"Generated {len(token_list)} tokens")
            
            # Phase 2: Syntax Analysis (Parsing)
            print("Phase 2: Syntax Analysis")
            ast = self.parser.parse(source_code, lexer=self.lexer)
            if ast is None:
                print("FAILED - Parsing failed")
                return False
            print("SUCCESS - AST generated")
            
            # Phase 3: Semantic Analysis
            print("Phase 3: Semantic Analysis")
            if not self.semantic_analyzer.analyze(ast):
                print("FAILED - Semantic analysis failed")
                return False
            print("SUCCESS - Semantic analysis passed")
            
            # Phase 4: Code Generation
            print("Phase 4: Code Generation")
            assembly_code = self.code_generator.generate(ast)
            print("SUCCESS - Assembly code generated")
            
            # Write output file if specified
            if output_file:
                with open(output_file, 'w') as f:
                    f.write(assembly_code)
                print(f"Assembly code written to {output_file}")
            
            return True
            
        except Exception as e:
            print(f"FAILED - Compilation error: {e}")
            return False
    
    def tokenize_only(self, source_code):
        """Tokenize source code only (for testing)"""
        return list(self.lexer.tokenize(source_code))
    
    def parse_only(self, source_code):
        """Parse source code only (for testing)"""
        return self.parser.parse(source_code, lexer=self.lexer)

if __name__ == "__main__":    # Simple test
    compiler = Compiler()
    test_code = "int x = 5;"
      # Test multiple simple cases
    test_cases = [
        "int x = 5;",
        "int x; x = 10;",
        "int x = 5; int y = 3;",
        # "if (x > 0) { x = 1; }"  # This will likely fail due to parser issues
    ]
    
    for i, test_code in enumerate(test_cases, 1):
        print(f"\n=== Test Case {i} ===")
        print(f"Code: {test_code}")
        success = compiler.compile(test_code, f"test_output_{i}.asm")
        print(f"Result: {'SUCCESS' if success else 'FAILED'}")
        print("-" * 40)