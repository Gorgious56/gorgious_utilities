import bpy


class GU_PT_object_tools(bpy.types.Panel):
    bl_label = "Tools"
    bl_idname = "GU_PT_object_tools"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout

        layout.operator("object.calc_volume", icon="SNAP_VOLUME")
