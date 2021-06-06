from queue import PriorityQueue
import bpy
from bpy.types import (
    Operator,
)


class GU_OT_print_highest_mesh_count(Operator):
    """Destructively applies modifiers, converts curves and instances, removes boolean collections, and join meshes"""

    bl_idname = "mesh.print_highest_mesh_count"
    bl_label = "Print Mesh Count"
    bl_options = {"UNDO"}

    def execute(self, context):
        verts = PriorityQueue()
        depsgraph = bpy.context.evaluated_depsgraph_get()
        for obj in bpy.data.objects:
            if obj and obj.type == "MESH":
                verts.put((len(obj.evaluated_get(depsgraph).data.vertices), len(obj.data.vertices), obj.name))
        while not verts.empty():
            print(verts.get())
        return {"FINISHED"}
