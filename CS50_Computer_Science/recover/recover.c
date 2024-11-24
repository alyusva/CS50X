#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

// Define the block size
#define BLOCK_SIZE 512

int main(int argc, char *argv[])
{
    // Check for correct usage
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover IMAGE\n");
        return 1;
    }

    // Open the memory card file
    FILE *card = fopen(argv[1], "r");
    if (card == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", argv[1]);
        return 1;
    }

    // Buffer to store a block of data
    uint8_t buffer[BLOCK_SIZE];

    // Variables to track the JPEG files
    FILE *img = NULL;
    char filename[8];
    int file_count = 0;

    // Read the memory card block by block
    while (fread(buffer, sizeof(uint8_t), BLOCK_SIZE, card) == BLOCK_SIZE)
    {
        // Check if the block contains the start of a new JPEG file
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff &&
            (buffer[3] & 0xf0) == 0xe0)
        {
            // If a new JPEG is found, close the previous one if it exists
            if (img != NULL)
            {
                fclose(img);
            }

            // Create a new JPEG file
            sprintf(filename, "%03i.jpg", file_count);
            img = fopen(filename, "w");
            if (img == NULL)
            {
                fprintf(stderr, "Could not create %s.\n", filename);
                fclose(card);
                return 1;
            }

            file_count++;
        }

        // If a JPEG file is open, write the block to it
        if (img != NULL)
        {
            fwrite(buffer, sizeof(uint8_t), BLOCK_SIZE, img);
        }
    }

    // Close any remaining files
    if (img != NULL)
    {
        fclose(img);
    }

    fclose(card);
    return 0;
}
