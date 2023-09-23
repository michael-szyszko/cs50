#include <cs50.h>
#include <stdio.h>

const int MAX_DIGITS = 16;

int main(void)
{
    int digit_count = 0;
    int digits[MAX_DIGITS];

    // Credit card numbers can start with 0,
    // however the assignment suggests to use get_long which would not capture leading zeros
    // therefore case with credit card starting with 0 is being ignored

    long number = get_long("Number: ");
    while(number > 0)
    {
        // stores the number backwards
        digits[digit_count] = (int)(number % 10);
        number = number / 10;
        digit_count += 1;
    }

    int checksum1 = 0;
    int checksum2 = 0;
    for (int i = 0; i < digit_count; i++)
    {
        if (i % 2 == 0)
        {
            checksum1 += digits[i];
        }
        else
        {
            int multiplied = digits[i] * 2;
            checksum2 += (multiplied % 10) + (multiplied / 10);
        }
    }
    printf("checksum 1: %i, checksum2: %i", checksum1, checksum2);

    if ((checksum1 + checksum2) % 10 != 0)
    {
        printf("INVALID\n");
    }
    else if (digit_count == 15 && digits[digit_count] == 3 && (digits[digit_count - 1] == 4 || digits[digit_count - 1] == 7))
    {
        printf("AMEX\n");
    }
    else if (digits[digit_count - 1] == 4 && (digit_count == 13 || digit_count == 16))
    {
        printf("VISA\n");
    }
    else if (digits[digit_count] == 5 && (digits[digit_count - 1] == 1 || digits[digit_count - 1] == 2 || digits[digit_count - 1] == 3 || digits[digit_count - 1] == 4 || digits[digit_count - 1] == 5))
    {
        printf("MASTERCARD\n");
    }
}
//