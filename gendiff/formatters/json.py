import json


def normalize_node(node, key_name):
    dictionary = {}
    key_type = node['type']
    file1_value = node.get('file1_value')
    file2_value = node.get('file2_value')
    if key_type in ('updated', 'removed'):
        dictionary[f'- {key_name}'] = file1_value
    if key_type in ('updated', 'added'):
        dictionary[f'+ {key_name}'] = file2_value
    if key_type == 'unchanged':
        dictionary[key_name] = file1_value
    return dictionary


def make_json_dict(diff_tree):

    def inner(diff_nodes):
        dictionary = {}
        for node in diff_nodes:
            key_name = node['key_name']
            key_type = node['type']
            if key_type == 'nested':
                dictionary[key_name] = inner(node['children'])
            else:
                dictionary.update(normalize_node(node, key_name))
        return dictionary
    return inner(diff_tree)


def format(diff_tree):
    return json.dumps(
        make_json_dict(diff_tree), indent=4)
