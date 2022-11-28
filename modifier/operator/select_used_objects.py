import bpy

class GU_OT_select_used_objects(bpy.types.Operator):
    bl_idname = "gu.select_used_objects"
    bl_label = "Select Used Objects"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.active_object

    def execute(self, context):
        traversed_objects = set()
        def select_used_objects(obj):
            if obj in traversed_objects:
                return
            traversed_objects.add(obj)
            obj.select_set(True)
            for mod in obj.modifiers:
                if hasattr(mod, "object") and mod.object is not None:
                    select_used_objects(mod.object)

        for obj in context.selected_objects:
            select_used_objects(obj)
        return {"FINISHED"}
