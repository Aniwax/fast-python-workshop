#!/usr/bin/env python

from pathlib import Path


def sort_count_words(filepath, descending=True):
    """
    The function will count and sort the words in a text file.

    The words are defined by using a simple split and lower case.

    Parameters
    ----------
    filepath: str
        The input file.
    descending: bool, optional
        The order to be used in sorting (default True).

    Returns
    -------
    List
        The sorted list of tuples where the first element is the word and the second is
        its frequency.

    """
    counted_words = {}
    with open(filepath, "r") as file:
        for line in file:
            lower_words = line.lower().split()
            for word in lower_words:
                if word not in counted_words:
                    counted_words[word] = 1
                else:
                    counted_words[word] += 1

    return sorted(counted_words.items(), key=get_2nd_element, reverse=descending)


def get_2nd_element(tpl):
    return tpl[1]


if __name__ == "__main__":
    filepath = Path() / "gutenberg" / "README"
    top_n = 10
    histogram = sort_count_words(filepath)[:top_n]
    for word, count in histogram:
        print(word, ":", count)
    print("...")
