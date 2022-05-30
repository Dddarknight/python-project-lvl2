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


def plain_elem(value, node1, node2, key, path, dict_diff):
    result_str = ''
    if value == 'only_first':
        result_str = f"Property '{path}{key}'{dict_diff[value]}\n"
    elif value == 'changed':
        fact_value = normalize1(normalize2(node2[key]))
        old_value = normalize1(normalize2(node1[key]))
        result_str = f"Property '{path}{key}'" + (
            f"{dict_diff[value]}{old_value} to {fact_value}\n")
    elif value == 'only_second':
        fact_value = normalize1(normalize2(node2[key]))
        result_str = f"Property '{path}{key}'" + (
            f"{dict_diff[value]}{fact_value}\n")
    return result_str


def plain(tree, node1, node2):
    dict_diff = {'changed': ' was updated. From ',
                 'only_first': ' was removed',
                 'only_second': ' was added with value: '}

    def inner(tree, node1, node2, path='', result_str=''):
        for key, value in tree.items():
            if isinstance(value, dict):
                path_int = f'{path}{key}.'
                result_str += inner(
                    value, node1[key], node2[key], path=path_int)
            else:
                if value == 'unchanged':
                    continue
                else:
                    result_str += plain_elem(
                        value, node1, node2, key, path, dict_diff)
        path = ''
        return result_str
    return (inner(tree, node1, node2)).strip('\n')
