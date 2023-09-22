#include "helpers.h"
#include <math.h>



void swap(RGBTRIPLE *p1, RGBTRIPLE *p2);
RGBTRIPLE get_blurred_pixel(int height, int width, int row, int col, RGBTRIPLE image[height][width]);
RGBTRIPLE get_edged_pixel(int height, int width, int row, int col, RGBTRIPLE image[height][width]);
int get_GxGyCalculation(int gx, int gy);

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int r = 0; r < height; r++)
    {
        for (int c = 0; c < width; c++)
        {
            int average = round((image[r][c].rgbtBlue + image[r][c].rgbtGreen + image[r][c].rgbtRed) / 3.0);
            image[r][c].rgbtBlue = average;
            image[r][c].rgbtGreen = average;
            image[r][c].rgbtRed = average;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int r = 0; r < height; r++)
    {
        for (int c = 0; c < width / 2; c++)
        {
            RGBTRIPLE temp = image[r][c];
            image[r][c] = image[r][width - c - 1];
            image[r][width - c - 1] = temp;
        }
    }
    return;
}

void swap(RGBTRIPLE *p1, RGBTRIPLE *p2)
{
    RGBTRIPLE temp = *p1;
    *p1 = *p2;
    *p2 = temp;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE blurred_image[height][width];
    for (int r = 0; r < height; r++)
    {
        for (int c = 0; c < width; c++)
        {
            RGBTRIPLE blurred_pixel = get_blurred_pixel(height, width, r, c, image);
            blurred_image[r][c] = blurred_pixel;
        }
    }

    for (int r = 0; r < height; r++)
    {
        for (int c = 0; c < width; c++)
        {
            image[r][c] = blurred_image[r][c];
        }
    }
    return;
}

RGBTRIPLE get_blurred_pixel(int height, int width, int row, int col, RGBTRIPLE image[height][width])
{
    int elements = 0;
    double summed_blue = 0;
    double summed_green = 0;
    double summed_red = 0;

    for (int r = row - 1; r < row + 2; r++)
    {
        if (r >= 0 && r < height)
        {
            for (int c = col - 1; c < col + 2; c++)
            {
                if (c >= 0 && c < width)
                {
                    elements += 1;
                    summed_blue += image[r][c].rgbtBlue;
                    summed_green += image[r][c].rgbtGreen;
                    summed_red += image[r][c].rgbtRed;
                }
            }
        }
    }
    return (RGBTRIPLE) {.rgbtBlue = round(summed_blue / elements), .rgbtGreen = round(summed_green / elements), .rgbtRed = round(summed_red / elements) };
}

RGBTRIPLE get_edged_pixel(int height, int width, int row, int col, RGBTRIPLE image[height][width])
{


    int GxBlue = 0;
    int GxGreen = 0;
    int GxRed = 0;
    int GyBlue = 0;
    int GyGreen = 0;
    int GyRed = 0;
    int GxMultiplier[3][3];
    GxMultiplier[0][0] = -1;
    GxMultiplier[0][1] = 0;
    GxMultiplier[0][2] = 1;
    GxMultiplier[1][0] = -2;
    GxMultiplier[1][1] = 0;
    GxMultiplier[1][2] = 2;
    GxMultiplier[2][0] = -1;
    GxMultiplier[2][1] = 0;
    GxMultiplier[2][2] = 1;

    int GyMultiplier[3][3];
    GyMultiplier[0][0] = -1;
    GyMultiplier[0][1] = -2;
    GyMultiplier[0][2] = -1;
    GyMultiplier[1][0] = 0;
    GyMultiplier[1][1] = 0;
    GyMultiplier[1][2] = 0;
    GyMultiplier[2][0] = 1;
    GyMultiplier[2][1] = 2;
    GyMultiplier[2][2] = 1;

    for (int r = row - 1; r < row + 2; r++)
    {
        if (r >= 0 && r < height)
        {
            for (int c = col - 1; c < col + 2; c++)
            {
                if (c >= 0 && c < width)
                {
                    GxBlue += GxMultiplier[r - row + 1][c - col + 1] * image[r][c].rgbtBlue;
                    GxGreen += GxMultiplier[r - row + 1][c - col + 1] * image[r][c].rgbtGreen;
                    GxRed += GxMultiplier[r - row + 1][c - col + 1] * image[r][c].rgbtRed;
                    GyBlue += GyMultiplier[r - row + 1][c - col + 1] * image[r][c].rgbtBlue;
                    GyGreen += GyMultiplier[r - row + 1][c - col + 1] * image[r][c].rgbtGreen;
                    GyRed += GyMultiplier[r - row + 1][c - col + 1] * image[r][c].rgbtRed;
                }
            }
        }
    }
    int GxGyBlue = get_GxGyCalculation(GxBlue, GyBlue);
    int GxGyGreen = get_GxGyCalculation(GxGreen, GyGreen);
    int GxGyRed = get_GxGyCalculation(GxRed, GyRed);

    return (RGBTRIPLE) {.rgbtBlue = GxGyBlue, .rgbtGreen = GxGyGreen, .rgbtRed = GxGyRed };
}

int get_GxGyCalculation(int gx, int gy)
{
    double GxGy = round(sqrt((gx * gx) + (gy * gy)));
    if (GxGy > 255)
    {
        GxGy = 255;
    }
    return (int) GxGy;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE edged_image[height][width];
    for (int r = 0; r < height; r++)
    {
        for (int c = 0; c < width; c++)
        {
            RGBTRIPLE edged_pixel = get_edged_pixel(height, width, r, c, image);
            edged_image[r][c] = edged_pixel;
        }
    }

    for (int r = 0; r < height; r++)
    {
        for (int c = 0; c < width; c++)
        {
            image[r][c] = edged_image[r][c];
        }
    }

    return;
}
