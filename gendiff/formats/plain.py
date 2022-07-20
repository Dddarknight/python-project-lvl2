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


def make_plain_elem(value, file1, file2, path_relative):
    result_str = f"Property '{path_relative}'"
    if value == 'removed':
        result_str += f"{MAP_STATUS_TO_TEXT[value]}\n"
    elif value == 'updated':
        fact_value = normalize(find_path(path_relative, file2))
        old_value = normalize(find_path(path_relative, file1))
        result_str += (
            f"{MAP_STATUS_TO_TEXT[value]}{old_value} to {fact_value}\n")
    elif value == 'added':
        fact_value = normalize(find_path(path_relative, file2))
        result_str += f"{MAP_STATUS_TO_TEXT[value]}{fact_value}\n"
    return result_str


def make_plain(tree, file1, file2):

    def inner(tree, path='', result_str=''):
        for key in sorted(tree.keys()):
            value = tree[key]
            path_relative = f'{path}{key}'
            if isinstance(value, dict):
                result_str += inner(value, path=(path_relative + '.'))
            if value in ('updated', 'added', 'removed'):
                result_str += make_plain_elem(value, 
                                              file1,
                                              file2,
                                              path_relative)
        path = ''
        return result_str
    return (inner(tree)).strip('\n')
