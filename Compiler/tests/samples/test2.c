// Test Case 2: Nested if statements
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
