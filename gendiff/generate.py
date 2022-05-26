import json


def generate_diff(file1, file2):
    with open(file1, "r") as read_file1:
        file1_converted = json.load(read_file1)
    with open(file2, "r") as read_file2:
        file2_converted = json.load(read_file2)
    common_keys = set(file1_converted.keys()) & set(file2_converted.keys())
    result_string = '{' + '\n'
    for key in common_keys:
        if file1_converted[key] == file2_converted[key]:
            result_string += f'  {key}: {file1_converted[key]}\n'
        else:
            result_string += f'- {key}: {file1_converted[key]}\n+ {key}: {file2_converted[key]}\n'
    for key in (set(file1_converted.keys()) - common_keys):
        result_string += f'- {key}: {file1_converted[key]}\n'
    for key in (set(file2_converted.keys()) - common_keys):
        result_string += f'+ {key}: {file2_converted[key]}\n'
    result_string += '}'
    return result_string