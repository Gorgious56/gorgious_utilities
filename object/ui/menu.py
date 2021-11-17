import bpy


def draw_toggle_render_object_context(self, _):
    self.layout.operator("object.toggle_render", text="Toggle Render")


menus_appends = {
    bpy.types.VIEW3D_MT_object_context_menu: draw_toggle_render_object_context,
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
