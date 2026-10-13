#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Character encoding declaration, supporting multilingual text.

import re
import sys

def clean_text(text):
    """Remove punctuation from a text."""
    punct = "./?,;'#\""
    for p in punct:
        text = text.replace(p, "")
    return text

def tokenize(text):
    """Convert text into tokens, return a list of tokens (words)."""
    return text.split()

def tokenize2(text):
    """Convert text into tokens using regular expressions."""
    spaces = r"\s+"
    words = re.split(spaces, text)
    return words

def word_freq(words):
    """Counts words and return a dictionary of words with their occurrences."""
    index = {}
    for w in words:
        if w in index:
            index[w] += 1
        else:
            index[w] = 1
    return index

def most_common_word(words_freq_table):
    """Counts words and returns the most frequent word."""
    frequent = ""
    frequency = 0
    for word in words_freq_table:
        if words_freq_table[word] > frequency:
            frequent = word
            frequency = words_freq_table[word]
    return frequent

def read_file(filename):
    """Read a text from file."""
    try:
        f1 = open(filename, encoding='utf-8')
    except Exception:
        print("Can't open file,", filename)
        sys.exit()
    text = f1.read()
    f1.close()
    return text

def main():
    text = """Surprise steepest recurred landlord mr wandered amounted of.
    past oh shew roof Continuing devonshire but considered its. Rose
    is song neat. Do depend better praise do friend garden an wonder to.
    Intention age nay otherwise but breakfast.
    Around garden beyond to extent by."""
    
    # Clean text
    text = clean_text(text)
    print("--- Cleaned Text ---")
    print(text)
    
    # Tokenize text
    words = tokenize(text)
    print("\n--- Tokens ---")
    print(words)
    
    # Word frequency
    words_nb = word_freq(words)
    print("\n--- Word Frequencies ---")
    print(words_nb)
    
    # Test reading from an external file
    try:
        data = read_file("data.txt")
        print("\n--- Data from file.txt ---")
        print(data)
        words_file = tokenize(data)
        word_freq_table = word_freq(words_file)
        freqw = most_common_word(word_freq_table)
        print(f"Most frequent word is '{freqw}' appearing {word_freq_table[freqw]} times.")
    except SystemExit:
        print("\n[Notice: Create a 'data.txt' file in your workspace to test the file-reading function!]")

if __name__ == "__main__":
    main()