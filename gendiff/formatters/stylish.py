import itertools


MAP_KEY_TYPE_TO_PREFIX = {'nested': '  ',
                          'updated': '',
                          'unchanged': '  ',
                          'removed': '- ',
                          'added': '+ '}


SPACE_COUNT = 4
PREFIX_LENGTH = 2
ZERO_OFFSET = 0


def normalize(x):
    if x is True:
        return 'true'
    if x is False:
        return 'false'
    if x is None:
        return 'null'
    return str(x)


def get_indent(depth, offset=ZERO_OFFSET):
    return ' ' * (depth * SPACE_COUNT - offset)


def stringify(value, depth):

    def inner(current_value, depth):
        if not isinstance(current_value, dict):
            return normalize(current_value)
        lines = []
        for key, val in current_value.items():
            lines.append(f'{get_indent(depth+1)}{key}: {inner(val, depth+1)}')
        result = itertools.chain("{", lines, [get_indent(depth) + "}"])
        return '\n'.join(result)

    return inner(value, depth)


def format(diff_tree):
    def inner(diff_nodes, depth=1):
        depth_indent = get_indent(depth, offset=PREFIX_LENGTH)
        rows = ['{\n']
        for node in diff_nodes:
            key_type = node['type']
            key_name = node['key_name']
            prefix = MAP_KEY_TYPE_TO_PREFIX[key_type]
            indent = f'{depth_indent}{prefix}'
            if key_type == 'nested':
                nested_value = inner(node['children'], depth + 1)
                rows.extend([f'{indent}{key_name}: {nested_value}', '\n',
                             get_indent(depth), '}', '\n'])
                continue

            file1_value = stringify(node.get('file1_value'), depth)
            file2_value = stringify(node.get('file2_value'), depth)

            if key_type == 'updated':
                rows.extend(
                    [f'{depth_indent}- {key_name}: {file1_value}\n',
                     f'{depth_indent}+ {key_name}: {file2_value}\n'])
                continue
            if key_type in ('unchanged', 'removed'):
                rows.extend([f'{indent}{key_name}: '
                             f'{file1_value}\n'])
                continue
            rows.extend([f'{indent}{key_name}: '
                         f'{file2_value}\n'])
        return ''.join(rows).strip('\n')
    return f"{''.join(inner(diff_tree))}\n}}"
