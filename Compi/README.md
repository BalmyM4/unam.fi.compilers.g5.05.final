# Simple C Compiler

A basic C compiler that supports a subset of C grammar including if statements and for loops.

## Features

- **Lexical Analysis**: Tokenizes C source code
- **Parsing**: LR(1) parser with 1 lookahead token
- **Semantic Analysis**: Symbol table and type checking
- **Code Generation**: Generates x86 assembly code

## Supported Grammar

```
program : statement_list

statement : function_def
         | var_decl SEMICOLON
         | assignment SEMICOLON
         | if_stmt
         | for_stmt
         | return_stmt SEMICOLON
         | expression_stmt SEMICOLON
         | block

if_stmt : IF LPAREN expression RPAREN statement
        | IF LPAREN expression RPAREN statement ELSE statement

for_stmt : FOR LPAREN assignment SEMICOLON expression SEMICOLON assignment RPAREN statement

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

## Usage

```bash
python compiler.py input.c output.s
```

## Example

Compile an if statement:
```c
int main() {
    int x = 5;
    if (x > 3) {
        x = x + 1;
    }
    return x;
}
```

Compile a for loop:
```c
int main() {
    int i;
    int sum = 0;
    for (i = 1; i < 10; i = i + 1) {
        sum = sum + i;
    }
    return sum;
}
```

## Testing

```bash
python compiler.py if_test.c if_test.s
python compiler.py for_test.c for_test.s
python compiler.py test.c test.s
python compiler.py extra_test.c extra_test.s
```

## Requirements

- Python 3.x
- PLY (Python Lex-Yacc)

Install dependencies:
```bash
pip install ply
```

## Files

- `compiler.py` - Main compiler entry point
- `lexer.py` - Lexical analyzer
- `parser.py` - Syntax analyzer and AST nodes
- `semantic.py` - Semantic analyzer
- `codegen.py` - Assembly code generator
- `keywords.py` - C keywords definitions
- `tests/` - Test files and examples
