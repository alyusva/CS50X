#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int height;

    // Solicitar la altura al usuario, asegurándose de que esté entre 1 y 8 inclusive
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);

    // Construir las pirámides
    for (int i = 1; i <= height; i++)
    {
        // Imprimir espacios antes de la primera pirámide
        for (int j = 0; j < height - i; j++)
        {
            printf(" ");
        }

        // Imprimir hashes de la primera pirámide
        for (int j = 0; j < i; j++)
        {
            printf("#");
        }

        // Imprimir el espacio entre las pirámides
        printf("  ");

        // Imprimir hashes de la segunda pirámide
        for (int j = 0; j < i; j++)
        {
            printf("#");
        }

        // Nueva línea después de cada fila
        printf("\n");
    }

    return 0;
}
