import re

def luhn_algorithm(card_number):
    total = 0
    num_digits = len(card_number)
    odd_even = num_digits & 1

    for count in range(num_digits):
        digit = int(card_number[count])

        if not ((count & 1) ^ odd_even):
            digit = digit * 2
        if digit > 9:
            digit = digit - 9

        total += digit

    return (total % 10) == 0

def get_card_type(card_number):
    if re.match(r'^3[47][0-9]{13}$', card_number):
        return "AMEX"
    elif re.match(r'^5[1-5][0-9]{14}$', card_number):
        return "MASTERCARD"
    elif re.match(r'^4[0-9]{12}(?:[0-9]{3})?$', card_number):
        return "VISA"
    else:
        return "INVALID"

def main():
    card_number = input("Number: ")

    if luhn_algorithm(card_number):
        card_type = get_card_type(card_number)
    else:
        card_type = "INVALID"

    print(card_type)

if __name__ == "__main__":
    main()
