#include <stdio.h>

int main(void) {
    char name[50];  // Declarar una variable para almacenar el nombre

    // Pedir al usuario su nombre
    printf("What's your name? ");
    scanf("%49s", name);  // Leer el nombre del usuario

    // Imprimir el saludo
    printf("hello, %s\n", name);
    return 0;
}
