from collections import defaultdict
import bpy


def get_parent(col):
    for c in bpy.data.collections:
        if col.name in c.children:
            return c
    return None


def get_all_children(col):
    yield col
    for child in col.children:
        yield from get_all_children(child)


def get_collection_layer_from_collection(view_layer, collection):
    layer_collections = get_all_children(view_layer.layer_collection)
    for col_layer in layer_collections:
        if col_layer.collection == collection:
            return col_layer


def get_collection_layers_from_collections(view_layer, collections):
    layer_collections = get_all_children(view_layer.layer_collection)
    cols_ret = []
    for col_layer in layer_collections:
        if col_layer.collection in collections:
            cols_ret.append(col_layer)
    return cols_ret


def get_tree(col):
    tree = defaultdict(set)
    all_cols = []

    def get_children_tree(tree, _col, parent=None):
        tree[parent].add(_col)
        all_cols.append(_col)
        for child in _col.children:
            get_children_tree(tree, child, _col)

    get_children_tree(tree, col)
    return tree, all_cols


def rename_children_and_self_objects(col):
    if col is None:
        return
    for obj in col.objects:
        obj.name = col.name
        if hasattr(obj, "data") and obj.data is not None:
            obj.data.name = col.name
    for sub_col in col.children:
        rename_children_and_self_objects(sub_col)
