import bpy


class GU_PT_clean_scene(bpy.types.Panel):
    bl_label = "Cleaning"
    bl_idname = "GU_PT_clean_scene"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout

        layout.operator("clean.remove_fake_users")
        layout.operator("clean.remove_single_empties")


class GU_PT_clean_view_layer(bpy.types.Panel):
    bl_label = "Cleaning"
    bl_idname = "GU_PT_clean_view_layer"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "view_layer"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        layout.operator("clean.sort_view_layers")


class GU_PT_clean_scene_drivers(bpy.types.Panel):
    bl_label = "Drivers"
    bl_idname = "GU_PT_clean_scene_drivers"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"
    bl_parent_id = "GU_PT_clean_scene"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        layout.operator("clean.faulty_drivers", text="Clean")
        layout.operator("clean.update_drivers", text="Update")
