
int main() {
    int score;
    int bonus;
    int final_score;
    
    score = 85;
    bonus = 10;
    
    if (score >= 90) {
        final_score = score + bonus;
        if (final_score > 100) {
            final_score = 100;
        }
    } else {
        if (score >= 70) {
            final_score = score + bonus / 2;
        } else {
            final_score = score;
        }
    }
    
    return final_score;
}
