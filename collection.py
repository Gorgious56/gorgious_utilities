from collections import defaultdict
import bpy
from bpy.types import (
    Operator,
    Panel,
)


class GU_OT_collection_move_to_this(Operator):
    """Toggle Visibility of Boolean Collections"""

    bl_idname = "collection.move_selected_to_this"
    bl_label = "Move selected objects to this collection"
    bl_options = {"UNDO"}

    def execute(self, context):
        target_col = context.collection
        objs = set()
        objs.add(context.active_object)
        objs.update(context.selected_objects)
        for obj in (o for o in objs if o):
            already_linked = False
            for col in obj.users_collection:
                if col == target_col:
                    already_linked = True
                else:
                    col.objects.unlink(obj)
            if not already_linked:
                target_col.objects.link(obj)

        return {"FINISHED"}


class GU_OT_collection_replace_in_name(Operator):    
    bl_idname = "collection.replace_in_name"
    bl_label = "Replace in collection names"
    bl_options = {"REGISTER", "UNDO"}

    replace_from: bpy.props.StringProperty(name="Replace")
    replace_to: bpy.props.StringProperty(name="By")

    def invoke(self, context, event):
        self.replace_from = context.collection.name
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        if not self.replace_from:
            return {"FINISHED"}
        for col in context.selected_ids:
            if not isinstance(col, bpy.types.Collection):
                continue
            col.name = col.name.replace(self.replace_from, self.replace_to)
        return {"FINISHED"}


class GU_OT_collection_duplicate_hierarchy_only(Operator):
    bl_idname = "collection.duplicate_hierarchy_only"
    bl_label = "Duplicate Collection Hierarchy Only"
    bl_options = {"REGISTER", "UNDO"}
    replace_from: bpy.props.StringProperty(name="Replace")
    replace_to: bpy.props.StringProperty(name="By")

    @classmethod
    def poll(cls, context):
        return context.collection

    def invoke(self, context, event):
        self.replace_from = context.collection.name
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        tree, all_colls = get_tree(context.collection)

        new_colls = []
        for coll in all_colls:
            new_coll = bpy.data.collections.new(coll.name.replace(self.replace_from, self.replace_to))
            new_coll.color_tag = coll.color_tag
            new_colls.append(new_coll)

        for old_col_parent, old_cols in tree.items():
            for old_col in old_cols:
                child = new_colls[all_colls.index(old_col)]
                if old_col_parent is None:
                    parent = get_parent(old_col)
                    if parent is None:
                        parent = context.scene.collection
                else:
                    parent = new_colls[all_colls.index(old_col_parent)]
                parent.children.link(child)

        return {"FINISHED"}


class GU_OT_collection_toggle_object_visibility(Operator):
    """Toggle Visibility of Boolean Collections"""

    bl_idname = "collection.toggle_objects_viewport"
    bl_label = "Toggle Boolean Viewport Visibility"
    bl_options = {"UNDO"}

    col_name: bpy.props.StringProperty(name="Col Name", default="BOOL")

    def execute(self, context):
        cols = [c for c in bpy.data.collections if self.col_name.lower() in c.name.lower()]
        if cols:
            exclude = None
            layer_collections = get_all_children(context.view_layer.layer_collection)
            layer_collections_collections = [l_c.collection for l_c in layer_collections]
            for i, col in enumerate(cols):
                index = layer_collections_collections.index(col)
                if i == 0:
                    exclude = not layer_collections[index].exclude
                layer_collections[index].exclude = exclude

        return {"FINISHED"}


def get_collection_layer_from_collection(context, collection):
    layer_collections = get_all_children(context.view_layer.layer_collection)
    for col_layer in layer_collections:
        if col_layer.collection == collection:
            return col_layer


def get_collection_layers_from_collections(context, collections):
    layer_collections = get_all_children(context.view_layer.layer_collection)
    cols_ret = []
    for col_layer in layer_collections:
        if col_layer.collection in collections:
            cols_ret.append(col_layer)
    return cols_ret


def get_all_children(col):
    yield col
    for child in col.children:
        yield from get_all_children(child)


def get_parent(col):
    for c in bpy.data.collections:
        if col.name in c.children:
            return c
    return None

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


class GU_OT_destructively_join_meshes(Operator):
    """Destructively applies modifiers, converts curves and instances, removes boolean collections, and join meshes"""

    bl_idname = "collection.destructively_join_meshes"
    bl_label = "Destructively join meshes"
    bl_options = {"UNDO"}

    col_name: bpy.props.StringProperty(name="Col Name", default="BOOL")
    join_wire_objects: bpy.props.BoolProperty(name="Join Wire Objects", default=False)

    @classmethod
    def poll(cls, context):
        return context.selected_objects

    def execute(self, context):
        col_parent = context.collection
        bpy.ops.object.select_all(action="DESELECT")

        all_converted_objects = []
        remove_objs = []
        instances = []

        for obj in col_parent.all_objects:
            if obj.name not in context.view_layer.objects:
                continue
            if obj.type == "MESH":
                if not self.join_wire_objects and obj.display_type == "WIRE":
                    remove_objs.append(obj)
                    continue
                obj.select_set(True)
                all_converted_objects.append(obj)
                continue
            elif obj.type == "EMPTY" and obj.instance_type == "COLLECTION":
                instances.append(obj)
                continue
            elif obj.type == "CURVE":
                curve = obj.data
                if curve.bevel_depth > 0 or obj.modifiers:
                    obj.select_set(True)
                    all_converted_objects.append(obj)
                else:
                    remove_objs.append(obj)
            else:
                remove_objs.append(obj)

        context.view_layer.objects.active = context.selected_objects[0]
        bpy.ops.object.make_single_user(object=True, obdata=True, material=False, animation=False)
        bpy.ops.object.convert(target="MESH")
        bpy.ops.object.select_all(action="DESELECT")

        if instances:
            ctx = context.copy()
            ctx["object"] = instances[0]
            ctx["active_object"] = instances[0]
            ctx["selected_objects"] = instances
            ctx["selected_editable_objects"] = instances
            bpy.ops.object.duplicates_make_real(ctx)

        # Delete all Empty Objects
        while remove_objs:
            bpy.data.objects.remove(remove_objs.pop())
        while instances:
            bpy.data.objects.remove(instances.pop())

        all_child_collections = get_all_children(col_parent)

        for coll in all_child_collections:
            if coll == col_parent:
                continue
            if coll:
                if self.col_name.lower() in coll.name.lower():
                    obs = [o for o in coll.objects if o.users == 1]
                    while obs:
                        bpy.data.objects.remove(obs.pop())
                else:
                    obs = [o for o in coll.objects]
                    while obs:
                        col_parent.objects.link(obs.pop())

                bpy.data.collections.remove(coll)

        join_objects = [obj for obj in col_parent.all_objects if obj.type == "MESH"]

        if join_objects:
            ctx = context.copy()
            o = join_objects[0]
            ctx["object"] = o
            ctx["active_object"] = o
            ctx["selected_objects"] = join_objects
            ctx["selected_editable_objects"] = join_objects
            bpy.ops.object.join(ctx)

            o.name = col_parent.name

        return {"FINISHED"}


def rename_children_and_self_objects(col):
    if col is None:
        return
    for obj in col.objects:
        obj.name = col.name
        if hasattr(obj, "data") and obj.data is not None:
            obj.data.name = col.name
    for sub_col in col.children:
        rename_children_and_self_objects(sub_col)


class GU_OT_collection_rename_objects(Operator):
    """Rename each object in the collection as the collection name"""

    bl_idname = "collection.rename_objects_as_me"
    bl_label = "Rename each object in the collection as the collection name"
    bl_options = {"UNDO"}

    def execute(self, context):
        rename_children_and_self_objects(context.collection)
        return {"FINISHED"}


class GU_PT_collection_properties_utilities(Panel):
    bl_label = "Utilities"
    bl_idname = "GU_PT_collection_properties_utilities"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "collection"

    def draw(self, context):
        layout = self.layout

        layout.operator(GU_OT_collection_duplicate_hierarchy_only.bl_idname)