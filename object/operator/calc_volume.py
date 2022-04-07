import bpy
import bmesh


class GU_OT_object_calc_volume(bpy.types.Operator):
    bl_idname = "object.calc_volume"
    bl_label = "Calculate Volume"
    bl_options = {"UNDO"}

    @classmethod
    def poll(cls, context):
        return any(context.selected_objects) > 0

    def execute(self, context):
        depsgraph = context.evaluated_depsgraph_get()
        for ob in context.selected_objects:
            object_eval = ob.evaluated_get(depsgraph)
            try:
                mesh_eval = object_eval.to_mesh()
            except RuntimeError:
                continue
            else:
                bm = bmesh.new()
                bm.from_mesh(mesh_eval)
                volume = round(bm.calc_volume(signed=True), 2)
                ob["volume"] = volume
        return {"FINISHED"}
