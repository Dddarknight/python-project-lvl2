MAP_BOOL_NONE_VALUE_TO_REQUIRED = {True: 'true', False: 'false', None: 'null'}


def normalize(elem):
    if isinstance(elem, dict):
        return '[complex value]'
    elif isinstance(elem, str):
        return f"'{elem}'"
    elif elem in MAP_BOOL_NONE_VALUE_TO_REQUIRED.keys():
        return MAP_BOOL_NONE_VALUE_TO_REQUIRED[elem]
    else:
        return elem


def find_path(path, node):
    path = path.split('.')
    for elem in path:
        node = node[elem]
    return node


MAP_STATUS_TO_TEXT = {'updated': ' was updated. From ',
                      'removed': ' was removed',
                      'added': ' was added with value: '}


def modify_elem(value, file1, file2, path_relative):
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


def modify(tree, file1, file2):

    def inner(tree, path='', result_str=''):
        for key in sorted(tree.keys()):
            value = tree[key]
            path_relative = f'{path}{key}'
            if isinstance(value, dict):
                result_str += inner(value, path=(path_relative + '.'))
            if value in ('updated', 'added', 'removed'):
                result_str += modify_elem(value, file1, file2, path_relative)
        path = ''
        return result_str
    return (inner(tree)).strip('\n')
