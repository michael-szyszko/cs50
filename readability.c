#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int const MAX_GRADE = 16;

int main(void)
{
    string text = get_string("Text: ");

    int length = strlen(text);

    int letters = 0;
    int words = 1;
    int sentences = 0;

    for (int i = 0; i < length; i++)
    {
        if (toupper(text[i]) >= 'A' && toupper(text[i]) <= 'a')
        {
            letters++;
        }
        else if (text[i] == ' ')
        {
            words++;
        }
        else if (text[i] == '!' || text[i] == '.' || text[i] == '?')
        {
            sentences++;
        }
    }

    double avg_num_letters_per_100_words = (double) letters / words * 100.0;
    double avg_num_sentences_per_100_words = (double) sentences / words * 100.0;

    int grade = round((0.0588 * avg_num_letters_per_100_words) - (0.296 * avg_num_sentences_per_100_words) - 15.8);
    if (grade > 1 && grade < 16)
    {
        printf("Grade %i\n", grade);
    }
    else if (grade >= MAX_GRADE)
    {
        printf("Grade %i+\n", MAX_GRADE);
    }
    else
    {
        printf("Before Grade 1\n");
    }
}