#!/usr/bin/env python3

"""
Comprehensive Test Suite for C-like Language Compiler
=====================================================

This script runs all test cases and validates the compiler functionality.
"""

import os
import sys
from compiler import Compiler

def run_test_suite():
    """Run comprehensive test suite for the compiler"""
    print("C-like Language Compiler Test Suite")
    print("=" * 50)
    print()
    
    compiler = Compiler()
    test_results = []
    
    # Define test cases
    tests = [
        {
            "name": "Simple Variable Assignment",
            "code": """
int main() {
    int x;
    x = 42;
    return x;
}""",
            "should_pass": True,
            "description": "Basic variable declaration and assignment"
        },
        {
            "name": "Simple If-Else Statement",
            "code": """
int main() {
    int x;
    x = 10;
    if (x > 5) {
        x = 20;
    } else {
        x = 0;
    }
    return x;
}""",
            "should_pass": True,
            "description": "Basic conditional statement"
        },
        {
            "name": "Undefined Variable Error",
            "code": """
int main() {
    int x;
    x = undefined_variable;
    return x;
}""",
            "should_pass": False,
            "description": "Should catch undefined variable error"
        }
    ]
    
    # Run each test
    for i, test in enumerate(tests, 1):
        print(f"Test {i}: {test['name']}")
        print("-" * (len(test['name']) + 8))
        print(f"Description: {test['description']}")
        print()
        
        try:
            # Create temporary test file
            test_file = f"temp_test_{i}.c"
            with open(test_file, 'w') as f:
                f.write(test['code'])
            
            # Run compiler
            output_file = f"temp_test_{i}.asm"
            success = compiler.compile(test['code'], output_file)
            
            # Check result
            if success == test['should_pass']:
                if success:
                    print("PASS - Compilation successful as expected")
                else:
                    print("PASS - Compilation failed as expected (caught error)")
                test_results.append(("PASS", test['name']))
            else:
                if success:
                    print("FAIL - Expected compilation to fail but it succeeded")
                else:
                    print("FAIL - Expected compilation to succeed but it failed")
                test_results.append(("FAIL", test['name']))
            
            # Clean up temporary files
            try:
                os.remove(test_file)
                if os.path.exists(output_file):
                    os.remove(output_file)
            except:
                pass
                
        except Exception as e:
            print(f"ERROR - Test execution failed: {e}")
            test_results.append(("ERROR", test['name']))
        
        print()
        print("=" * 50)
        print()
    
    # Summary
    print("Test Results Summary")
    print("=" * 25)
    
    passed = sum(1 for result, _ in test_results if result == "PASS")
    failed = sum(1 for result, _ in test_results if result == "FAIL")
    errors = sum(1 for result, _ in test_results if result == "ERROR")
    total = len(test_results)
    
    print(f"Total Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Errors: {errors}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    print()
    
    if failed > 0 or errors > 0:
        print("Failed/Error Tests:")
        for result, name in test_results:
            if result != "PASS":
                print(f"  {result}: {name}")
    
    return passed == total

def validate_components():
    """Validate individual compiler components"""
    print("Component Validation")
    print("=" * 25)
    
    components = [
        ("Lexer", "lexer.py"),
        ("Parser", "parser.py"), 
        ("Semantic Analyzer", "semantic_analyzer.py"),
        ("Code Generator", "code_generator.py"),
        ("Keywords", "keywords.py")
    ]
    
    all_valid = True
    
    for name, filename in components:
        try:
            if os.path.exists(filename):
                # Try to import the module
                module_name = filename[:-3]  # Remove .py extension
                __import__(module_name)
                print(f"OK - {name} ({filename})")
            else:
                print(f"MISSING - {name} ({filename})")
                all_valid = False
        except Exception as e:
            print(f"ERROR - {name} ({filename}): {e}")
            all_valid = False
    
    print()
    return all_valid

def main():
    """Main function to run the test suite"""
    print("Starting Compiler Validation...")
    print()
    
    # Validate components first
    components_ok = validate_components()
    
    if components_ok:
        # Run test suite
        tests_passed = run_test_suite()
        
        if tests_passed:
            print("All tests passed! Compiler is working correctly.")
            return True
        else:
            print("Some tests failed. Please check the implementation.")
            return False
    else:
        print("Component validation failed. Please check file integrity.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
