import itertools


INDENT_FOR_STRINGIFY = '    '
MAP_KEY_TYPE_TO_INDENT = {'nested': '  ',
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


def stringify(value, depth):

    def iter_(current_value, depth):
        if not isinstance(current_value, dict):
            return normalize(current_value)

        current_indent = INDENT_FOR_STRINGIFY * (depth + 1)
        last_indent = INDENT_FOR_STRINGIFY * depth
        lines = []
        for key, val in current_value.items():
            lines.append(f'{current_indent}{key}: {iter_(val, depth+1)}')
        result = itertools.chain("{", lines, [last_indent + "}"])
        return '\n'.join(result)

    return iter_(value, depth)


def format(diff_tree):
    def inner(diff_nodes, depth=1):
        initial_indent = ' ' * (depth * 4 - 2)
        last_indent = ' ' * (depth * 4 - 4)
        result_str = '{\n'
        for node in diff_nodes:
            key_type = node['type']
            key_name = node['key_name']
            special_indent = MAP_KEY_TYPE_TO_INDENT[key_type]
            indent = f'{initial_indent}{special_indent}'
            if key_type == 'nested':
                nested_value = inner(node['children'], depth + 1)
                result_str += f'{indent}{key_name}: {nested_value}'
                continue
            if key_type == 'updated':
                file1_value = stringify(node['file1_value'], depth)
                file2_value = stringify(node['file2_value'], depth)
                result_str += (f'{initial_indent}- {key_name}: {file1_value}\n'
                               f'{initial_indent}+ {key_name}: {file2_value}\n')
                continue
            if key_type in ('unchanged', 'removed'):
                value = node['file1_value']
            else:
                value = node['file2_value']
            normalized_value = stringify(value, depth)
            result_str += (f'{indent}{key_name}: '
                           f'{normalized_value}\n')
        return result_str + last_indent + '}' + '\n'
    return inner(diff_tree).strip('\n')
