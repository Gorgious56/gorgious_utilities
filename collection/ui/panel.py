import bpy
from gorgious_utilities.collection.helper import (
    get_collection_layer_from_collection,
)


class GU_PT_collection_properties_utilities(bpy.types.Panel):
    bl_label = "Utilities"
    bl_idname = "GU_PT_collection_properties_utilities"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "collection"

    def draw(self, context):
        layout = self.layout

        layout.operator("collection.duplicate_hierarchy_only")

        col = context.collection
        layer_col = get_collection_layer_from_collection(context.view_layer, col)
        exclude = layer_col.exclude
        op = layout.operator(
            "collection.include_or_exclude_from_all_view_layers",
            text="Exclude Globally" if not exclude else "Include Globally",
        )
        op.col_name = col.name
        op.exclude = not exclude
