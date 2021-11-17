import bpy


class GU_OT_remove_single_empties(bpy.types.Operator):
    """Remove empties with no parenting hierarchy attached"""

    bl_idname = "clean.remove_single_empties"
    bl_label = "Remove Single Empties"
    bl_options = {"UNDO"}

    def execute(self, context):
        empties = [o for o in bpy.data.objects if o.type == "EMPTY" and o.parent is None]
        for o in bpy.data.objects:
            if o.parent in empties:
                empties.remove(o.parent)

        bpy.ops.object.select_all(action="DESELECT")
        [e.select_set(True) for e in empties]
        bpy.ops.object.delete()
        return {"FINISHED"}
