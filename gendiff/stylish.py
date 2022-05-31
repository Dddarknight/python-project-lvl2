from gendiff.stringify import stringify


def stylish(tree, node1, node2):
    def inner(tree, depth, node1, node2):
        indent = '  ' + '    ' * (depth)
        current_indent = '    ' * depth
        result_str = '{\n'
        for key, value in tree.items():
            if isinstance(value, dict):
                new_value = inner(value, depth + 1, node1[key], node2[key])
                result_str += f'{indent}  {key}: {new_value}'
                continue
            old_value, new_value = '', ''
            if value in ('unchanged', 'added', 'updated'):
                new_value = stringify(node2[key], depth + 1)
            if value in ('removed', 'updated'):
                old_value = stringify(node1[key], depth + 1)
            if value == 'unchanged':
                result_str += f'{indent}' '{key}: {new_value}\n'
                continue
            if old_value:
                result_str += f'{indent}'- '{key}: {new_value}\n'
            if new_value:
                result_str += f'{indent}'+ '{key}: {new_value}\n'
        return (result_str + current_indent + '}\n')
    return (inner(tree, 0, node1, node2)[:-2] + '}')
