#!/usr/bin/env python3
import sys
import os
import json
import gzip
import urllib.request
import io
from file_utils import open_file_dir_safe

date = sys.argv[1]

url = f"http://data.githubarchive.org/{date}.json.gz"

response = urllib.request.urlopen(url)
compressed_file = io.BytesIO(response.read())
file = gzip.GzipFile(fileobj=compressed_file)

output_filename = "../outputs/messages.txt"
output_mode = "a" if os.path.exists(output_filename) else "w"
output_file = open_file_dir_safe(output_filename, output_mode)

with file as f:
    for line in f:
        event = json.loads(line)
        if event['type'] == 'PushEvent':
            author = event['actor']['login']
            repo = event['repo']['name']
            commits = event['payload']['commits']
            for commit in commits:
                message_lines = commit['message'].split("\n")
                output_file.write(f"{author}::{repo}::{len(message_lines)}::{message_lines[0]}\n")
