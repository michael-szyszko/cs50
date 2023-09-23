#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "wav.h"

int check_format(WAVHEADER header);
int get_block_size(WAVHEADER header);

int main(int argc, char *argv[])
{
    // Ensure proper usage
    if (argc != 3)
    {
        printf("Usage: ./reverse infile outfile\n");
        return 1;
    }

    char *infile = argv[1];
    char *outfile = argv[2];

    // Open input file for reading
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        printf("Could not open %s.\n", infile);
        return 1;
    }

    // Read header
    WAVHEADER wh;
    fread(&wh, sizeof(WAVHEADER), 1, inptr);

    // Use check_format to ensure WAV format
    if (!check_format(wh))
    {
        printf("Incorrect file format.\n");
        return 1;
    }

    // Open output file for writing
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        printf("Could not create %s.\n", outfile);
        return 1;
    }

    // Write header to file
    fwrite(&wh, sizeof(WAVHEADER), 1, outptr);

    // Use get_block_size to calculate size of block
    int block_size = get_block_size(wh);

    // Write reversed audio to file
    BYTE block[block_size];
    long start_position = ftell(inptr);

    // For the purposes of transvesing the audio file, the variable blocks will determine how far fseek() will iterate
    int blocks = 1;
    fseek(inptr, -block_size * blocks, SEEK_END);

    // Read the audio file backwards and write blocks of audio data into the new file
    while (ftell(inptr) > start_position - 1)
    {
        blocks++;
        fread(block, sizeof(BYTE) * block_size, 1, inptr);
        fwrite(block, sizeof(BYTE) * block_size, 1, outptr);
        fseek(inptr, -block_size * blocks, SEEK_END);
    }

    fclose(inptr);
    fclose(outptr);
}

int check_format(WAVHEADER header)
{
    char check_word[5] = "WAVE";
    int length = strlen(check_word);

    for (int i = 0; i < length; i++)
    {
        if (check_word[i] != header.format[i])
        {
            return 0;
        }
    }
    return 1;
}

int get_block_size(WAVHEADER header)
{
    // block size is number of channels multiplied by bytes per sample
    return (header.bitsPerSample / 8) * header.numChannels;
}