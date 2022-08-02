import json


def convert_elem_to_required(key, key_type, node1, node2):
    dictionary = {}
    if key_type in ('updated', 'removed'):
        dictionary[f'- {key}'] = node1[key]
    if key_type in ('updated', 'added'):
        dictionary[f'+ {key}'] = node2[key]
    if key_type == 'unchanged':
        dictionary[key] = node1[key]
    return dictionary


def make_json_dict(diff_tree, node1, node2):

    def inner(diff_tree, node1, node2, dictionary={}):
        for key in diff_tree.keys():
            key_type = diff_tree[key]['type']
            if key_type == 'nested':
                dictionary[key] = make_json_dict(diff_tree[key]['children'],
                                                 node1[key],
                                                 node2[key])
            else:
                dictionary.update(convert_elem_to_required(
                    key, key_type, node1, node2))
        return dictionary
    return inner(diff_tree, node1, node2)


def modify(diff_tree, file1_dict, file2_dict):
    return json.dumps(
        make_json_dict(diff_tree, file1_dict, file2_dict), indent=4)
