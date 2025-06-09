#!/usr/bin/env python3

"""
Comprehensive Test Suite for C-like Compiler
Tests all phases: lexing, parsing, semantic analysis, and code generation
"""

import sys
import os
import tempfile
import unittest
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.lexer.lexer import Lexer
from src.lexer.tokens import TokenType
from src.parser.parser import Parser
from src.semantic.analyzer import SemanticAnalyzer
from src.codegen.generator import CodeGenerator

class TestLexer(unittest.TestCase):
    """Test the lexer"""
    
    def setUp(self):
        self.lexer = Lexer()
    
    def test_basic_tokens(self):
        """Test basic token recognition"""
        source = "int main() { return 0; }"
        tokens = list(self.lexer.tokenize(source))
        
        expected_types = [
            TokenType.INT, TokenType.IDENTIFIER, TokenType.LPAREN, TokenType.RPAREN,
            TokenType.LBRACE, TokenType.RETURN, TokenType.INTEGER, TokenType.SEMICOLON,
            TokenType.RBRACE, TokenType.EOF
        ]
        
        actual_types = [token.type for token in tokens]
        self.assertEqual(actual_types, expected_types)
    
    def test_data_types(self):
        """Test all C data types"""
        source = "char short int long float double void"
        tokens = list(self.lexer.tokenize(source))
        
        expected_types = [
            TokenType.CHAR, TokenType.SHORT, TokenType.INT, TokenType.LONG,
            TokenType.FLOAT, TokenType.DOUBLE, TokenType.VOID, TokenType.EOF
        ]
        
        actual_types = [token.type for token in tokens]
        self.assertEqual(actual_types, expected_types)
    
    def test_operators(self):
        """Test operator recognition"""
        source = "+ - * / % == != < <= > >= && || ! & | ^ << >>"
        tokens = list(self.lexer.tokenize(source))
        
        operators = [token.value for token in tokens if token.type != TokenType.EOF]
        expected = ['+', '-', '*', '/', '%', '==', '!=', '<', '<=', '>', '>=', 
                   '&&', '||', '!', '&', '|', '^', '<<', '>>']
        
        self.assertEqual(operators, expected)
    
    def test_literals(self):
        """Test different literal types"""
        source = '42 3.14 "hello" \'A\' 0xFF 0777'
        tokens = list(self.lexer.tokenize(source))
        
        # Filter out EOF token
        tokens = [t for t in tokens if t.type != TokenType.EOF]
        
        self.assertEqual(tokens[0].type, TokenType.INTEGER)
        self.assertEqual(tokens[0].value, 42)
        
        self.assertEqual(tokens[1].type, TokenType.FLOAT)
        self.assertEqual(tokens[1].value, 3.14)
        
        self.assertEqual(tokens[2].type, TokenType.STRING)
        self.assertEqual(tokens[2].value, "hello")
        
        self.assertEqual(tokens[3].type, TokenType.CHAR)
        self.assertEqual(tokens[3].value, 'A')
        
        self.assertEqual(tokens[4].type, TokenType.INTEGER)
        self.assertEqual(tokens[4].value, 0xFF)
        
        self.assertEqual(tokens[5].type, TokenType.INTEGER)
        self.assertEqual(tokens[5].value, 0o777)

class TestParser(unittest.TestCase):
    """Test the parser"""
    
    def setUp(self):
        self.lexer = Lexer()
        self.parser = Parser()
    
    def test_function_definition(self):
        """Test function definition parsing"""
        source = """
        int add(int a, int b) {
            return a + b;
        }
        """
        tokens = list(self.lexer.tokenize(source))
        ast = self.parser.parse(tokens)
        
        self.assertEqual(len(ast), 1)
        func_def = ast[0]
        self.assertEqual(func_def.__class__.__name__, 'FunctionDefinition')
        self.assertEqual(func_def.name, 'add')
        self.assertEqual(len(func_def.parameters), 2)
    
    def test_variable_declaration(self):
        """Test variable declaration parsing"""
        source = """
        int main() {
            int x = 42;
            float y = 3.14;
            char c = 'A';
            return 0;
        }
        """
        tokens = list(self.lexer.tokenize(source))
        ast = self.parser.parse(tokens)
        
        self.assertEqual(len(ast), 1)
        func_def = ast[0]
        body = func_def.body
        self.assertEqual(len(body.statements), 4)  # 3 declarations + return
    
    def test_control_flow(self):
        """Test control flow statement parsing"""
        source = """
        int main() {
            int i = 0;
            while (i < 10) {
                if (i % 2 == 0) {
                    i = i + 2;
                } else {
                    i = i + 1;
                }
            }
            return i;
        }
        """
        tokens = list(self.lexer.tokenize(source))
        ast = self.parser.parse(tokens)
        
        self.assertEqual(len(ast), 1)
        func_def = ast[0]
        body = func_def.body
        # Should have declaration, while loop, and return
        self.assertEqual(len(body.statements), 3)

class TestSemanticAnalyzer(unittest.TestCase):
    """Test the semantic analyzer"""
    
    def setUp(self):
        self.lexer = Lexer()
        self.parser = Parser()
        self.analyzer = SemanticAnalyzer()
    
    def test_type_checking(self):
        """Test type checking"""
        source = """
        int main() {
            int x = 42;
            float y = 3.14;
            x = y;  // Should generate warning about implicit conversion
            return 0;
        }
        """
        tokens = list(self.lexer.tokenize(source))
        ast = self.parser.parse(tokens)
        self.analyzer.analyze(ast)
        
        # Should have no errors but may have warnings
        self.assertEqual(len(self.analyzer.errors), 0)
    
    def test_function_call_validation(self):
        """Test function call validation"""
        source = """
        int add(int a, int b) {
            return a + b;
        }
        
        int main() {
            int result = add(5, 3);
            return result;
        }
        """
        tokens = list(self.lexer.tokenize(source))
        ast = self.parser.parse(tokens)
        self.analyzer.analyze(ast)
        
        # Should have no errors
        self.assertEqual(len(self.analyzer.errors), 0)
    
    def test_undefined_variable_error(self):
        """Test undefined variable detection"""
        source = """
        int main() {
            int x = y;  // y is undefined
            return x;
        }
        """
        tokens = list(self.lexer.tokenize(source))
        ast = self.parser.parse(tokens)
        self.analyzer.analyze(ast)
        
        # Should have an error
        self.assertGreater(len(self.analyzer.errors), 0)
    
    def test_function_redefinition_error(self):
        """Test function redefinition detection"""
        source = """
        int add(int a, int b) {
            return a + b;
        }
        
        int add(int x, int y) {  // Redefinition
            return x + y;
        }
        
        int main() {
            return 0;
        }
        """
        tokens = list(self.lexer.tokenize(source))
        ast = self.parser.parse(tokens)
        self.analyzer.analyze(ast)
        
        # Should have an error
        self.assertGreater(len(self.analyzer.errors), 0)

class TestCodeGenerator(unittest.TestCase):
    """Test the code generator"""
    
    def setUp(self):
        self.lexer = Lexer()
        self.parser = Parser()
        self.analyzer = SemanticAnalyzer()
        self.generator = CodeGenerator()
    
    def test_simple_program(self):
        """Test simple program code generation"""
        source = """
        int main() {
            int x = 42;
            return x;
        }
        """
        tokens = list(self.lexer.tokenize(source))
        ast = self.parser.parse(tokens)
        self.analyzer.analyze(ast)
        
        # Should have no errors
        self.assertEqual(len(self.analyzer.errors), 0)
        
        assembly = self.generator.generate(ast)
        
        # Check that assembly contains expected elements
        self.assertIn("_start:", assembly)
        self.assertIn("mov eax, 42", assembly)
        self.assertIn("int 0x80", assembly)
    
    def test_function_call_generation(self):
        """Test function call code generation"""
        source = """
        int add(int a, int b) {
            return a + b;
        }
        
        int main() {
            int result = add(5, 3);
            return result;
        }
        """
        tokens = list(self.lexer.tokenize(source))
        ast = self.parser.parse(tokens)
        self.analyzer.analyze(ast)
        
        self.assertEqual(len(self.analyzer.errors), 0)
        
        assembly = self.generator.generate(ast)
        
        # Check for function definition and call
        self.assertIn("add:", assembly)
        self.assertIn("call add", assembly)
        self.assertIn("push eax", assembly)  # Argument pushing

class TestIntegration(unittest.TestCase):
    """Integration tests for the complete compiler"""
    
    def setUp(self):
        self.lexer = Lexer()
        self.parser = Parser()
        self.analyzer = SemanticAnalyzer()
        self.generator = CodeGenerator()
    
    def compile_program(self, source):
        """Helper method to compile a complete program"""
        tokens = list(self.lexer.tokenize(source))
        ast = self.parser.parse(tokens)
        self.analyzer.analyze(ast)
        
        if self.analyzer.errors:
            return None, self.analyzer.errors
        
        assembly = self.generator.generate(ast)
        return assembly, []
    
    def test_comprehensive_program(self):
        """Test a comprehensive program with multiple features"""
        source = """
        int factorial(int n) {
            if (n <= 1) {
                return 1;
            } else {
                return n * factorial(n - 1);
            }
        }
        
        int main() {
            int num = 5;
            int result = factorial(num);
            printf("Factorial of %d is %d\\n", num, result);
            return 0;
        }
        """
        
        assembly, errors = self.compile_program(source)
        
        # Should compile without errors
        self.assertEqual(len(errors), 0)
        self.assertIsNotNone(assembly)
        
        # Check for key assembly features
        self.assertIn("factorial:", assembly)
        self.assertIn("_start:", assembly)
        self.assertIn("call factorial", assembly)
        self.assertIn("call printf", assembly)
    
    def test_data_types_program(self):
        """Test program with various data types"""
        source = """
        int main() {
            char c = 'X';
            short s = 100;
            int i = 1000;
            long l = 100000;
            float f = 2.5;
            double d = 3.14159;
            
            printf("char: %c, int: %d, float: %f\\n", c, i, f);
            return 0;
        }
        """
        
        assembly, errors = self.compile_program(source)
        
        # Should compile without errors
        self.assertEqual(len(errors), 0)
        self.assertIsNotNone(assembly)
    
    def test_control_flow_program(self):
        """Test program with control flow"""
        source = """
        int main() {
            int sum = 0;
            int i;
            
            for (i = 1; i <= 10; i++) {
                if (i % 2 == 0) {
                    sum += i;
                }
            }
            
            while (sum > 100) {
                sum -= 10;
            }
            
            return sum;
        }
        """
        
        assembly, errors = self.compile_program(source)
        
        # Should compile without errors
        self.assertEqual(len(errors), 0)
        self.assertIsNotNone(assembly)
        
        # Check for control flow labels
        self.assertIn("for_start", assembly)
        self.assertIn("while_start", assembly)

def run_all_tests():
    """Run all test suites"""
    print("=== C-LIKE LANGUAGE COMPILER - COMPREHENSIVE TEST SUITE ===\n")
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestLexer))
    suite.addTests(loader.loadTestsFromTestCase(TestParser))
    suite.addTests(loader.loadTestsFromTestCase(TestSemanticAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestCodeGenerator))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print(f"\n=== TEST SUMMARY ===")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
