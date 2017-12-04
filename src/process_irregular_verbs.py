#!/usr/bin/env python3
from pyquery import PyQuery as pq
import re

from config import Directories
from file_utils import save_json


def parse_word_groups(cell):
    """
    Find word groups (i.e. word with its conjugations separated by hyphen).
    :param cell: content of a cell containing one or more word groups
    :return: list of parsed word groups (as strings)
    """
    return re.findall(
        """(?:\w|/|\*|(?: /))+ – (?:\w|/|\*)+ – (?:\w|/|\*)+""",
        cell
    )


def parse_conjugations(group):
    """
    Parse conjugations in a word group.
    :param group: string of a word group
    :return: list of parsed conjugations
    """
    return list(
        map(
            lambda x: x.split('/')[0].strip(),
            group.split(' – ')
            )
    )


def parse_cells(cells):
    """
    Parse words and their conjugations in cells.
    :param cells: list of raw cells
    :return: dictionary of words in infinitive:past_tense form
    """
    words = {}

    for cell in cells:
        text = pq(cell).text()
        groups = parse_word_groups(text)

        for group in groups:
            if group[0] == '*':
                continue  # archaic
            conjugations = parse_conjugations(group)
            infinitive = conjugations[0]
            words[infinitive] = conjugations[1]

    return words


def process_irregular_verbs():
    """
    Read irregular verbs from a downloaded Wikipedia page, parse it and save.
    """
    doc = pq(filename=f'{Directories.raw_data}/irregular_verbs.html')

    table = doc(".wikitable")
    raw_cells = table("tr td:first")

    words = parse_cells(raw_cells)

    save_json(words, f"{Directories.processed_data}/irregular_verbs.json")


process_irregular_verbs()
