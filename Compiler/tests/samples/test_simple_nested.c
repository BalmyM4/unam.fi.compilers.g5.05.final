int main() {
    int a;
    int b;
    int result;
    
    a = 20;
    b = 15;
    
    if (a > b) {
        result = a + b;
        if (result > 30) {
            result = result - 10;
        } else {
            result = result + 5;
        }
    } else {
        result = b - a;
    }
    
    return result;
}
