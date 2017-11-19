#!/usr/bin/env python3
import re
from file_utils import open_file_dir_safe

input_file = open("../data/raw/verbs.txt")
output_file = open_file_dir_safe("../data/processed/infinitives.txt", "w")

with input_file, output_file:
    for line in input_file:
        match = re.match("""^[0-9]{8}\s[0-9]{2}\s[a-z]\s[0-9]{2}\s([a-zA-Z]*)\s""", line)
        if match:
            output_file.write(match.group(1) + "\n")
