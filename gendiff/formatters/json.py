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


def make_json_dict(diff_tree, file1_node, file2_node):

    def inner(diff_tree, file1_node, file2_node, dictionary={}):
        for key in diff_tree.keys():
            key_type = diff_tree[key]['type']
            if key_type == 'nested':
                dictionary[key] = make_json_dict(diff_tree[key]['children'],
                                                 file1_node[key],
                                                 file2_node[key])
            else:
                dictionary.update(convert_elem_to_required(
                    key, key_type, file1_node, file2_node))
        return dictionary
    return inner(diff_tree, file1_node, file2_node)


def modify(diff_tree, file1_dict, file2_dict):
    return json.dumps(
        make_json_dict(diff_tree, file1_dict, file2_dict), indent=4)
