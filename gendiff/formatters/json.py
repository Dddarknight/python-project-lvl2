import json


def convert_elem_to_required(diff_node, key):
    dictionary = {}
    key_type = diff_node[key]['type']
    old_value = diff_node[key]['old_value']
    new_value = diff_node[key]['new_value']
    if key_type in ('updated', 'removed'):
        dictionary[f'- {key}'] = old_value
    if key_type in ('updated', 'added'):
        dictionary[f'+ {key}'] = new_value
    if key_type == 'unchanged':
        dictionary[key] = new_value
    return dictionary


def make_json_dict(diff_tree):

    def inner(diff_node, dictionary={}):
        for key in diff_node.keys():
            key_type = diff_node[key]['type']
            if key_type == 'nested':
                dictionary[key] = make_json_dict(diff_node[key]['children'])
            else:
                dictionary.update(convert_elem_to_required(diff_node, key))
        return dictionary
    return inner(diff_tree)


def modify(diff_tree):
    return json.dumps(
        make_json_dict(diff_tree), indent=4)
