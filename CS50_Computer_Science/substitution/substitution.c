#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

bool is_valid_key(string key);
string encrypt(string plaintext, string key);

int main(int argc, string argv[])
{
    // Verificar si el número de argumentos es correcto
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    string key = argv[1];

    // Verificar si la clave es válida
    if (!is_valid_key(key))
    {
        printf("Key must contain 26 unique alphabetic characters.\n");
        return 1;
    }

    // Solicitar el texto plano al usuario
    string plaintext = get_string("plaintext: ");

    // Encriptar el texto plano usando la clave
    string ciphertext = encrypt(plaintext, key);

    // Imprimir el texto encriptado
    printf("ciphertext: %s\n", ciphertext);

    return 0;
}

// Función para verificar si la clave es válida
bool is_valid_key(string key)
{
    // Verificar que la longitud de la clave sea 26
    if (strlen(key) != 26)
    {
        return false;
    }

    // Verificar que todos los caracteres sean alfabéticos y únicos
    bool seen[26] = {false};
    for (int i = 0; i < 26; i++)
    {
        if (!isalpha(key[i]))
        {
            return false;
        }
        int index = toupper(key[i]) - 'A';
        if (seen[index])
        {
            return false;
        }
        seen[index] = true;
    }
    return true;
}

// Función para encriptar el texto plano usando la clave
string encrypt(string plaintext, string key)
{
    int n = strlen(plaintext);
    string ciphertext = plaintext;
    for (int i = 0; i < n; i++)
    {
        if (isalpha(plaintext[i]))
        {
            bool is_upper = isupper(plaintext[i]);
            int index = toupper(plaintext[i]) - 'A';
            char cipher_char = is_upper ? toupper(key[index]) : tolower(key[index]);
            ciphertext[i] = cipher_char;
        }
        else
        {
            ciphertext[i] = plaintext[i];
        }
    }
    return ciphertext;
}
