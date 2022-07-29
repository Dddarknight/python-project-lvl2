def make(node1, node2):
    tree = {}
    common_keys = set(node1.keys()) & set(node2.keys())
    removed = set(node1.keys()) - common_keys
    added = set(node2.keys()) - common_keys
    tree.update({key: 'removed' for key in removed})
    tree.update({key: 'added' for key in added})
    for key in common_keys:
        if isinstance(node1[key], dict) and isinstance(node2[key], dict):
            tree[key] = make(node1[key], node2[key])
            continue
        tree[key] = 'unchanged' if node1[key] == node2[key] else 'updated'
    return tree
