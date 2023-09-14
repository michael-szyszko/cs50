#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Prompt for start size
    int population_size;
    do
    {
        population_size = get_int("Start size: ");
    }
    while (population_size < 9);

    // Prompt for end size
    int end_population_size;
    do
    {
        end_population_size = get_int("End size: ");
    }
    while (end_population_size < population_size);

    // Calculate number of years until we reach threshold
    int years = 0;
    while (population_size < end_population_size)
    {
        int births = population_size / 3;
        int deaths = population_size / 4;
        population_size = population_size + births - deaths;
        years++;
    }
    // Print number of years
    printf("Years: %i\n", years);
}
