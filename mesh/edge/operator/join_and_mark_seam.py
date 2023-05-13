import bpy
from bpy.types import Macro


class GU_OT_mesh_edge_join_and_mark_sharp(Macro):
    bl_idname = "gu.mesh_edge_join_and_mark_sharp"
    bl_label = "Join and Mark Sharp"


def register():
    try:
        bpy.utils.register_class(GU_OT_mesh_edge_join_and_mark_sharp)
    except ValueError:
        pass
    GU_OT_mesh_edge_join_and_mark_sharp.define("mesh.vert_connect_path")
    GU_OT_mesh_edge_join_and_mark_sharp.define("mesh.mark_sharp")
