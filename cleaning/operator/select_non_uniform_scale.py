import bpy


class GU_OT_select_non_uniform_scale(bpy.types.Operator):
    bl_idname = "gu.select_non_uniform_scale"
    bl_label = "Select Objects with Non-Uniform Scale"
    bl_options = {"UNDO"}

    def execute(self, context):
        eps = 10e-5
        def is_uniform_scale(scale):
            return all(abs(axis - 1) < eps for axis in scale)
        if context.selected_objects:
            for obj in context.selected_objects:
                obj.select_set(not is_uniform_scale(obj.scale))
        else:
            for obj in context.selectable_objects:
                if not is_uniform_scale(obj.scale):
                    obj.select_set(True)
        return {"FINISHED"}
