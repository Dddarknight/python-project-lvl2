import json
import yaml


def extract_file_format(file_path):
    file_list = file_path.split('.')
    file_format = file_list[-1]
    return file_format


def convert(file_path):
    file_format = extract_file_format(file_path)
    if file_format == 'json':
        with open(file_path, "r") as read_file:
            file_converted = json.load(read_file)
    if file_format in ('yaml', 'yml'):
        with open(file_path, "r") as read_file:
            file_converted = yaml.load(read_file, Loader=yaml.FullLoader)
    return file_converted
