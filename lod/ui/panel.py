import bpy
from bpy.types import Panel
import gorgious_utilities.core.property.collection.ui.draw_generic


class GU_PT_scene_lod(Panel):
    bl_label = "LOD Baking"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        props = context.active_object.GUProps.lod

        box = layout.box()
        box.label(text="LODs")
        row = box.row(align=True)
        row.operator("gu.lod_remesh", text="Create LODs", icon="MOD_REMESH")
        row.operator("gu.bake_batch", text="Bake LODs", icon="TEXTURE")
        gorgious_utilities.core.property.collection.ui.draw_generic.draw(box, props.target_lods)

        props.draw(layout)


class GU_PT_object_lod_settings(Panel):
    bl_label = "LOD override settings"
    bl_options = {"INSTANCED"}
    bl_space_type = "VIEW_3D"
    bl_region_type = "WINDOW"

    def draw(self, context):
        context.lod.object.GUProps.lod.draw_lod_settings(self.layout)
