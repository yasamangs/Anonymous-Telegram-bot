import json


def read_json_file(file_path):
    with open(file_path, 'r') as f:
        json.load(f)


def write_json_file(data, file_path, indent=4):
    with open(file_path, 'a') as f:
        json.dump(data, f, indent=indent)

def write_file(data, file_path):
    with open(file_path, 'w') as f:
        f.write(data)
    
