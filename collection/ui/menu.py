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
    collection_layers = list(
        get_collection_layers_from_collections(
            context.view_layer.layer_collection, context.active_object.users_collection
        )
    )
    draw_all_collections_toggle(layout, collection_layers, context)

    collection_layers = set(collection_layers)
    hierarchies = {}

    for col_layer in collection_layers:
        hierarchies[col_layer] = [l_c for l_c in get_hierarchy(context.view_layer.layer_collection, col_layer)]
    
    for col_layer in collection_layers:
        for col_layer_test, hierarchy in hierarchies.copy().items():
            if col_layer_test == col_layer:
                continue
            if col_layer in hierarchy:
                try:
                    del hierarchies[col_layer]
                except KeyError:
                    pass

    for col_layer in collection_layers:
        if col_layer not in hierarchies.keys():
            continue
        hierarchy = hierarchies[col_layer]
        tick = ""
        box = layout.box()
        column = box.column(align=True)
        for col_layer in reversed(hierarchy):
            split = column.split(align=True, factor=0.5)
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
            tick += " "

            add_to_collection = split.operator("gu.collection_move_selected_to_this", text="", icon="ADD")
            add_to_collection.collection = col_layer.collection.name
            add_to_collection.unlink_others = False

            row = split.row(align=True)
            remove_from_collection = row.operator("gu.collection_remove_selected_from_this", text="", icon="REMOVE")
            remove_from_collection.collection = col_layer.collection.name
            row.enabled = context.active_object.name in col_layer.collection.objects

            select_objects = split.operator("gu.collection_select_all_objects", text="", icon="OBJECT_DATA")
            select_objects.collection = col_layer.collection.name


def draw_all_collections_toggle(layout, col_layers, context):
    split = layout.split(align=True, factor=0.4)

    split.label(text="All Collections")
    state = not getattr(col_layers[0], "exclude")
    op = split.operator("gu.collections_state_toggle", text="", icon="CHECKBOX_HLT" if state else "CHECKBOX_DEHLT")
    op.attribute = "exclude"
    op.state = state
    op.mode = "layer"

    state = not getattr(context.active_object.users_collection[0], "hide_select")
    op = split.operator(
        "gu.collections_state_toggle", text="", icon="RESTRICT_SELECT_OFF" if state else "RESTRICT_SELECT_ON"
    )
    op.attribute = "hide_select"
    op.state = state
    op.mode = "col"

    state = not getattr(col_layers[0], "hide_viewport")
    op = split.operator("gu.collections_state_toggle", text="", icon="HIDE_OFF" if state else "HIDE_ON")
    op.attribute = "hide_viewport"
    op.state = state
    op.mode = "layer"

    state = not getattr(context.active_object.users_collection[0], "hide_viewport")
    op = split.operator(
        "gu.collections_state_toggle", text="", icon="RESTRICT_VIEW_OFF" if state else "RESTRICT_VIEW_ON"
    )
    op.attribute = "hide_viewport"
    op.state = state
    op.mode = "col"

    state = not getattr(context.active_object.users_collection[0], "hide_render")
    op = split.operator(
        "gu.collections_state_toggle", text="", icon="RESTRICT_RENDER_OFF" if state else "RESTRICT_RENDER_ON"
    )
    op.attribute = "hide_render"
    op.state = state
    op.mode = "col"

def draw_outliner_collection_context(self, context):
    layout = self.layout
    layout.separator()
    layout.operator("collection.rename_objects", text="Rename Objects")
    op = layout.operator("gu.collection_move_selected_to_this", text="Move Selected Objects to Collection")
    op.unlink_others = True
    op = layout.operator("gu.collection_move_selected_to_this", text="Add Selected Objects to Collection")
    op.unlink_others = False
    op = layout.operator("gu.collection_remove_selected_from_this", text="Remove Selected Objects from Collection")

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
