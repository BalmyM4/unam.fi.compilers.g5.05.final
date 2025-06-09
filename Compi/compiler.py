import sys
from lexer import tokenize
from parser import parse
from semantic import SemanticAnalyzer
from codegen import CodeGenerator

def compile_file(input_file, output_file):
    try:
        with open(input_file, 'r') as f:
            source_code = f.read()
        
        print("Tokenizing...")
        tokens = tokenize(source_code)
        
        print("Parsing...")
        ast = parse(source_code)
        if not ast:
            print("Parse error")
            return False
        
        print("Semantic analysis...")
        analyzer = SemanticAnalyzer()
        errors = analyzer.analyze(ast)
        if errors:
            for error in errors:
                print(f"Semantic error: {error}")
            return False
        
        print("Code generation...")
        generator = CodeGenerator()
        assembly_code = generator.generate(ast)
        
        with open(output_file, 'w') as f:
            f.write(assembly_code)
        
        print(f"Compilation successful: {output_file}")
        return True
        
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found")
        return False
    except Exception as e:
        print(f"Compilation error: {e}")
        return False

def main():
    if len(sys.argv) != 3:
        print("Usage: python compiler.py <input.c> <output.s>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    if compile_file(input_file, output_file):
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
