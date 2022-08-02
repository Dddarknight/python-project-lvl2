from gendiff.diffs import tree
from gendiff.parsers import file_to_dict
from gendiff.formatters.builder import modify


def extract_file_format(file_path):
    file_list = file_path.split('.')
    file_format = file_list[-1]
    return file_format


def generate_diff(file1_path, file2_path, formatter_name='stylish'):
    file1_data = open(file1_path, 'r')
    file2_data = open(file2_path, 'r')
    file1_format = extract_file_format(file1_path)
    file2_format = extract_file_format(file2_path)
    file1_dict = file_to_dict.convert(file1_data, file1_format)
    file2_dict = file_to_dict.convert(file2_data, file2_format)
    diff = tree.make(file1_dict, file2_dict)
    print(diff)
    return modify(diff, file1_dict, file2_dict, formatter_name)
