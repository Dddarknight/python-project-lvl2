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


MAP_STATUS_TO_TEXT = {'updated': ' was updated. From ',
                      'removed': ' was removed',
                      'added': ' was added with value: '}


def modify_elem(diff_node, key, path_relative):
    result_str = f"Property '{path_relative}'"
    key_type = diff_node[key]['type']
    old_value = normalize(diff_node[key]['old_value'])
    new_value = normalize(diff_node[key]['new_value'])
    if key_type == 'removed':
        result_str += f"{MAP_STATUS_TO_TEXT[key_type]}\n"
    elif key_type == 'updated':
        result_str += (
            f"{MAP_STATUS_TO_TEXT[key_type]}{old_value} to {new_value}\n")
    elif key_type == 'added':
        result_str += f"{MAP_STATUS_TO_TEXT[key_type]}{new_value}\n"
    return result_str


def modify(diff_tree):

    def inner(diff_node, path='', result_str=''):
        for key in diff_node.keys():
            key_type = diff_node[key]['type']
            path_relative = f'{path}{key}'
            if key_type == 'nested':
                result_str += inner(diff_node[key]['children'],
                                    path=(path_relative + '.'))
            if key_type in ('updated', 'added', 'removed'):
                result_str += modify_elem(diff_node,
                                          key,
                                          path_relative)
        path = ''
        return result_str
    return (inner(diff_tree)).strip('\n')
