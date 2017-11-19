import json
import os


def open_file_dir_safe(path, mode='r'):
    directory = os.path.dirname(path)
    os.makedirs(directory, exist_ok=True)
    return open(path, mode)


def save_json(content, path):
    encoded = json.dumps(content, indent=2)

    file = open_file_dir_safe(path, 'w')
    with file:
        file.write(encoded)


def load_json(path):
    file = open_file_dir_safe(path)
    return json.load(file)


def load_txt_into_dict(path, skip_first_line=True, value=True):
    result = {}
    file = open_file_dir_safe(path)
    with file:
        if skip_first_line:
            file.readline()

        for line in file:
            line = line.strip()
            result[line] = value

    return result
