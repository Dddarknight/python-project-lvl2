from gendiff import diff_tree
from gendiff import file_to_dict
from gendiff.formatters import format


def extract_file_format(file_path):
    name_parts = file_path.split('.')
    file_format = name_parts[-1]
    return file_format


def generate_diff(file1_path, file2_path, format_name='stylish'):
    file1_data = open(file1_path, 'r')
    file2_data = open(file2_path, 'r')
    file1_format = extract_file_format(file1_path)
    file2_format = extract_file_format(file2_path)
    file1_dict = file_to_dict.convert(file1_data, file1_format)
    file2_dict = file_to_dict.convert(file2_data, file2_format)
    diff = diff_tree.build(file1_dict, file2_dict)
    return format(diff, format_name)
