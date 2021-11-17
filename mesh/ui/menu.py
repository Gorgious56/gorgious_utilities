import bpy


def draw_new_mesh_objects(self, _):
    self.layout.operator("mesh.add_empty", text="Empty", icon="GHOST_ENABLED")
    self.layout.operator("mesh.add_single_vertex", text="Single Vertex", icon="DOT")


def draw_print_mesh_count(self, _):
    self.layout.operator("mesh.print_highest_verts_count")


menus_appends = {
    bpy.types.VIEW3D_MT_mesh_add: draw_new_mesh_objects,
    bpy.types.VIEW3D_MT_object_cleanup: draw_print_mesh_count,
}
menus_prepends = {}


def register():
    for menu, draw in menus_appends.items():
        menu.append(draw)
    for menu, draw in menus_prepends.items():
        menu.prepend(draw)


def unregister():
    for menu, draw in menus_appends.items():
        menu.remove(draw)
    for menu, draw in menus_prepends.items():
        menu.remove(draw)
