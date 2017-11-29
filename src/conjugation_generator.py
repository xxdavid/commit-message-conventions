import re
from config import Directories
from file_utils import load_json


class ConjugationGenerator:
    def __init__(self):
        self.irregular =\
            load_json(f"{Directories.processed_data}/irregular_verbs.json")
        self.vowel = "[aeiouy]"
        self.consonant = "[b-df-hj-np-tv-z]"

    def imperative(self, infinitive):
        return infinitive

    def third_person(self, infinitive):
        if re.search(f"{self.consonant}y$", infinitive):
            return infinitive[:-1] + "ies"
        if re.search("(s|z|ch|sh|x)$", infinitive) or infinitive.endswith("o"):
            return infinitive + "es"
        return infinitive + "s"

    def gerund(self, infinitive):
        if infinitive.endswith("e"):
            return infinitive[:-1] + "ing"
        if re.search(f"{self.consonant}{self.vowel}{self.consonant}$", infinitive) \
                and not infinitive.endswith("fix"):
            return infinitive + infinitive[-1] + "ing"
        return infinitive + "ing"

    def past_tense(self, infinitive):
        if infinitive in self.irregular:
            return self.irregular[infinitive]
        if infinitive.endswith("e"):
            return infinitive + "d"
        if re.search(f"{self.consonant}{self.vowel}{self.consonant}$", infinitive) \
                and not infinitive.endswith("fix"):
            return infinitive + infinitive[-1] + "ed"
        if re.search(f"{self.consonant}y$", infinitive):
            return infinitive[:-1] + "ied"
        return infinitive + "ed"
