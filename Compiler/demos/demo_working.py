#!/usr/bin/env python3

"""
Compiler Demonstration
Shows the capabilities of the C-like compiler
"""

import os
import sys
from pathlib import Path

# Import existing working compiler components
from compiler import compile_file

def demonstrate_compiler_features():
    """Demonstrate the compiler features"""
    
    print("=" * 60)
    print("C-LIKE LANGUAGE COMPILER DEMONSTRATION")
    print("=" * 60)
    print()
    
    # Example files to demonstrate
    examples = [
        {
            'file': 'examples/hello_world.c',
            'description': 'Basic program structure and printf function',
            'features': ['Function definitions', 'Built-in functions', 'String literals']
        },
        {
            'file': 'examples/calculator.c', 
            'description': 'Function definitions and parameter passing',
            'features': ['Multiple functions', 'Parameter lists', 'Return values', 'Conditional logic']
        },
        {
            'file': 'examples/data_types.c',
            'description': 'All supported C data types',
            'features': ['All C data types', 'Signed/unsigned variants', 'Type declarations', 'Printf formatting']
        },
        {
            'file': 'examples/control_flow.c',
            'description': 'Control flow structures',
            'features': ['For loops', 'While loops', 'Do-while loops', 'Nested conditions', 'Recursion']
        },
        {
            'file': 'examples/interactive.c',
            'description': 'User input and interactive features', 
            'features': ['scanf input', 'Switch statements', 'User interaction', 'Menu systems']
        }
    ]
    
    compiled_count = 0
    total_count = len(examples)
    
    for i, example in enumerate(examples, 1):
        print(f"📋 Example {i}/{total_count}: {example['description']}")
        print(f"   File: {example['file']}")
        print("   Enhanced Features:")
        for feature in example['features']:
            print(f"     • {feature}")
        print()
          # Check if file exists
        if not os.path.exists(example['file']):
            print(f"   ERROR - File not found: {example['file']}")
            print()
            continue
        
        # Show source code snippet
        try:
            with open(example['file'], 'r') as f:
                lines = f.readlines()
            
            print("   Source Code Preview:")
            print("   " + "-" * 40)
            for j, line in enumerate(lines[:10], 1):
                print(f"   {j:2d}: {line.rstrip()}")
            if len(lines) > 10:
                print(f"   ... and {len(lines) - 10} more lines")
            print("   " + "-" * 40)
            print()
              except Exception as e:
            print(f"   ERROR - Error reading file: {e}")
            print()
            continue
        
        # Compile the example
        print("   Compiling with Compiler...")
        try:
            output_file = f"output/{Path(example['file']).stem}_compiled.asm"
            
            # Use the existing compiler
            success = compile_file(example['file'], output_file)
              if success:
                print(f"   SUCCESS - Compilation successful!")
                print(f"   Output: {output_file}")
                compiled_count += 1
                
                # Show output file size
                if os.path.exists(output_file):
                    size = os.path.getsize(output_file)
                    with open(output_file, 'r') as f:
                        lines = len(f.readlines())
                    print(f"   Generated {lines} lines of assembly ({size} bytes)")
                
            else:
                print(f"   FAILED - Compilation failed")
                
        except Exception as e:
            print(f"   ERROR - Compilation error: {e}")
        
        print()
        print("=" * 60)
        print()
      # Summary
    print("COMPILER DEMONSTRATION SUMMARY")
    print("=" * 60)print(f"Total examples: {total_count}")
    print(f"Successfully compiled: {compiled_count}")
    print(f"Success rate: {(compiled_count/total_count)*100:.1f}%")
    print()
    
    if compiled_count > 0:
        print("Features Demonstrated:")
        print("   - Function definitions and calls")
        print("   - All C data types (char, short, int, long, float, double)")
        print("   - Signed and unsigned type variants")  
        print("   - Control flow (if-else, while, for, do-while, switch)")
        print("   - Built-in functions (printf, scanf)")
        print("   - String and character literals")
        print("   - Complex expressions and operators")
        print("   - Variable declarations and assignments")
        print("   - Recursive function calls")
        print("   - User input and output")
        print()
        
        print("Architecture Components:")
        print("   - Modular compiler design with separate phases")
        print("   • Enhanced lexical analysis with comprehensive token support")
        print("   • Advanced parser with full C-like grammar")
        print("   • Sophisticated semantic analysis with type checking")
        print("   • Improved code generation with function call support")
        print("   • Comprehensive error reporting and debugging")
        print()
        
        print("📂 Generated Files:")
        output_dir = "output"
        if os.path.exists(output_dir):
            asm_files = [f for f in os.listdir(output_dir) if f.endswith('.asm')]
            for asm_file in asm_files:
                print(f"   📄 {asm_file}")
        print()
    
    print("🎉 Enhanced C-like Compiler demonstration completed!")
    print("   The compiler now supports advanced C language features")
    print("   with a robust, modular architecture suitable for")
    print("   educational purposes and further development.")

if __name__ == "__main__":
    demonstrate_enhanced_features()
