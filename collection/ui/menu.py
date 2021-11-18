import bpy
from gorgious_utilities.collection.helper import (
    get_collection_layers_from_collections,
    get_collection_layer_from_collection,
)


def draw_boolean_collection_toggle(self, _):
    op = self.layout.operator("collection.toggle_objects_viewport", text="Toggle Booleans")
    op.col_name = "BOOL"


def draw_blueprint_collection_toggle(self, _):
    op = self.layout.operator("collection.toggle_objects_viewport", text="Toggle Blueprints")
    op.col_name = "BP_"


def draw_exclude_collections_from_object(self, context):
    layout = self.layout
    for col_layer in get_collection_layers_from_collections(context.view_layer, context.active_object.users_collection):
        split = layout.split(align=True, factor=0.4)
        split.label(text=col_layer.name)
        split.prop(col_layer, "exclude", text="")
        col_name = col_layer.collection.name
        col = bpy.data.collections[col_name]
        split.prop(col, "hide_select", text="")
        split.prop(col_layer, "hide_viewport", text="")
        split.prop(col, "hide_viewport", text="")
        split.prop(col, "hide_render", text="")


def draw_outliner_collection_context(self, context):
    layout = self.layout
    layout.separator()
    layout.operator("collection.rename_objects_as_me", text="Rename Objects")
    layout.operator("collection.move_selected_to_this", text="Move Selected Objects to this Collection")

    col = next(_id for _id in context.selected_ids if isinstance(_id, bpy.types.Collection))
    layer_col = get_collection_layer_from_collection(context.view_layer, col)
    exclude = layer_col.exclude
    op = layout.operator(
        "collection.include_or_exclude_from_all_view_layers",
        text="Exclude Globally" if not exclude else "Include Globally",
    )
    op.col_name = col.name
    op.exclude = not exclude

    oc = layout.operator_context
    layout.operator_context = "INVOKE_DEFAULT"
    layout.operator("collection.duplicate_hierarchy_only", text="Duplicate Hierarchy")
    layout.operator("collection.replace_in_name", text="Replace names")
    layout.operator_context = oc

    op = layout.operator("collection.delete_objects", text="Delete Objects Recursively").recursive = True
    op = layout.operator("collection.delete_objects", text="Delete Objects In Collection").recursive = False

    layout.operator("collection.destructively_join_meshes", text="Destructively Join Meshes")


menus_appends = {
    bpy.types.VIEW3D_MT_view: draw_boolean_collection_toggle,
    bpy.types.VIEW3D_MT_view: draw_blueprint_collection_toggle,
    bpy.types.OUTLINER_MT_collection: draw_outliner_collection_context,
    bpy.types.OBJECT_PT_collections: draw_exclude_collections_from_object,
}
menus_prepends = {}


def register():
    for menu, draw in menus_appends.items():
        menu.append(draw)
    for menu, draw in menus_prepends.items():
        menu.prepend(draw)


def unregister():
    for menu, draw in menus_appends.items():
        menu.remove(draw)
    for menu, draw in menus_prepends.items():
        menu.remove(draw)
