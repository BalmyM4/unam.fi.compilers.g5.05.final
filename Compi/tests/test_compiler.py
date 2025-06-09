import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lexer import tokenize
from parser import parse
from semantic import SemanticAnalyzer
from codegen import CodeGenerator

class TestCompiler(unittest.TestCase):
    
    def test_lexer(self):
        code = "int x = 5;"
        tokens = tokenize(code)
        self.assertEqual(tokens[0].type, 'INT')
        self.assertEqual(tokens[1].type, 'IDENTIFIER')
        self.assertEqual(tokens[2].type, 'ASSIGN')
        self.assertEqual(tokens[3].type, 'NUMBER')
        self.assertEqual(tokens[4].type, 'SEMICOLON')
    
    def test_parser_if(self):
        code = """
        int main() {
            int x = 5;
            if (x > 3) {
                x = x + 1;
            }
            return x;
        }
        """
        ast = parse(code)
        self.assertIsNotNone(ast)
    
    def test_parser_for(self):
        code = """
        int main() {
            int i;
            for (i = 0; i < 10; i = i + 1) {
                i = i + 1;
            }
            return i;
        }
        """
        ast = parse(code)
        self.assertIsNotNone(ast)
    
    def test_semantic_analysis(self):
        code = """
        int main() {
            int x = 5;
            return x;
        }
        """
        ast = parse(code)
        analyzer = SemanticAnalyzer()
        errors = analyzer.analyze(ast)
        self.assertEqual(len(errors), 0)
    
    def test_code_generation(self):
        code = """
        int main() {
            int x = 5;
            return x;
        }
        """
        ast = parse(code)
        generator = CodeGenerator()
        assembly = generator.generate(ast)
        self.assertIn(".section .text", assembly)

if __name__ == '__main__':
    unittest.main()
