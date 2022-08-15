MAP_TYPE_TO_TEXT = {'updated': ' was updated. From ',
                    'removed': ' was removed',
                    'added': ' was added with value: '}


def normalize(value):
    if isinstance(value, dict):
        return '[complex value]'
    if isinstance(value, str):
        return f"'{value}'"
    if value is True:
        return 'true'
    if value is False:
        return 'false'
    if value is None:
        return 'null'
    return value


def format_node(node, path_relative):
    node_rows = []
    node_rows.extend(f"Property '{path_relative}'")
    key_type = node['type']
    file1_value = normalize(node.get('file1_value', None))
    file2_value = normalize(node.get('file2_value', None))
    if key_type == 'removed':
        node_rows.extend(f"{MAP_TYPE_TO_TEXT[key_type]}\n")
    elif key_type == 'updated':
        node_rows.extend(
            f"{MAP_TYPE_TO_TEXT[key_type]}{file1_value} to {file2_value}\n")
    elif key_type == 'added':
        node_rows.extend(f"{MAP_TYPE_TO_TEXT[key_type]}{file2_value}\n")
    return node_rows


def format(diff_tree):

    def inner(diff_nodes, path=''):
        rows = []
        for node in diff_nodes:
            key_type = node['type']
            key_name = node['key_name']
            relative_path = f'{path}{key_name}'
            if key_type == 'nested':
                rows.extend(inner(node['children'],
                                     path=(f'{relative_path}.')))
            if key_type in ('updated', 'added', 'removed'):
                rows.extend(format_node(node, relative_path))
        return rows
    return (''.join(inner(diff_tree))).strip('\n')
