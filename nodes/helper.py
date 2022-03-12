def get_active_node_tree(context):
    node_area = context.area if context.area.type == "NODE_EDITOR" else None
    if node_area is None:
        return
    return node_area.spaces[0].edit_tree


def get_node_types(_, context):
    node_types = set()
    for node in get_active_node_tree(context).nodes:
        node_types.add(node.type)
    node_types = list(node_types)
    node_types.sort()
    return [(node_type,) * 3 for node_type in node_types]
