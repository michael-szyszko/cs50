#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int n;
    do
    {
        n = get_int("Height: ");
    } while (n <= 0);

    for (int row = 0; row < n; row++)
    {
        for(int left_side = 0; left_side < n; left_side++)
        {
            if (left_side >= (n - row - 1))
            {
                printf("#");
            }
            else
            {
                printf(" ");
            }
        }
        printf("  ");
        for (int right_side = 0; right_side <= row; right_side++){
            printf("#");
        }
        printf("\n");
    }
}