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
    for col_layer in layer_collections:
        if col_layer.collection in collections:
            yield col_layer


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


def copy_collection_attributes(view_layers, col_from, col_to):
    for attr in dir(col_from):
        if attr == "name":
            continue
        try:
            setattr(col_to, attr, getattr(col_from, attr))
        except AttributeError:
            continue
    for v_l in view_layers:
        layer_col_from, layer_col_to = get_collection_layers_from_collections(v_l, (col_from, col_to))
        for attr in dir(layer_col_from):
            try:
                setattr(layer_col_to, attr, getattr(layer_col_from, attr))
            except AttributeError:
                continue
