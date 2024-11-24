#include <cs50.h>
#include <stdio.h>

// Prototipos de funciones
bool check_luhn(long number);
void check_card_type(long number);

int main(void)
{
    // Solicitar número de tarjeta al usuario
    long card_number = get_long("Number: ");

    // Verificar la validez del número de tarjeta usando el algoritmo de Luhn
    if (check_luhn(card_number))
    {
        // Determinar y mostrar el tipo de tarjeta
        check_card_type(card_number);
    }
    else
    {
        printf("INVALID\n");
    }
}

// Función para verificar la validez del número de tarjeta usando el algoritmo de Luhn
bool check_luhn(long number)
{
    int sum = 0;
    bool alternate = false;

    while (number > 0)
    {
        int digit = number % 10;
        if (alternate)
        {
            digit *= 2;
            if (digit > 9)
            {
                digit -= 9;
            }
        }
        sum += digit;
        alternate = !alternate;
        number /= 10;
    }

    return (sum % 10) == 0;
}

// Función para determinar y mostrar el tipo de tarjeta
void check_card_type(long number)
{
    // Obtener el tamaño del número de tarjeta
    int length = 0;
    long temp = number;
    while (temp > 0)
    {
        temp /= 10;
        length++;
    }

    // Obtener los primeros dos dígitos del número de tarjeta
    long start_digits = number;
    while (start_digits > 100)
    {
        start_digits /= 10;
    }

    // Verificar el tipo de tarjeta
    if (length == 15 && (start_digits == 34 || start_digits == 37))
    {
        printf("AMEX\n");
    }
    else if (length == 16 && (start_digits >= 51 && start_digits <= 55))
    {
        printf("MASTERCARD\n");
    }
    else if ((length == 13 || length == 16) && (start_digits / 10 == 4))
    {
        printf("VISA\n");
    }
    else
    {
        printf("INVALID\n");
    }
}
