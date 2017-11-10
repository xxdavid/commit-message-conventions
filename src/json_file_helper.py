import json

def save_json(content, filename):
    encoded = json.dumps(content, indent=2)

    file = open(filename, "w")
    with file:
        file.write(encoded)