import bpy

class GU_OT_select_used_objects(bpy.types.Operator):
    bl_idname = "gu.select_used_objects"
    bl_label = "Select Used Objects"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.active_object

    def execute(self, context):
        for obj in context.selected_objects:
            for mod in obj.modifiers:
                if hasattr(mod, "object") and mod.object is not None:
                    mod.object.select_set(True)
        return {"FINISHED"}
