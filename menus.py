import bpy.types
from .object_bl import (
    GU_OT_mesh_empty_add,
    GU_OT_mesh_single_vertex_add,
    GU_OT_copy_custom_props,
    GU_OT_material_init_custom_props,
    GU_OT_remove_custom_props,
    GU_OT_toggle_object_render,
)
from .mesh import (
    GU_OT_print_highest_mesh_count,
)
from .property import (
    GU_OT_property_copy,
)
from .modifier import (
    GU_OT_modifier_replace_a_with_b,
)


def draw_new_mesh_objects(self, _):
    self.layout.operator(GU_OT_mesh_empty_add.bl_idname, text="Empty", icon="GHOST_ENABLED")
    self.layout.operator(GU_OT_mesh_single_vertex_add.bl_idname, text="Single Vertex", icon="DOT")


def draw_custom_properties_ops(self, _):
    row = self.layout.row(align=True)
    row.operator(GU_OT_copy_custom_props.bl_idname, text="", icon="EYEDROPPER")
    row.operator(GU_OT_material_init_custom_props.bl_idname, text="", icon="MATERIAL").overwrite = False
    row.operator(GU_OT_material_init_custom_props.bl_idname, text="", icon="NODE_MATERIAL").overwrite = True
    row.operator(GU_OT_remove_custom_props.bl_idname, text="", icon="TRASH")


def draw_toggle_render_object_context(self, _):
    self.layout.operator(GU_OT_toggle_object_render.bl_idname, text="Toggle Render")


def draw_print_mesh_count(self, _):
    self.layout.operator(GU_OT_print_highest_mesh_count.bl_idname)


def draw_custom_props_links(self, _):
    self.layout.operator(GU_OT_material_init_custom_props.bl_idname, text="Copy Material Attributes")
    self.layout.operator(GU_OT_copy_custom_props.bl_idname, text="Copy Custom Properties")
    self.layout.operator(GU_OT_property_copy.bl_idname, text="Copy ANY Property")



def draw_modifiers_properties(self, _):
    self.layout.operator(GU_OT_modifier_replace_a_with_b.bl_idname, icon="NODETREE")


menus_appends = {
    bpy.types.VIEW3D_MT_make_links: draw_custom_props_links,
    bpy.types.VIEW3D_MT_object_context_menu: draw_toggle_render_object_context,
    bpy.types.VIEW3D_MT_mesh_add: draw_new_mesh_objects,
    bpy.types.VIEW3D_MT_object_cleanup: draw_print_mesh_count,
}
menus_prepends = {
    bpy.types.OBJECT_PT_custom_props: draw_custom_properties_ops,
    bpy.types.DATA_PT_modifiers: draw_modifiers_properties,
}


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
