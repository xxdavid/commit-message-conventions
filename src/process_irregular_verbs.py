#!/usr/bin/env python3
from pyquery import PyQuery as pq
import re

from config import Directories
from file_utils import save_json

doc = pq(filename=f'{Directories.raw_data}/irregular_verbs.html')

table = doc(".wikitable")
tds = table("tr td:first")
texts = list(tds.map(lambda i, el: pq(el).text()))

words = {}
for text in texts:
    groups = re.findall("""(?:\w|/|\*|(?: /))+ – (?:\w|/|\*)+ – (?:\w|/|\*)+""", text)
    for group in groups:
        if group[0] == '*':
            continue  # archaic
        conjugations = group.split(' – ')
        conjugations = list(map(lambda x: x.split('/')[0].strip(), conjugations))
        infinitive = conjugations.pop(0)
        words[infinitive] = conjugations[0]

save_json(words, f"{Directories.processed_data}/irregular_verbs.json")
