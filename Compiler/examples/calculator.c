/*
 * Calculator Program
 * Demonstrates function definitions, parameters, and arithmetic operations
 */

int add(int a, int b) {
    return a + b;
}

int subtract(int a, int b) {
    return a - b;
}

int multiply(int a, int b) {
    return a * b;
}

int divide(int a, int b) {
    if (b != 0) {
        return a / b;
    } else {
        return 0;
    }
}

int main() {
    int x = 20;
    int y = 5;
    
    printf("Calculator Demo\n");
    printf("x = %d, y = %d\n", x, y);
    printf("x + y = %d\n", add(x, y));
    printf("x - y = %d\n", subtract(x, y));
    printf("x * y = %d\n", multiply(x, y));
    printf("x / y = %d\n", divide(x, y));
    
    return 0;
}
