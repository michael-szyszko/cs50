// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

void free_nodes(node *words);

// Hash table setup for 26 * 26 for aa to zz hash table
const unsigned int N = 676;

//
double WORD_COUNT;
// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    int hash_value = hash(word);

    node *dict_word = table[hash_value];

    while (dict_word != NULL)
    {
        if (strcasecmp(dict_word->word, word) == 0)
        {
            return true;
        }
        else
        {
            dict_word = dict_word->next;
        }
    }

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    if (strlen(word) == 1)
    {
        return toupper(word[0]) - 'A';
    }
    else
    {
        return toupper(word[1]) - 'A' + (toupper(word[0]) - 'A') * 26;
    }
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    WORD_COUNT = 0;
    FILE *inptr = fopen(dictionary, "r");
    if (inptr == NULL)
    {
        printf("Could not open %s.\n", dictionary);
        return 1;
    }

    // set all points to null in hash table
    for (int i = 0; i < LENGTH; i++)
    {
        table[i] = NULL;
    }

    char temp[LENGTH + 1];

    while (fscanf(inptr, "%s", temp) != EOF)
    {
        node *word = malloc(sizeof(node));
        if (word == NULL)
        {
            unload();
            printf("memory error");
            fclose(inptr);
            return false;
        }

        int hash_value = hash(temp);
        strcpy(word->word, temp);
        WORD_COUNT += 1;

        if (table[hash_value] == NULL)
        {
            table[hash_value] = word;
            word->next = NULL;
        }
        else
        {
            node *temp_ptr = table[hash_value];
            table[hash_value] = word;
            word->next = temp_ptr;
        }
    }
    fclose(inptr);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return WORD_COUNT;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        if (table[i] != NULL)
        {
            free_nodes(table[i]);
        }
    }
    return true;
}

// Free node and all linked nodes
void free_nodes(node *words)
{
    // TODO: Handle base case
    if (words->next == NULL)
    {
        free(words);
        return;
    }
    else
    {
        free_nodes(words->next);
        free(words);
    }
}
