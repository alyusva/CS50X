#include <ctype.h>
#include <cs50.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

// Prototipos de funciones
int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    // Solicitar al usuario que ingrese un texto
    string text = get_string("Text: ");

    // Contar el número de letras, palabras y oraciones en el texto
    int letters = count_letters(text);
    int words = count_words(text);
    int sentences = count_sentences(text);

    // Calcular el índice de Coleman-Liau
    float L = ((float) letters / words) * 100;
    float S = ((float) sentences / words) * 100;
    float index = 0.0588 * L - 0.296 * S - 15.8;

    // Redondear el índice al número entero más cercano
    int grade = round(index);

    // Imprimir el nivel de grado correspondiente
    if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (grade >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", grade);
    }
}

// Función para contar el número de letras en el texto
int count_letters(string text)
{
    int letters = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (isalpha(text[i]))
        {
            letters++;
        }
    }
    return letters;
}

// Función para contar el número de palabras en el texto
int count_words(string text)
{
    int words = 1; // Comenzamos en 1 porque la última palabra no tiene un espacio después
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (isspace(text[i]))
        {
            words++;
        }
    }
    return words;
}

// Función para contar el número de oraciones en el texto
int count_sentences(string text)
{
    int sentences = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            sentences++;
        }
    }
    return sentences;
}
