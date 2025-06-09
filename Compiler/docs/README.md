# C-like Language Compiler Documentation

This document provides detailed technical information about the C-like language compiler implementation.

## Architecture Overview

The compiler follows a traditional four-phase architecture:

### Compilation Phases

1. **Lexical Analysis** (Tokenization)
   - Converts source code into tokens
   - Recognizes keywords, identifiers, operators, literals
   - Handles whitespace and comments

2. **Syntax Analysis** (Parsing)
   - Builds Abstract Syntax Tree (AST) from tokens
   - Enforces language grammar rules
   - Detects syntax errors

3. **Semantic Analysis**
   - Performs type checking
   - Variable scope validation
   - Function signature verification

4. **Code Generation**
   - Generates x86 assembly code
   - Optimizes output for target architecture
   - Handles memory management and register allocation

## Language Features

### Supported Data Types
- `int` - Integer values
- `float` - Floating-point numbers  
- `char` - Character values
- `void` - Function return type for no value

### Control Flow Constructs
- `if-else` statements with conditional logic
- `while` loops for iteration
- `for` loops with initialization, condition, and increment
- Nested control structures supported

### Function Support
- Function declarations with parameters
- Function calls with argument passing
- Return statements and values
- Built-in functions (printf, scanf)

### Operators
- **Arithmetic**: `+`, `-`, `*`, `/`, `%`
- **Comparison**: `==`, `!=`, `<`, `<=`, `>`, `>=`
- **Logical**: `&&`, `||`, `!`
- **Assignment**: `=`, `+=`, `-=`, `*=`, `/=`

## Implementation Details

### Module Structure
```
src/
├── lexer/
│   ├── lexer.py           # Tokenizer implementation
│   └── tokens.py          # Token definitions
├── parser/
│   ├── parser.py          # Parser implementation
│   └── ast_nodes.py       # AST node classes
├── semantic/
│   └── analyzer.py        # Semantic analysis
└── codegen/
    └── generator.py       # Code generation
```

### Error Handling
- Lexical errors (invalid characters, malformed tokens)
- Syntax errors (grammar violations, unexpected tokens)
- Semantic errors (type mismatches, undefined variables)
- Runtime error prevention (division by zero, null pointers)

## Usage

### Command Line
```bash
python compiler.py <input_file.c> [output_file.asm]
```

### Example
```bash
python compiler.py test1.c output.asm
```

### Demo
```bash
python demo.py
```

## Test Cases

### Test 1: Simple if-else
```c
int main() {
    int x;
    int y;
    x = 10;
    y = 5;
    if (x > y) {
        x = x + 1;
    } else {
        x = x - 1;
    }
    return x;
}
```

### Test 2: Nested if statements
```c
int main() {
    int a;
    int b;
    int c;
    a = 15;
    b = 10;
    c = 20;
    if (a > b) {
        if (a > c) {
            a = a * 2;
        } else {
            a = c;
        }
    } else {
        a = b;
    }
    return a;
}
```

### Test 3: Complex expressions with logical operators
```c
int main() {
    int x;
    int y;
    int result;
    x = 8;
    y = 3;
    if (x > 5 && y < 10) {
        result = x + y * 2;
        if (result > 10) {
            result = result - 5;
        }
    } else {
        result = 0;
    }
    return result;
}
```

### Test 4: Error detection (undefined variable)
```c
int main() {
    int x;
    x = 10;
    if (x > undefined_var) {  // This will cause a semantic error
        x = x + 1;
    }
    return x;
}
```

## Dependencies

- Python 3.6+
- PLY (Python Lex-Yacc) library

### Installation
```bash
pip install ply
```

## Grammar

The compiler supports a subset of C grammar:

```
program : statement_list

statement : function_def
         | var_decl SEMICOLON
         | assignment SEMICOLON
         | if_stmt
         | while_stmt
         | return_stmt SEMICOLON
         | expression_stmt SEMICOLON
         | block

if_stmt : IF LPAREN expression RPAREN statement
        | IF LPAREN expression RPAREN statement ELSE statement

expression : expression PLUS expression
          | expression MINUS expression
          | expression TIMES expression
          | expression DIVIDE expression
          | expression EQ expression
          | expression NE expression
          | expression LT expression
          | expression GT expression
          | expression AND expression
          | expression OR expression
          | IDENTIFIER
          | NUMBER
```

## Output

The compiler generates x86 assembly code that can be assembled and linked using standard tools. The output includes:

- Data section with string constants
- Text section with generated code
- Proper function prologue/epilogue
- Conditional jumps for if-else statements
- Arithmetic and logical operations

## Error Handling

The compiler provides comprehensive error reporting:

- **Lexical errors**: Illegal characters
- **Syntax errors**: Invalid grammar constructs
- **Semantic errors**: Undefined variables, type mismatches
- **Line number tracking**: All errors include line numbers for easy debugging

## Example Output

For a simple if-else statement, the compiler generates assembly code like:

```assembly
# Generated Assembly Code
.section .data
newline: .asciz "\n"
printf_int: .asciz "%d\n"

.section .text
.global _start

_start:
    pushl %ebp
    movl %esp, %ebp
    subl $64, %esp
    
    movl $10, %eax
    # Assignment to x
    movl $5, %eax
    # Assignment to y
    
    # If statement condition
    movl -31(%ebp), %eax
    pushl %eax
    movl -51(%ebp), %eax
    movl %eax, %ebx
    popl %eax
    cmpl %ebx, %eax
    setg %al
    movzbl %al, %eax
    
    cmpl $0, %eax
    je L0
    # Then branch
    # ... code ...
    jmp L1
L0:
    # Else branch
    # ... code ...
L1:
    # End of if statement
```
