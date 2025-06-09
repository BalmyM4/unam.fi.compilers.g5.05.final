int main() {
    int x = 10;
    int y = 5;
    int result = 0;
    int i = 0;
    
    if (x > y) {
        result = x + y;
    } else {
        result = x - y;
    }
    
    for (i = 0; i < 5; i = i + 1) {
        result = result + 1;
    }
    
    int a = 3;
    int b = 7;
    
    if (a < b) {
        int j;
        for (j = 0; j < 3; j = j + 1) {
            a = a * 2;
        }
    }
    
    int sum = 0;
    int k;
    for (k = 1; k < 4; k = k + 1) {
        sum = sum + k;
        if (sum > 5) {
            sum = sum - 1;
        }
    }
    
    int final = result + a + sum;
    
    if (final > 30) {
        final = final / 2;
    } else {
        if (final < 20) {
            final = final + 10;
        }
    }
    int m;
    for (m = 0; m < 2; m = m + 1) {
        if (m == 1) {
            final = final + 5;
        }
    }
    
    return final;
}