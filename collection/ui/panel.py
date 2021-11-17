import bpy
from gorgious_utilities.collection.operator import (
    duplicate_hierarchy_only,
)

class GU_PT_collection_properties_utilities(bpy.types.Panel):
    bl_label = "Utilities"
    bl_idname = "GU_PT_collection_properties_utilities"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "collection"

    def draw(self, context):
        layout = self.layout

        layout.operator(duplicate_hierarchy_only.GU_OT_collection_duplicate_hierarchy_only.bl_idname)