import bpy


class GU_PT_grease_pencil(bpy.types.Panel):
    bl_label = "Convert"
    bl_idname = "GU_PT_grease_pencil"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"

    @classmethod
    def poll(cls, context):
        return context.active_object.type == "GPENCIL"

    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)
        mesh_convert = row.operator("grease_pencil.convert", text="Convert", icon="MESH_DATA")
        mesh_convert.mode = "MESH"
        curve_convert = row.operator("grease_pencil.convert", text="Convert", icon="CURVE_DATA")
        curve_convert.mode = "CURVE"
