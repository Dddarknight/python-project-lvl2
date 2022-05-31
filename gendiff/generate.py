import json
import yaml
from gendiff.stylish import stylish
from gendiff.plain import plain
from gendiff.json import json_


def converting(file):
    file_list = file.split('.')
    if file_list[len(file_list) - 1] == 'json':
        with open(file, "r") as read_file:
            file_converted = json.load(read_file)
    if (file_list[len(file_list) - 1] == 'yaml' or (
            file_list[len(file_list) - 1] == 'yml')):
        with open(file, "r") as read_file:
            file_converted = yaml.load(read_file, Loader=yaml.FullLoader)
    return file_converted


def diff_internal(node1, node2):
    tree = {}
    common_keys = set(node1.keys()) & set(node2.keys())
    removed = set(node1.keys()) - common_keys
    added = set(node2.keys()) - common_keys
    tree.update({key: 'removed' for key in removed})
    tree.update({key: 'added' for key in added})
    for key in common_keys:
        if isinstance(node1[key], dict) and isinstance(node2[key], dict):
            tree[key] = diff_internal(node1[key], node2[key])
            continue
        tree[key] = 'unchanged' if node1[key] == node2[key] else 'updated'
    return tree


def generate_diff(file1, file2, format_name='stylish'):
    file1_converted = converting(file1)
    file2_converted = converting(file2)
    diff = diff_internal(file1_converted, file2_converted)
    if format_name == 'stylish' or format_name is None:
        return stylish(diff, file1_converted, file2_converted)
    if format_name == 'plain':
        return plain(diff, file1_converted, file2_converted)
    if format_name == 'json':
        return json_(diff, file1_converted, file2_converted)
