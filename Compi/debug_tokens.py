from lexer import tokenize

code = """int main() {
    int result = 42;
    return result;
}"""

tokens = tokenize(code)
for token in tokens:
    print(f"{token.type}: {token.value}")
