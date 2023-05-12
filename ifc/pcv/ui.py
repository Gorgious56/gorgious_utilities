from bpy.types import Panel

try:
    from blenderbim.bim.ifc import IfcStore
    import blenderbim.bim.helper
except:
    pass
finally:

    class GU_PT_IFC_PCV(Panel):
        bl_label = "Point Cloud Visualizer"
        bl_space_type = "PROPERTIES"
        bl_region_type = "WINDOW"
        bl_context = "object"
        bl_parent_id = "BIM_PT_object_metadata"

        @classmethod
        def poll(cls, context):
            if not context.active_object:
                return False
            return IfcStore.get_file() and blenderbim.bim.helper.get_obj_ifc_definition_id(
                context, context.active_object.name, "Object"
            )

        def draw(self, context):
            layout = self.layout
            row = layout.row(align=True)
            row.operator("ifc.pcv_store_settings", icon="IMPORT")
            row.operator("ifc.pcv_update_settings", icon="EXPORT")
