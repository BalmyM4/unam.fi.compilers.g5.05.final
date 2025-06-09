/*
 * Interactive Program
 * Demonstrates user input with scanf and interactive features
 */

int get_grade_letter(int score) {
    if (score >= 90) {
        return 'A';
    } else if (score >= 80) {
        return 'B';
    } else if (score >= 70) {
        return 'C';
    } else if (score >= 60) {
        return 'D';
    } else {
        return 'F';
    }
}

void print_menu() {
    printf("\n=== Interactive Calculator ===\n");
    printf("1. Add two numbers\n");
    printf("2. Calculate factorial\n");
    printf("3. Grade calculator\n");
    printf("4. Exit\n");
    printf("Enter your choice (1-4): ");
}

int main() {
    int choice;
    int num1, num2, result;
    int score;
    char grade;
    
    printf("Welcome to the Interactive C Program!\n");
    
    do {
        print_menu();
        scanf("%d", &choice);
        
        switch (choice) {
            case 1:
                printf("Enter two integers: ");
                scanf("%d %d", &num1, &num2);
                result = num1 + num2;
                printf("Result: %d + %d = %d\n", num1, num2, result);
                break;
                
            case 2:
                printf("Enter a number for factorial: ");
                scanf("%d", &num1);
                if (num1 < 0) {
                    printf("Factorial is not defined for negative numbers.\n");
                } else {
                    result = 1;
                    int i;
                    for (i = 1; i <= num1; i++) {
                        result *= i;
                    }
                    printf("Factorial of %d is %d\n", num1, result);
                }
                break;
                
            case 3:
                printf("Enter student score (0-100): ");
                scanf("%d", &score);
                if (score < 0 || score > 100) {
                    printf("Invalid score! Please enter 0-100.\n");
                } else {
                    grade = get_grade_letter(score);
                    printf("Score: %d, Grade: %c\n", score, grade);
                }
                break;
                
            case 4:
                printf("Thank you for using the calculator!\n");
                break;
                
            default:
                printf("Invalid choice! Please enter 1-4.\n");
                break;
        }
        
    } while (choice != 4);
    
    return 0;
}
