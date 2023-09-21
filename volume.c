// Modifies the volume of an audio file

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// Number of bytes in .wav header
const int HEADER_SIZE = 44;

int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc != 4)
    {
        printf("Usage: ./volume input.wav output.wav factor\n");
        return 1;
    }

    // Open files and determine scaling factor
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    FILE *output = fopen(argv[2], "w");
    if (output == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    float factor = atof(argv[3]);

    // TODO: Copy header (44 bytes) from input file to output file
    uint8_t header[HEADER_SIZE];
    if (fread(header, 1, HEADER_SIZE, input))
    {
        fwrite(header, 1, HEADER_SIZE, output);
    }
    else
    {
        printf("failed to read from file\n");
        // Close files
        fclose(input);
        fclose(output);
        return 1;
    }

    int16_t data;

    while (fread(&data, sizeof(int16_t), 1, input))
    {
        data *= factor;
        fwrite(&data, 2, 1, output);
    }
    // TODO: Read samples from input file and write updated data to output file

    // Close files
    fclose(input);
    fclose(output);
}
