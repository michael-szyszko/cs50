#include <cs50.h>
#include <stdio.h>

void print_left_pyramid(int row, int height);
void print_right_pyramid(int row);

int main(void)
{
    int n;
    do
    {
        n = get_int("Height: ");
    }
    while (n <= 0);

    for (int row = 0; row < n; row++)
    {
        print_left_pyramid(row, n);
        printf("  ");
        print_right_pyramid(row);
        printf("\n");
    }
}

void print_left_pyramid(int row, int height)
{
    for (int i = 0; i < height; i++)
    {
        if (i >= (height - row - 1))
        {
            printf("#");
        }
        else
        {
            printf(" ");
        }
    }
}

void print_right_pyramid(int row)
{
    for (int i = 0; i <= row; i++)
    {
        printf("#");
    }
}

/*
int main(void)
{
    int n;
    do
    {
        n = get_int("Height: ");
    }
    while (n <= 0);

    for (int row = 0; row < n; row++)
    {
        for (int left_side = 0; left_side < n; left_side++)
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
        for (int right_side = 0; right_side <= row; right_side++)
        {
            printf("#");
        }
        printf("\n");
    }
}*/