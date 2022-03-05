import bpy


def draw_custom_props_links(self, _):
    self.layout.operator("material.init_custom_properties", text="Copy Material Attributes")


def draw_update_viewport_material(self, _):
    self.layout.operator(
        "material.set_viewport_color_to_main_color", text="Update Viewport Color", icon="NODE_MATERIAL"
    )


menus_appends = {
    bpy.types.VIEW3D_MT_make_links: draw_custom_props_links,
    bpy.types.MATERIAL_MT_context_menu: draw_update_viewport_material,
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
