"""
This module contains the implementation of the get_number_of_characters function, which calculates the total number of characters in a given string or a list of strings.
"""

import csv
import nltk

def get_number_of_characters(text):
    """
    This function takes a string or a list of strings as input and returns the total number of characters.
    """
    if isinstance(text, str):
        return len(text)
    elif isinstance(text, list):
        return sum(len(item) for item in text)
    else:
        raise ValueError("Input must be a string or a list of strings.")

def get_character_set(text):
    """
    This function takes a string or a list of strings as input and returns a set of unique characters.
    """
    if isinstance(text, str):
        return set(text)
    elif isinstance(text, list):
        return set(char for item in text for char in item)
    else:
        raise ValueError("Input must be a string or a list of strings.")

def get_number_of_occurrences(text, character):
    """
    This function takes a string or a list of strings and a character as input and returns the number of occurrences of that character.
    """
    if isinstance(text, str):
        return text.count(character)
    elif isinstance(text, list):
        return sum(item.count(character) for item in text)
    else:
        raise ValueError("Input must be a string or a list of strings.")

def get_number_character_set(text):
    """
    This function takes a string or a list of strings as input and returns the number of unique characters.
    """
    set = get_character_set(text)
    data = {}
    for char in set:
        data[char] = get_number_of_occurrences(text, char)
    return data

def full_text_search(text, search_string):
    """
    This function takes a string or a list of strings and a search string as input and returns the number of occurrences of the search string.
    """
    if isinstance(text, str):
        return text.count(search_string)
    elif isinstance(text, list):
        return sum(item.count(search_string) for item in text)
    else:
        raise ValueError("Input must be a string or a list of strings.")

def tokenize_text(text):
    """
    This function takes a string or a list of strings as input and returns a list of tokens.
    """
    if isinstance(text, str):
        return nltk.word_tokenize(text)
    elif isinstance(text, list):
        list_of_token_lists = [nltk.word_tokenize(item) for item in text]
        return [token for sublist in list_of_token_lists for token in sublist]
    else:
        raise ValueError("Input must be a string or a list of strings.")

def tokenize_text_with_positions(text):
    """
    This function takes a string or a list of strings as input and returns a list of tuples, where each tuple contains a token and its position in the text.
    """
    if isinstance(text, str):
        tokens = nltk.word_tokenize(text)
        return [(token,0, index) for index, token in enumerate(tokens)]
    elif isinstance(text, list):
        tokens_with_positions = []
        for document, item in enumerate(text):
            tokens = nltk.word_tokenize(item)
            for index, token in enumerate(tokens):
                tokens_with_positions.append((token, document, index))
        return tokens_with_positions
    else:
        raise ValueError("Input must be a string or a list of strings.")

def get_number_of_words(text):
    """
    This function takes a string or a list of strings as input and returns the total number of words.
    """
    tokens = tokenize_text(text)
    if isinstance(tokens, list):
        return sum(len(item) for item in tokens)
    else:
        return len(tokens)

def get_number_of_sentences(text):
    """
    This function takes a string or a list of strings as input and returns the number of sentences.
    """
    if isinstance(text, str):
        return len(nltk.sent_tokenize(text))
    elif isinstance(text, list):
        return sum(len(nltk.sent_tokenize(item)) for item in text)
    else:
        raise ValueError("Input must be a string or a list of strings.")

def get_number_of_different_words(text):
    """
    This function takes a string or a list of strings as input and returns the number of unique words.
    """
    tokens = tokenize_text(text)
    if isinstance(tokens, list):
        return len(set(tokens))
    else:
        return len(set(tokens))

def get_inverted_index(text):
    """
    This function takes a string or a list of strings as input and returns an inverted index, which is a dictionary where the keys are unique words and the values are lists of indices where those words appear in the text.
    """
    tokens_with_positions = tokenize_text_with_positions(text)
    inverted_index = {}
    for token, document, index in tokens_with_positions:
        if token not in inverted_index:
            inverted_index[token] = []
        inverted_index[token].append((document, index))
    return inverted_index

if __name__ == '__main__':
    with open('data/test.csv', 'r', encoding='utf-8') as f:
        data = csv.reader(f)
        skip = True
        for row in data:
            if skip:
                skip = False
                continue
            text = row[1]
            print(get_number_of_characters(text))
            print(get_character_set(text))
            print(get_number_of_occurrences(text, 'o'))
            print(get_number_character_set(text))
            print(full_text_search(text, "test"))
            print(tokenize_text(text))
            print(get_number_of_words(text))
            print(get_number_of_different_words(text))
            print(get_inverted_index(text))
