import itertools


MAP_KEY_TYPE_TO_PREFIX = {'nested': '  ',
                          'updated': '',
                          'unchanged': '  ',
                          'removed': '- ',
                          'added': '+ '}


STANDART_SPACE_COUNT = 4
STANDART_SPECIAL_INDENT_LENGTH = 2


def normalize(x):
    if x is True:
        return 'true'
    if x is False:
        return 'false'
    if x is None:
        return 'null'
    return str(x)


def get_indent(depth, flag=False):
    return ' ' * (
        depth * STANDART_SPACE_COUNT - STANDART_SPECIAL_INDENT_LENGTH
    ) if flag else ' ' * depth * STANDART_SPACE_COUNT


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
    def inner(diff_nodes, depth=0):
        initial_indent = get_indent(depth + 1, flag=True)
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

            file1_value = stringify(node.get('file1_value', None), depth + 1)
            file2_value = stringify(node.get('file2_value', None), depth + 1)

            if key_type == 'updated':
                strings.extend(
                    [f'{initial_indent}- {key_name}: {file1_value}\n',
                     f'{initial_indent}+ {key_name}: {file2_value}\n'])
                continue
            if key_type in ('unchanged', 'removed'):
                strings.extend([f'{indent}{key_name}: '
                                f'{file1_value}\n'])
            else:
                strings.extend([f'{indent}{key_name}: '
                                f'{file2_value}\n'])
        strings.extend([get_indent(depth), '}', '\n'])
        return ''.join(strings)
    return ''.join(inner(diff_tree)).strip('\n')
