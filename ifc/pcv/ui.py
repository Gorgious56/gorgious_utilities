from bpy.types import Panel

try:
    from blenderbim.bim.ifc import IfcStore
except:
    pass
finally:

    class GU_PT_IFC_PCV(Panel):
        bl_label = "Point Cloud"
        # bl_idname = "BIM_PT_class"
        bl_space_type = "PROPERTIES"
        bl_region_type = "WINDOW"
        bl_context = "object"
        bl_parent_id = "BIM_PT_object_metadata"

        @classmethod
        def poll(cls, context):
            if not context.active_object:
                return False
            return IfcStore.get_file()

        def draw(self, context):
            layout = self.layout
            layout.operator("ifc.pcv_update_settings")
