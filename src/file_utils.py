import json


def save_json(content, filename):
    encoded = json.dumps(content, indent=2)

    file = open(filename, 'w')
    with file:
        file.write(encoded)


def load_txt_into_dict(path, skip_first_line=True, value=True):
    result = {}
    file = open(path, 'r')
    with file:
        if skip_first_line:
            file.readline()

        for line in file:
            line = line.strip()
            result[line] = value

    return result
