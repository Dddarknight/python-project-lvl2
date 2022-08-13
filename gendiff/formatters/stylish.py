import itertools


MAP_KEY_TYPE_TO_PREFIX = {'nested': '  ',
                          'updated': '',
                          'unchanged': '  ',
                          'removed': '- ',
                          'added': '+ '}


def normalize(x):
    if x is True:
        return 'true'
    elif x is False:
        return 'false'
    elif x is None:
        return 'null'
    else:
        return str(x)


def get_indent(depth, case='default'):
    if case == 'with_special_indent':
        return ' ' * (depth * 4 - 2)
    else:
        return ' ' * depth * 4


def stringify(value, depth):

    def iter_(current_value, depth):
        if not isinstance(current_value, dict):
            return normalize(current_value)
        lines = []
        for key, val in current_value.items():
            lines.append(f'{get_indent(depth+1)}{key}: {iter_(val, depth+1)}')
        result = itertools.chain("{", lines, [get_indent(depth) + "}"])
        return '\n'.join(result)

    return iter_(value, depth)


def format(diff_tree):
    def inner(diff_nodes, depth=1):
        initial_indent = get_indent(depth, case='with_special_indent')
        strings = ['{\n']
        for node in diff_nodes:
            key_type = node['type']
            key_name = node['key_name']
            special_indent = MAP_KEY_TYPE_TO_PREFIX[key_type]
            indent = f'{initial_indent}{special_indent}'
            if key_type == 'nested':
                nested_value = inner(node['children'], depth + 1)
                strings.extend([f'{indent}{key_name}: {nested_value}'])
                continue
            if key_type == 'updated':
                file1_value = stringify(node['file1_value'], depth)
                file2_value = stringify(node['file2_value'], depth)
                strings.extend(
                    [f'{initial_indent}- {key_name}: {file1_value}\n',
                     f'{initial_indent}+ {key_name}: {file2_value}\n'])
                continue
            if key_type in ('unchanged', 'removed'):
                value = node['file1_value']
            else:
                value = node['file2_value']
            normalized_value = stringify(value, depth)
            strings.extend([f'{indent}{key_name}: '
                            f'{normalized_value}\n'])
        strings.extend([get_indent(depth - 1), '}', '\n'])
        return ''.join(strings)
    return ''.join(inner(diff_tree)).strip('\n')
