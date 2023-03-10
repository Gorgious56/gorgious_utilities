from bpy.types import Panel
import gorgious_utilities.core.ui.collection_property


class GU_PT_scene_lod(Panel):
    bl_label = "LOD baking"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        props = context.active_object.GUProps.lod

        box = layout.box()
        box.label(text="LODs")
        gorgious_utilities.core.ui.collection_property.draw(box, props.target_lods)

        box.operator("gu.lod_remesh", text="Create LODs")

        row = layout.row(align=True)
        row.prop(props, "image_size")
        row.label(text=f"{props.pixel_size}*{props.pixel_size} pixels")

        box.operator("gu.bake_batch", text="Bake LODs")
