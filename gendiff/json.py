import json


def json_dict_elem(value, key, node1, node2):
    dictionary = {}
    if value == 'updated':
        dictionary[f'- {key}'] = node1[key]
        dictionary[f'+ {key}'] = node2[key]
    elif value == 'removed':
        dictionary[f'- {key}'] = node1[key]
    elif value == 'added':
        dictionary[f'+ {key}'] = node2[key]
    else:
        dictionary[key] = node1[key]
    return dictionary


def json_dict(tree, node1, node2):

    def inner(tree, node1, node2, dictionary={}):
        for key, value in tree.items():
            if isinstance(value, dict):
                dictionary[key] = inner(
                    value, node1[key], node2[key], dictionary={})
            else:
                dictionary.update(json_dict_elem(
                    value, key, node1, node2))
        return dictionary
    return inner(tree, node1, node2)


def json_(tree, file1, file2):
    return json.dumps(json_dict(tree, file1, file2), indent=4)
