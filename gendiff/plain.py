def normalize1(x):
    if x is True:
        return 'true'
    elif x is False:
        return 'false'
    elif x is None:
        return 'null'
    else:
        return x


def normalize2(x):
    if isinstance(x, dict):
        return '[complex value]'
    elif isinstance(x, str):
        return f"'{x}'"
    else:
        return x


def find_path(path, node):
    path = path.split('.')
    for elem in path:
        node = node[elem]
    return node


def plain_elem(value, file1, file2, path_int):
    dict_diff = {'updated': ' was updated. From ',
                 'removed': ' was removed',
                 'added': ' was added with value: '}
    result_str = f"Property '{path_int}'"
    if value == 'removed':
        result_str += f"{dict_diff[value]}\n"
    elif value == 'updated':
        fact_value = normalize1(normalize2(find_path(path_int, file2)))
        old_value = normalize1(normalize2(find_path(path_int, file1)))
        result_str += f"{dict_diff[value]}{old_value} to {fact_value}\n"
    elif value == 'added':
        fact_value = normalize1(normalize2(find_path(path_int, file2)))
        result_str += f"{dict_diff[value]}{fact_value}\n"
    return result_str


def plain(tree, file1, file2):

    def inner(tree, path='', result_str=''):
        for key, value in tree.items():
            path_int = f'{path}{key}'
            if isinstance(value, dict):
                result_str += inner(value, path=(path_int+'.'))
            if value in ('updated', 'added', 'removed'):
                result_str += plain_elem(value, file1, file2, path_int)
        path = ''
        return result_str
    return (inner(tree)).strip('\n')
