import bpy
from gorgious_utilities.core.menu import GU_Menu


def draw_new_mesh_objects(self, _):
    self.layout.operator("mesh.add_empty", text="Empty", icon="GHOST_ENABLED")
    self.layout.operator("mesh.add_single_vertex", text="Single Vertex", icon="DOT")


def draw_print_mesh_count(self, _):
    self.layout.operator("mesh.print_highest_verts_count")


class GU_Menu_Mesh(GU_Menu):
    appends = {
        bpy.types.VIEW3D_MT_mesh_add: draw_new_mesh_objects,
        bpy.types.VIEW3D_MT_object_cleanup: draw_print_mesh_count,
    }


def register():
    GU_Menu_Mesh.register()


def unregister():
    GU_Menu_Mesh.unregister()
