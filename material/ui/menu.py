import bpy


def draw_custom_props_links(self, _):
    self.layout.operator("material.init_custom_properties", text="Copy Material Attributes")


menus_appends = {
    bpy.types.VIEW3D_MT_make_links: draw_custom_props_links,
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
