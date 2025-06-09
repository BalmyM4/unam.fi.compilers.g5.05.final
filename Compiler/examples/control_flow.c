/*
 * Control Flow Demo
 * Demonstrates if-else, while, for, and do-while loops
 */

int factorial(int n) {
    if (n <= 1) {
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}

int fibonacci(int n) {
    if (n <= 1) {
        return n;
    }
    
    int a = 0, b = 1, temp;
    int i;
    
    for (i = 2; i <= n; i++) {
        temp = a + b;
        a = b;
        b = temp;
    }
    
    return b;
}

int main() {
    printf("=== Control Flow Demonstration ===\n\n");
    
    // If-else demonstration
    int num = 15;
    printf("Testing if-else with num = %d:\n", num);
    
    if (num > 10) {
        printf("  %d is greater than 10\n", num);
    } else if (num > 5) {
        printf("  %d is between 6 and 10\n", num);
    } else {
        printf("  %d is 5 or less\n", num);
    }
    
    // While loop demonstration  
    printf("\nWhile loop - counting down from 5:\n");
    int countdown = 5;
    while (countdown > 0) {
        printf("  %d...\n", countdown);
        countdown--;
    }
    printf("  Blast off!\n");
    
    // For loop demonstration
    printf("\nFor loop - even numbers 2 to 10:\n");
    int i;
    for (i = 2; i <= 10; i += 2) {
        printf("  %d\n", i);
    }
    
    // Do-while demonstration
    printf("\nDo-while loop - at least one iteration:\n");
    int x = 0;
    do {
        printf("  x = %d\n", x);
        x++;
    } while (x < 3);
    
    // Function calls with recursion
    printf("\nFactorial of 6: %d\n", factorial(6));
    printf("Fibonacci of 8: %d\n", fibonacci(8));
    
    // Nested loops
    printf("\nMultiplication table (3x3):\n");
    int row, col;
    for (row = 1; row <= 3; row++) {
        for (col = 1; col <= 3; col++) {
            printf("%4d", row * col);
        }
        printf("\n");
    }
    
    return 0;
}
