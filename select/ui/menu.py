import bpy


def draw_select_used_booleans(self, context):
    self.layout.operator("select.used_booleans")


menus_appends = {
    bpy.types.VIEW3D_MT_select_object: draw_select_used_booleans,
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
