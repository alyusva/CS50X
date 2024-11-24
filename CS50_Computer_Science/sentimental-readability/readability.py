import re
from cs50 import get_string

def count_letters(text):
    letters = sum(1 for char in text if char.isalpha())
    return letters

def count_words(text):
    words = len(text.split())
    return words

def count_sentences(text):
    sentences = sum(1 for char in text if char in '.!?')
    return sentences

def calculate_index(letters, words, sentences):
    L = (letters / words) * 100
    S = (sentences / words) * 100
    index = 0.0588 * L - 0.296 * S - 15.8
    return round(index)

def main():
    text = get_string("Text: ")
    letters = count_letters(text)
    words = count_words(text)
    sentences = count_sentences(text)
    index = calculate_index(letters, words, sentences)

    if index < 1:
        print("Before Grade 1")
    elif index >= 16:
        print("Grade 16+")
    else:
        print(f"Grade {index}")

if __name__ == "__main__":
    main()
