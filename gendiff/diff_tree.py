def make(node1, node2):
    tree = {}
    common_keys = set(node1.keys()) & set(node2.keys())
    removed = set(node1.keys()) - common_keys
    added = set(node2.keys()) - common_keys
    tree.update({key: {'type': 'removed',
                       'children': {},
                       'old_value': node1[key],
                       'new_value': ''} for key in removed})
    tree.update({key: {'type': 'added',
                       'children': {},
                       'old_value': '',
                       'new_value': node2[key]} for key in added})
    for key in common_keys:
        if isinstance(node1[key], dict) and isinstance(node2[key], dict):
            children = make(node1[key], node2[key])
            tree.update({key: {'type': 'nested',
                               'children': children,
                               'old_value': 'not defined',
                               'new_value': 'not defined'}})
            continue
        if node1[key] == node2[key]:
            tree.update({key: {'type': 'unchanged',
                               'children': {},
                               'old_value': node1[key],
                               'new_value': node2[key]}})
        else:
            tree.update({key: {'type': 'updated',
                               'children': {},
                               'old_value': node1[key],
                               'new_value': node2[key]}})
    tree = {key: value for key, value in sorted(tree.items())}
    return tree
