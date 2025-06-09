// Comprehensive test case - complex if-else with multiple operations
int main() {
    int a;
    int b;
    int c;
    int result;
    
    a = 20;
    b = 15;
    c = 10;
    
    if (a > b) {
        if (b > c) {
            result = a + b * c;
            if (result > 100) {
                result = result - 50;
            } else {
                result = result + 25;
            }
        } else {
            result = a - b;
        }
    } else {
        if (a == b) {
            result = a * 2;
        } else {
            result = b / 2;
        }
    }
    
    return result;
}
