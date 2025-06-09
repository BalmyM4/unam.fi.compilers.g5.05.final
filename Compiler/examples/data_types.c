/*
 * Data Types Demo
 * Demonstrates all supported C data types
 */

int main() {
    // Integer types
    char c = 'A';
    signed char sc = -50;
    unsigned char uc = 200;
    
    short s = -1000;
    signed short ss = -2000;
    unsigned short us = 3000;
    
    int i = -50000;
    signed int si = -60000;
    unsigned int ui = 70000;
    
    long l = -1000000;
    signed long sl = -2000000;
    unsigned long ul = 3000000;
    
    // Floating point types
    float f = 3.14159;
    double d = 2.71828;
    long double ld = 1.41421;
    
    // Display values
    printf("=== C Data Types Demo ===\n");
    
    printf("Character types:\n");
    printf("  char c = '%c' (ASCII: %d)\n", c, c);
    printf("  signed char = %d\n", sc);
    printf("  unsigned char = %u\n", uc);
    
    printf("Short integer types:\n");
    printf("  short = %d\n", s);
    printf("  signed short = %d\n", ss);
    printf("  unsigned short = %u\n", us);
    
    printf("Integer types:\n");
    printf("  int = %d\n", i);
    printf("  signed int = %d\n", si);
    printf("  unsigned int = %u\n", ui);
    
    printf("Long integer types:\n");
    printf("  long = %ld\n", l);
    printf("  signed long = %ld\n", sl);
    printf("  unsigned long = %lu\n", ul);
    
    printf("Floating point types:\n");
    printf("  float = %.5f\n", f);
    printf("  double = %.5f\n", d);
    printf("  long double = %.5Lf\n", ld);
    
    return 0;
}
