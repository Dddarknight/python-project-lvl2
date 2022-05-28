import json
import yaml


def normalize_bool(x):
    if x is True:
        return 'true'
    elif x is False:
        return 'false'
    else:
        return x


def converting(file):
    file_list = file.split('.')
    if file_list[len(file_list) - 1] == 'json':
        with open(file, "r") as read_file:
            file_converted = json.load(read_file)
    if (file_list[len(file_list) - 1] == 'yaml' or (
            file_list[len(file_list) - 1] == 'yml')):
        with open(file, "r") as read_file:
            file_converted = yaml.load(read_file, Loader=yaml.FullLoader)
    file_converted = {key: normalize_bool(value)
                      for key, value in file_converted.items()}
    return file_converted


def generate_diff(file1, file2):
    file1_converted = converting(file1)
    file2_converted = converting(file2)
    common_keys = set(file1_converted.keys()) & set(file2_converted.keys())
    result_string = '{' + '\n'
    for key in common_keys:
        if file1_converted[key] == file2_converted[key]:
            result_string += f'    {key}: {file1_converted[key]}\n'
        else:
            result_string += f'  - {key}: {file1_converted[key]}\n' + \
                             f'  + {key}: {file2_converted[key]}\n'
    for key in (set(file1_converted.keys()) - common_keys):
        result_string += f'  - {key}: {file1_converted[key]}\n'
    for key in (set(file2_converted.keys()) - common_keys):
        result_string += f'  + {key}: {file2_converted[key]}\n'
    result_string += '}'
    return result_string
