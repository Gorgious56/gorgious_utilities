import bpy

from .tool import delaunay


class GU_OT_mesh_delaunay(bpy.types.Operator):
    bl_idname = "gu.mesh_delaunay"
    bl_label = "Make Delaunay Triangulation"
    bl_options = {"REGISTER", "UNDO"}
    bl_description = "Creates a Delaunay triangulation of selected mesh vertices"

    def execute(self, context):
        delaunay(context.active_object)
        return {"FINISHED"}
