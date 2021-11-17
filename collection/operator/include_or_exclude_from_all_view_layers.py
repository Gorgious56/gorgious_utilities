import bpy
from gorgious_utilities.collection.helper import (
    get_collection_layer_from_collection,
)



class GU_OT_collection_include_or_exclude_from_all_view_layers(bpy.types.Operator):
    bl_idname = "collection.include_or_exclude_from_all_view_layers"
    bl_label = "Include or Exclude from all view layers"
    bl_options = {"UNDO"}
    col_name: bpy.props.StringProperty()
    exclude: bpy.props.BoolProperty()

    def execute(self, context):
        col = bpy.data.collections.get(self.col_name)
        if col is not None:
            for view_layer in context.scene.view_layers:
                layer_col = get_collection_layer_from_collection(view_layer, col)
                layer_col.exclude = self.exclude

        return {"FINISHED"}
