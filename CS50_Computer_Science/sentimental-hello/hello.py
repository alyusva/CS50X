from cs50 import get_string

def main():
    # Solicita el nombre del usuario
    name = get_string("What is your name? ")
    # Imprime el saludo personalizado
    print(f"hello, {name}")

if __name__ == "__main__":
    main()
