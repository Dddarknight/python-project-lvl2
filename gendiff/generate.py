import json
import yaml
from gendiff.stringify import stringify


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
    for key in common_keys:
        if isinstance(node1[key], dict) and isinstance(node2[key], dict):
            tree[key] = diff_internal(node1[key], node2[key])
        else:
            if node1[key] == node2[key]:
                tree[key] = 'unchanged'
            else:
                tree[key] = 'changed'
    for key in (set(node1.keys()) - common_keys):
        tree[key] = 'only_first'
    for key in (set(node2.keys()) - common_keys):
        tree[key] = 'only_second'
    return tree


def stylysh(tree, node1, node2):
    def inner(tree, depth, node1, node2):
        indent = '  ' + '    ' * (depth)
        current_indent = '    ' * depth
        result_str = '{\n'
        for key, value in tree.items():
            if isinstance(value, dict):
                new_value = inner(value, depth + 1, node1[key], node2[key])
                result_str += f'{indent}  {key}: {new_value}'
            else:
                dict_diff = {'unchanged': ['  ', node1],
                             'only_first': ['- ', node1],
                             'only_second': ['+ ', node2]}
                if value == 'changed':
                    new_value1 = stringify(node1[key], depth + 1)
                    new_value2 = stringify(node2[key], depth + 1)
                    result_str += f'{indent}- {key}: {new_value1}\n' + (
                                  f'{indent}+ {key}: {new_value2}\n')
                else:
                    new_value = stringify(dict_diff[value][1][key], depth + 1)
                    new_indent = dict_diff[value][0]
                    result_str += f'{indent}{new_indent}{key}: {new_value}\n'
        return (result_str + current_indent + '}\n')
    return (inner(tree, 0, node1, node2)[:-2] + '}')


def generate_diff(file1, file2):
    file1_converted = converting(file1)
    file2_converted = converting(file2)
    diff = diff_internal(file1_converted, file2_converted)
    return stylysh(diff, file1_converted, file2_converted)
