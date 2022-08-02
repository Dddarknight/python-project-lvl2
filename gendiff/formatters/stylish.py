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


def modify(diff_tree, node1, node2):
    def inner(diff_tree, depth, node1, node2):
        indent = '  ' + '    ' * (depth)
        current_indent = '    ' * depth
        result_str = '{\n'
        for key in diff_tree.keys():
            type = diff_tree[key]['type']
            if type == 'nested':
                new_value = inner(diff_tree[key]['children'],
                                  depth + 1,
                                  node1[key],
                                  node2[key])
                result_str += f'{indent}  {key}: {new_value}'
                continue
            if type == 'updated':
                old_value = stringify(node1[key], depth + 1)
                new_value = stringify(node2[key], depth + 1)
                result_str += f'{indent}- {key}: {old_value}\n' + (
                              f'{indent}+ {key}: {new_value}\n')
                continue
            map_type_to_node = {'unchanged': ['  ', node1],
                                'removed': ['- ', node1],
                                'added': ['+ ', node2]}
            new_value = stringify(map_type_to_node[type][1][key],
                                  depth + 1)
            new_indent = map_type_to_node[type][0]
            result_str += f'{indent}{new_indent}{key}: {new_value}\n'
        return (result_str + current_indent + '}\n')
    return (inner(diff_tree, 0, node1, node2)[:-2] + '}')
