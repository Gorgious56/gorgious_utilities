import bpy
from collections import defaultdict
from gorgious_utilities.collection.tool import get_collection_layers_from_collections, get_family_down
from gorgious_utilities.custom_property.helper import copy_struct


class GU_OT_view_layers_sort(bpy.types.Operator):
    bl_idname = "view_layers.sort"
    bl_label = "Sort View Layers"
    bl_options = {"UNDO"}
    TEMP_NAME = "__TEMPORARY_VIEW_LAYER__"

    def execute(self, context):
        active_view_layer_name = context.window.view_layer.name
        view_layers = context.scene.view_layers
        names_sorted = sorted((v_l.name for v_l in view_layers), key=lambda n: n.lower())
        l_c_mapping = defaultdict(dict)
        for view_layer in view_layers:
            layer_cols = set(
                get_collection_layers_from_collections(
                    view_layer.layer_collection, list(get_family_down(context.scene.collection))
                )
            )
            for lc in layer_cols:
                l_c_mapping[view_layer.name][lc.name] = lc.exclude

        for v_l in context.scene.view_layers:
            v_l.name = v_l.name + self.TEMP_NAME
        for v_l_name in names_sorted:
            new = context.scene.view_layers.new(v_l_name)
            context.window.view_layer = new
            states = l_c_mapping[v_l_name]
            layer_cols = get_collection_layers_from_collections(
                new.layer_collection, list(get_family_down(context.scene.collection))
            )
            for l_c in layer_cols:
                l_c.exclude = states[l_c.name]
            copy_struct(context.scene.view_layers[v_l_name + self.TEMP_NAME], new, ignore=["name", "original"])
        for v_l_name in names_sorted:
            context.scene.view_layers.remove(context.scene.view_layers[v_l_name + self.TEMP_NAME])
        context.window.view_layer = context.scene.view_layers[active_view_layer_name]
        return {"FINISHED"}


if __name__ == "__main__":
    bpy.utils.register_class(GU_OT_clean_sort_view_layers)
