import bpy
from gorgious_utilities.camera.helper import reset_camera_rotation, reset_camera_view


class GU_OT_gpencil_reset_canvas_rotation(bpy.types.Operator):
    bl_idname = "gpencil.reset_canvas_rotation"
    bl_label = "Reset Rotation"

    def execute(self, context):
        reset_camera_rotation(context)
        reset_camera_view(context)
        return {"FINISHED"}
