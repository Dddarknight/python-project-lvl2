def normalize(value):
    if isinstance(value, dict):
        return '[complex value]'
    elif isinstance(value, str):
        return f"'{value}'"
    elif value is True:
        return 'true'
    elif value is False:
        return 'false'
    elif value is None:
        return 'null'
    else:
        return value


MAP_TYPE_TO_TEXT = {'updated': ' was updated. From ',
                    'removed': ' was removed',
                    'added': ' was added with value: '}


def format_node(node, path_relative):
    result_str = f"Property '{path_relative}'"
    key_type = node['type']
    if key_type == 'removed':
        result_str += f"{MAP_TYPE_TO_TEXT[key_type]}\n"
    elif key_type == 'updated':
        file1_value = normalize(node['file1_value'])
        file2_value = normalize(node['file2_value'])
        result_str += (
            f"{MAP_TYPE_TO_TEXT[key_type]}{file1_value} to {file2_value}\n")
    elif key_type == 'added':
        file2_value = normalize(node['file2_value'])
        result_str += f"{MAP_TYPE_TO_TEXT[key_type]}{file2_value}\n"
    return result_str


def format(diff_tree):

    def inner(diff_nodes, path='', result_str=''):
        for node in diff_nodes:
            key_type = node['type']
            key_name = node['key_name']
            relative_path = f'{path}{key_name}'
            if key_type == 'nested':
                result_str += inner(node['children'],
                                    path=(relative_path + '.'))
            if key_type in ('updated', 'added', 'removed'):
                result_str += format_node(node, relative_path)
        path = ''
        return result_str
    return (inner(diff_tree)).strip('\n')
