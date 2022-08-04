import itertools


def normalize(x):
    if x is True:
        return 'true'
    elif x is False:
        return 'false'
    elif x is None:
        return 'null'
    else:
        return x


def stringify(value, depth, replacer='    '):

    def iter_(current_value, depth):
        if not isinstance(current_value, dict):
            return str(normalize(current_value))

        current_indent = replacer * (depth + 1)
        lines = []
        for key, val in current_value.items():
            lines.append(f'{current_indent}{key}: {iter_(val, depth+1)}')
        result = itertools.chain("{", lines, [current_indent[:-4] + "}"])
        return '\n'.join(result)

    return iter_(value, depth)


def modify(diff_tree):
    def inner(diff_node, depth):
        indent = '  ' + '    ' * (depth)
        current_indent = '    ' * depth
        result_str = '{\n'
        for key in diff_node.keys():
            key_type = diff_node[key]['type']
            if key_type == 'nested':
                nested_value = inner(diff_node[key]['children'], depth + 1)
                result_str += f'{indent}  {key}: {nested_value}'
                continue
            old_value = stringify(diff_node[key]['old_value'], depth + 1)
            new_value = stringify(diff_node[key]['new_value'], depth + 1)
            if key_type == 'updated':
                result_str += f'{indent}- {key}: {old_value}\n' + (
                              f'{indent}+ {key}: {new_value}\n')
                continue
            map_type_to_value = {'unchanged': ['  ', old_value],
                                 'removed': ['- ', old_value],
                                 'added': ['+ ', new_value]}
            new_indent = map_type_to_value[key_type][0]
            result_str += (f'{indent}{new_indent}{key}: '
                           f'{map_type_to_value[key_type][1]}\n')
        return (result_str + current_indent + '}\n')
    return (inner(diff_tree, 0)[:-2] + '}')
