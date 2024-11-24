#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Puntos asignados a cada letra del alfabeto
int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

// Prototipo de función
int compute_score(string word);

int main(void)
{
    // Solicitar las palabras a los jugadores
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    // Calcular el puntaje de cada palabra
    int score1 = compute_score(word1);
    int score2 = compute_score(word2);

    // Determinar el ganador
    if (score1 > score2)
    {
        printf("Player 1 wins!\n");
    }
    else if (score2 > score1)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }
}

// Función para calcular el puntaje de una palabra
int compute_score(string word)
{
    int score = 0;
    for (int i = 0, n = strlen(word); i < n; i++)
    {
        if (isalpha(word[i]))
        {
            // Convertir la letra a mayúscula
            char uppercase_letter = toupper(word[i]);
            // Calcular el puntaje sumando el valor correspondiente
            score += POINTS[uppercase_letter - 'A'];
        }
    }
    return score;
}
