// Test Case 3: If with arithmetic and logical operations
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
