import json


def convert_elem_to_required(key, value, node1, node2):
    dictionary = {}
    if value in ('updated', 'removed'):
        dictionary[f'- {key}'] = node1[key]
    if value in ('updated', 'added'):
        dictionary[f'+ {key}'] = node2[key]
    if value == 'unchanged':
        dictionary[key] = node1[key]
    return dictionary


def make_json_dict(tree, node1, node2):

    def inner(tree, node1, node2, dictionary={}):
        for key in sorted(tree.keys()):
            value = tree[key]
            if isinstance(value, dict):
                dictionary[key] = inner(
                    value, node1[key], node2[key], dictionary={})
            else:
                dictionary.update(convert_elem_to_required(
                    key, value, node1, node2))
        return dictionary
    return inner(tree, node1, node2)


def make_json(tree, file1, file2):
    return json.dumps(make_json_dict(tree, file1, file2), indent=4)
