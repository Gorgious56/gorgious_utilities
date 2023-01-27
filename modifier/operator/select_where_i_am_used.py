import bpy

class GU_OT_select_where_i_am_used(bpy.types.Operator):
    bl_idname = "gu.select_where_i_am_used"
    bl_label = "Select Where I Am Used"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.active_object

    def execute(self, context):
        ao = context.active_object
        for obj in context.selectable_objects:
            for mod in obj.modifiers:
                if hasattr(mod, "object") and mod.object == ao:
                    obj.select_set(True)
        return {"FINISHED"}
