import json
import yaml
import gendiff.formats.stylish as stylish
import gendiff.formats.plain as plain
import gendiff.formats.json as json_format


MAP_INPUT_TO_FORMAT = {'stylish': stylish,
                       'plain': plain,
                       'json': json_format,
                       None: stylish}


def convert_file_to_dict(file):
    file_list = file.split('.')
    file_format = file_list[len(file_list) - 1]
    if file_format == 'json':
        with open(file, "r") as read_file:
            file_converted = json.load(read_file)
    if file_format in ('yaml', 'yml'):
        with open(file, "r") as read_file:
            file_converted = yaml.load(read_file, Loader=yaml.FullLoader)
    return file_converted


def make_diff_tree(node1, node2):
    tree = {}
    common_keys = set(node1.keys()) & set(node2.keys())
    removed = set(node1.keys()) - common_keys
    added = set(node2.keys()) - common_keys
    tree.update({key: 'removed' for key in removed})
    tree.update({key: 'added' for key in added})
    for key in common_keys:
        if isinstance(node1[key], dict) and isinstance(node2[key], dict):
            tree[key] = make_diff_tree(node1[key], node2[key])
            continue
        tree[key] = 'unchanged' if node1[key] == node2[key] else 'updated'
    return tree


def generate_diff(file1, file2, format_name='stylish'):
    file1_dict = convert_file_to_dict(file1)
    file2_dict = convert_file_to_dict(file2)
    diff = make_diff_tree(file1_dict, file2_dict)
    format = MAP_INPUT_TO_FORMAT[format_name]
    return format.modify(diff, file1_dict, file2_dict)
