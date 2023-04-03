import bpy
from bpy.types import Panel


class GU_PT_scene_lod(Panel):
    bl_label = "LOD Baking"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        props = context.active_object.GUProps.lod
        props.draw(layout)


class GU_PT_object_lod_settings(Panel):
    bl_label = "LOD override settings"
    bl_options = {"INSTANCED"}
    bl_space_type = "VIEW_3D"
    bl_region_type = "WINDOW"

    def draw(self, context):
        context.lod.object.GUProps.lod.draw_lod_settings(self.layout)
