import bpy


class GU_PT_clean_scene(bpy.types.Panel):
    bl_label = "Cleaning"
    bl_idname = "GU_PT_clean_scene"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.operator("clean.faulty_drivers")
        layout.operator("clean.update_drivers")
        layout.operator("clean.remove_fake_users")
        layout.operator("clean.remove_single_empties")
