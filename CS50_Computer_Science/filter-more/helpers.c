#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Calculate average of red, green, and blue
            int average = round((image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / 3.0);

            // Assign average value to red, green, and blue components
            image[i][j].rgbtRed = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtBlue = average;
        }
    }
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            // Swap the pixels
            RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][width - j - 1];
            image[i][width - j - 1] = temp;
        }
    }
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // Create a copy of the image to store the original values
    RGBTRIPLE temp[height][width];

    // Copy the original image to temp
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            temp[i][j] = image[i][j];
        }
    }

    // Loop over each pixel
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int red = 0;
            int green = 0;
            int blue = 0;
            int count = 0;

            // Loop over the neighboring pixels
            for (int di = -1; di <= 1; di++)
            {
                for (int dj = -1; dj <= 1; dj++)
                {
                    int ni = i + di;
                    int nj = j + dj;

                    // Check if the neighboring pixel is within the bounds of the image
                    if (ni >= 0 && ni < height && nj >= 0 && nj < width)
                    {
                        red += temp[ni][nj].rgbtRed;
                        green += temp[ni][nj].rgbtGreen;
                        blue += temp[ni][nj].rgbtBlue;
                        count++;
                    }
                }
            }

            // Calculate the average color values
            image[i][j].rgbtRed = round(red / (float)count);
            image[i][j].rgbtGreen = round(green / (float)count);
            image[i][j].rgbtBlue = round(blue / (float)count);
        }
    }
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    // Sobel kernels
    int Gx[3][3] = {
        {-1, 0, 1},
        {-2, 0, 2},
        {-1, 0, 1}
    };
    int Gy[3][3] = {
        {-1, -2, -1},
        {0, 0, 0},
        {1, 2, 1}
    };

    // Create a copy of the image to store the original values
    RGBTRIPLE temp[height][width];

    // Copy the original image to temp
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            temp[i][j] = image[i][j];
        }
    }

    // Loop over each pixel
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int Gx_red = 0;
            int Gx_green = 0;
            int Gx_blue = 0;
            int Gy_red = 0;
            int Gy_green = 0;
            int Gy_blue = 0;

            // Loop over the 3x3 grid of neighboring pixels
            for (int di = -1; di <= 1; di++)
            {
                for (int dj = -1; dj <= 1; dj++)
                {
                    int ni = i + di;
                    int nj = j + dj;

                    // Check if the neighboring pixel is within the bounds of the image
                    if (ni >= 0 && ni < height && nj >= 0 && nj < width)
                    {
                        Gx_red += temp[ni][nj].rgbtRed * Gx[di + 1][dj + 1];
                        Gx_green += temp[ni][nj].rgbtGreen * Gx[di + 1][dj + 1];
                        Gx_blue += temp[ni][nj].rgbtBlue * Gx[di + 1][dj + 1];
                        Gy_red += temp[ni][nj].rgbtRed * Gy[di + 1][dj + 1];
                        Gy_green += temp[ni][nj].rgbtGreen * Gy[di + 1][dj + 1];
                        Gy_blue += temp[ni][nj].rgbtBlue * Gy[di + 1][dj + 1];
                    }
                }
            }

            // Calculate the magnitude of the gradient
            int red = round(sqrt(Gx_red * Gx_red + Gy_red * Gy_red));
            int green = round(sqrt(Gx_green * Gx_green + Gy_green * Gy_green));
            int blue = round(sqrt(Gx_blue * Gx_blue + Gy_blue * Gy_blue));

            // Cap the values at 255
            image[i][j].rgbtRed = red > 255 ? 255 : red;
            image[i][j].rgbtGreen = green > 255 ? 255 : green;
            image[i][j].rgbtBlue = blue > 255 ? 255 : blue;
        }
    }
}
