import bpy


class GU_OT_toggle_object_render(bpy.types.Operator):
    """Tooltip"""

    bl_idname = "object.toggle_render"
    bl_label = "Toggle Render"
    bl_options = {"UNDO"}
    visibility_settings = ("camera", "diffuse", "glossy", "transmission", "volume_scatter", "shadow")

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        toggle = context.active_object.hide_render
        for obj in context.selected_objects:
            obj.hide_render = not toggle
            for attr in self.visibility_settings:
                setattr(obj, "visible_" + attr, toggle)
            obj.display_type = "TEXTURED" if toggle else "WIRE"
        return {"FINISHED"}

