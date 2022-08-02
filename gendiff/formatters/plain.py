def normalize_bool_none(elem):
    if elem is True:
        return 'true'
    elif elem is False:
        return 'false'
    elif elem is None:
        return 'null'
    else:
        return elem


def normalize_dict_str(elem):
    if isinstance(elem, dict):
        return '[complex value]'
    elif isinstance(elem, str):
        return f"'{elem}'"
    else:
        return elem


def normalize(elem):
    return normalize_bool_none(normalize_dict_str(elem))


def find_path(path, node):
    path = path.split('.')
    for elem in path:
        node = node[elem]
    return node


MAP_STATUS_TO_TEXT = {'updated': ' was updated. From ',
                      'removed': ' was removed',
                      'added': ' was added with value: '}


def modify_elem(key_type, node1, node2, path_relative):
    result_str = f"Property '{path_relative}'"
    if key_type == 'removed':
        result_str += f"{MAP_STATUS_TO_TEXT[key_type]}\n"
    elif key_type == 'updated':
        fact_value = normalize(find_path(path_relative, node2))
        old_value = normalize(find_path(path_relative, node1))
        result_str += (
            f"{MAP_STATUS_TO_TEXT[key_type]}{old_value} to {fact_value}\n")
    elif key_type == 'added':
        fact_value = normalize(find_path(path_relative, node2))
        result_str += f"{MAP_STATUS_TO_TEXT[key_type]}{fact_value}\n"
    return result_str


def modify(diff_tree, file1_node, file2_node):

    def inner(diff_tree, path='', result_str=''):
        for key in diff_tree.keys():
            key_type = diff_tree[key]['type']
            path_relative = f'{path}{key}'
            if key_type == 'nested':
                result_str += inner(diff_tree[key]['children'],
                                    path=(path_relative + '.'))
            if key_type in ('updated', 'added', 'removed'):
                result_str += modify_elem(key_type,
                                          file1_node,
                                          file2_node,
                                          path_relative)
        path = ''
        return result_str
    return (inner(diff_tree)).strip('\n')
