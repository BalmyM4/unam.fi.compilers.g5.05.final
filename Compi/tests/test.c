int main() {
    int x = 5;
    if (x > 3) {
        x = x + 1;
    } else {
        x = x - 1;
    }
    int i;
    int sum = 0;
    for (i = 1; i < 10; i = i + 1) {
        sum = sum + i;
    }
    return sum;
}
