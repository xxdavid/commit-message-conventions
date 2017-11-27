#!/usr/bin/env python3
from config import Directories
from file_utils import load_txt_into_set, load_json, open_file_dir_safe
import re

infinitives = load_txt_into_set(f"{Directories.processed_data}/infinitive.txt")
irregular = load_json(f"{Directories.processed_data}/irregular_verbs.json")

imperative_file = open_file_dir_safe(f"{Directories.processed_data}/imperative.txt", 'w')
third_person_file = open_file_dir_safe(f"{Directories.processed_data}/third_person.txt", 'w')
gerund_file = open_file_dir_safe(f"{Directories.processed_data}/gerund.txt", 'w')
past_tense_file = open_file_dir_safe(f"{Directories.processed_data}/past_tense.txt", 'w')

vowel = "[aeiouy]"
consonant = "[b-df-hj-np-tv-z]"

for infinitive in infinitives:
    # imperative
    # I know this is a duplicity but the two files have
    # a slightly different meaning and purpose
    imperative_file.write(infinitive + "\n")

    # third person
    if re.search(f"{consonant}y$", infinitive):
        third_person = infinitive[:-1] + "ies"
    elif re.search("(s|z|ch|sh|x)$", infinitive) or infinitive.endswith("o"):
        third_person = infinitive + "es"
    else:
        third_person = infinitive + "s"
    third_person_file.write(third_person + "\n")

    # gerund
    if infinitive.endswith("e"):
        gerund = infinitive[:-1] + "ing"
    elif re.search(f"{consonant}{vowel}{consonant}$", infinitive):
        gerund = infinitive + infinitive[-1] + "ing"
    else:
        gerund = infinitive + "ing"
    gerund_file.write(gerund + "\n")

    # past tense
    if infinitive in irregular:
        past_tense = irregular[infinitive]
    elif infinitive.endswith("e"):
        past_tense = infinitive + "d"
    elif re.search(f"{consonant}{vowel}{consonant}$", infinitive):
        past_tense = infinitive + infinitive[-1] + "ed"
    elif re.search(f"{consonant}y$", infinitive):
        past_tense = infinitive[:-1] + "ied"
    else:
        past_tense = infinitive + "ed"
    past_tense_file.write(past_tense + "\n")

gerund_exceptions = [
    "fixing"  # generated as fixxing
]
past_tense_exceptions = [
    "fixed"  # generated as fixxed
]

for word in gerund_exceptions:
    gerund_file.write(word + "\n")

for word in past_tense_exceptions:
    past_tense_file.write(word + "\n")

