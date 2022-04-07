import bpy


def draw_custom_render(self, _):
    layout = self.layout
    layout.operator("cameras.render_selected", icon="CAMERA_DATA")


menus_appends = {
    bpy.types.TOPBAR_MT_render: draw_custom_render,
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
