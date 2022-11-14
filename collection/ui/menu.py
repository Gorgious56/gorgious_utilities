import bpy
from gorgious_utilities.collection.tool import (
    get_collection_layers_from_collections,
    get_collection_layer_from_collection,
    get_hierarchy,
)
from gorgious_utilities.core.ui.menu_factory import GU_Menu


def draw_boolean_collection_toggle(self, _):
    op = self.layout.operator("collection.toggle_objects_viewport", text="Toggle Booleans")
    op.col_name = "BOOL"


def draw_blueprint_collection_toggle(self, _):
    op = self.layout.operator("collection.toggle_objects_viewport", text="Toggle Blueprints")
    op.col_name = "BP_"


def draw_exclude_collections_from_object(self, context):
    layout = self.layout
    collection_layers = list(get_collection_layers_from_collections(
        context.view_layer.layer_collection, context.active_object.users_collection
    ))
    split = layout.split(align=True, factor=0.4)

    split.label(text="All Collections")
    state = not getattr(collection_layers[0], "exclude")
    op = split.operator("gu.collections_state_toggle", text="", icon="CHECKBOX_HLT" if state else "CHECKBOX_DEHLT")
    op.attribute = "exclude"
    op.state = state
    state = not getattr(collection_layers[0], "hide_viewport")
    op = split.operator("gu.collections_state_toggle", text="", icon="HIDE_OFF" if state else "HIDE_ON")
    op.attribute = "hide_viewport"
    op.state = state
    
    all_layers = set(collection_layers)
    for col_layer in collection_layers:
        all_layers.update([l_c for l_c in get_hierarchy(context.view_layer.layer_collection, col_layer)])

    for col_layer in collection_layers:
        hierarchy = [l_c for l_c in get_hierarchy(context.view_layer.layer_collection, col_layer)]
        tick = ""
        box = layout.box()
        for col_layer in reversed(hierarchy):
            split = box.split(align=True, factor=0.4)
            split.label(text=tick + col_layer.name)
            split.prop(col_layer, "exclude", text="")
            col_name = col_layer.collection.name
            col = bpy.data.collections.get(col_name)
            if col is None:
                continue
            split.prop(col, "hide_select", text="")
            split.prop(col_layer, "hide_viewport", text="")
            split.prop(col, "hide_viewport", text="")
            split.prop(col, "hide_render", text="")
            tick += "."


def draw_outliner_collection_context(self, context):
    layout = self.layout
    layout.separator()
    layout.operator("collection.rename_objects", text="Rename Objects")
    op = layout.operator("collection.move_selected_to_this", text="Move Selected Objects to Collection")
    op.unlink_others = True
    op = layout.operator("collection.move_selected_to_this", text="Add Selected Objects to Collection")
    op.unlink_others = False

    col = next(_id for _id in context.selected_ids if isinstance(_id, bpy.types.Collection))
    layer_col = get_collection_layer_from_collection(context.view_layer.layer_collection, col)
    if layer_col is None:
        return
    exclude = layer_col.exclude
    op = layout.operator(
        "collection.include_or_exclude_from_all_view_layers",
        text="Exclude Globally" if not exclude else "Include Globally",
    )
    op.col_name = col.name
    op.exclude = not exclude


class GU_Menu_Collection(GU_Menu):
    appends = {
        bpy.types.VIEW3D_MT_view: draw_boolean_collection_toggle,
        bpy.types.VIEW3D_MT_view: draw_blueprint_collection_toggle,
        bpy.types.OUTLINER_MT_collection: draw_outliner_collection_context,
        bpy.types.OBJECT_PT_collections: draw_exclude_collections_from_object,
    }


def register():
    GU_Menu_Collection.register()


def unregister():
    GU_Menu_Collection.unregister()
