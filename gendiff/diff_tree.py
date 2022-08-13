def build(node1, node2):
    tree = []
    all_keys = sorted(list(set(node1.keys()) | set(node2.keys())))
    common_keys = set(node1.keys()) & set(node2.keys())
    removed_keys = set(node1.keys()) - common_keys
    added_keys = set(node2.keys()) - common_keys
    for key in all_keys:
        if key in removed_keys:
            tree.append({'key_name': key,
                         'type': 'removed',
                         'file1_value': node1[key]})
            continue
        if key in added_keys:
            tree.append({'key_name': key,
                         'type': 'added',
                         'file2_value': node2[key]})
            continue
        if isinstance(node1[key], dict) and isinstance(node2[key], dict):
            children = build(node1[key], node2[key])
            tree.append({'key_name': key,
                         'type': 'nested',
                         'children': children})
            continue
        elif node1[key] == node2[key]:
            tree.append({'key_name': key,
                         'type': 'unchanged',
                         'file1_value': node1[key]})
        else:
            tree.append({'key_name': key,
                         'type': 'updated',
                         'file1_value': node1[key],
                         'file2_value': node2[key]})
    return tree
