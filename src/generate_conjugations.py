#!/usr/bin/env python3
from config import Directories
from conjugation_generator import ConjugationGenerator
from file_utils import load_txt_into_set, open_file_dir_safe

infinitives = load_txt_into_set(f"{Directories.processed_data}/infinitive.txt")

generator = ConjugationGenerator()

forms = ['imperative', 'third_person', 'gerund', 'past_tense']
for form in forms:
    file = open_file_dir_safe(f"{Directories.processed_data}/{form}.txt", 'w')
    with file:
        for word in infinitives:
            method = getattr(generator, form)
            conjugation = method(word)
            file.write(conjugation + "\n")
