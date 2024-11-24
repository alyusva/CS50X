#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <ctype.h>
#include "dictionary.h"

// Represents number of buckets in hash table
#define N 100000

// Hash table
node *table[N];

// Number of words in dictionary
unsigned int word_count = 0;

// Hashes word to a number
unsigned int hash(const char *word)
{
    unsigned int hash = 0;
    while (*word)
    {
        hash = (hash << 2) ^ tolower(*word++);
    }
    return hash % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // Initialize hash table
    for (int i = 0; i < N; i++)
    {
        table[i] = NULL;
    }

    // Open dictionary file
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        return false;
    }

    // Buffer to store words
    char word[LENGTH + 1];

    // Read words from file
    while (fscanf(file, "%s", word) != EOF)
    {
        // Create a new node
        node *new_node = malloc(sizeof(node));
        if (new_node == NULL)
        {
            return false;
        }
        strcpy(new_node->word, word);

        // Hash the word to obtain a hash value
        int index = hash(word);

        // Insert node into hash table
        new_node->next = table[index];
        table[index] = new_node;

        // Increment word count
        word_count++;
    }

    // Close dictionary file
    fclose(file);

    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return word_count;
}

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // Create a copy of the word in lowercase
    char lower_word[LENGTH + 1];
    int i = 0;
    while (word[i] && i < LENGTH)
    {
        lower_word[i] = tolower(word[i]);
        i++;
    }
    lower_word[i] = '\0';

    // Hash the word to get the index
    int index = hash(lower_word);

    // Traverse the linked list at that index to find the word
    node *cursor = table[index];
    while (cursor != NULL)
    {
        if (strcasecmp(cursor->word, lower_word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }
    return false;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // Iterate over each bucket in the hash table
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];
        while (cursor != NULL)
        {
            node *temp = cursor;
            cursor = cursor->next;
            free(temp);
        }
    }
    return true;
}
