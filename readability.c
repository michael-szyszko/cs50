#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>


int main(void)
{
    //Need to calculate the number of letters, words(any space, wont start or end, so we can just space +1), and sentences (., !, ?)
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
        else if(text[i] == ' ')
        {
            words++;
        }
        else if (text[i] == '!' || text[i] == '.' || text[i] == '?')
        {
            sentences++;
        }
    }

    printf("%i letters\n%i words\n%i sentences\n", letters, words, sentences);

    double avg_num_letters_per_100_words = letters / words * 100.0;
    double avg_num_sentences_per_100_words = sentences / words * 100;
    int grade = 0.0588 * avg_num_letters_per_100_words - 0.296 * avg_num_sentences_per_100_words - 15.8;
    printf("Grade %i\n", grade);
}