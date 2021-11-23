import bpy
from rna_prop_ui import PropertyPanel
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

        oc = layout.operator_context
        layout.operator_context = "INVOKE_DEFAULT"
        layout.operator(
            "collection.duplicate_hierarchy_only", text="Duplicate Hierarchy", icon="OUTLINER_OB_GROUP_INSTANCE"
        )
        layout.operator_context = oc

        col = context.collection
        layer_col = get_collection_layer_from_collection(context.view_layer, col)
        excluded = layer_col.exclude
        op = layout.operator(
            "collection.include_or_exclude_from_all_view_layers",
            text=("Include" if excluded else "Exclude") + " Globally",
            icon="CHECKBOX_HLT" if not excluded else "CHECKBOX_DEHLT",
        )
        op.col_name = col.name
        op.exclude = not excluded

        grid = layout.grid_flow(columns=2, align=True)
        grid.label(text="Delete objects", icon="TRASH")
        grid.label(text="")
        op = grid.operator("collection.delete_objects", text="Recursively", icon="OUTLINER_OB_GROUP_INSTANCE")
        op.recursive = True
        grid.operator("collection.delete_objects", text="Collection", icon="OUTLINER_COLLECTION").recursive = False

        grid = layout.grid_flow(columns=2, align=True)
        grid.label(text="Rename", icon="SORTALPHA")
        grid.label(text="")
        op = grid.operator("collection.rename_objects", text="Objects", icon="OBJECT_DATAMODE")      
        oc = grid.operator_context
        grid.operator_context = "INVOKE_DEFAULT"
        grid.operator("collection.replace_in_name", text="Collection", icon="OUTLINER_COLLECTION")
        grid.operator_context = oc

        layout.operator("collection.destructively_join_meshes", text="Destructively Join Meshes")


class GU_PT_collection_custom_properties(bpy.types.Panel, PropertyPanel): 
    _context_path = "collection"
    _property_type = bpy.types.Collection
    bl_label = "Custom Properties"
    bl_idname = "GU_PT_collection_custom_properties"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "collection"
