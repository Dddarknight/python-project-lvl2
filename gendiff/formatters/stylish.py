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


def modify(tree, node1, node2):
    def inner(tree, depth, node1, node2):
        indent = '  ' + '    ' * (depth)
        current_indent = '    ' * depth
        result_str = '{\n'
        for key in sorted(tree.keys()):
            value = tree[key]
            if isinstance(value, dict):
                new_value = inner(value, depth + 1, node1[key], node2[key])
                result_str += f'{indent}  {key}: {new_value}'
                continue
            if value == 'updated':
                old_value = stringify(node1[key], depth + 1)
                new_value = stringify(node2[key], depth + 1)
                result_str += f'{indent}- {key}: {old_value}\n' + (
                              f'{indent}+ {key}: {new_value}\n')
                continue
            dict_diff = {'unchanged': ['  ', node1],
                         'removed': ['- ', node1],
                         'added': ['+ ', node2]}
            new_value = stringify(dict_diff[value][1][key], depth + 1)
            new_indent = dict_diff[value][0]
            result_str += f'{indent}{new_indent}{key}: {new_value}\n'
        return (result_str + current_indent + '}\n')
    return (inner(tree, 0, node1, node2)[:-2] + '}')
