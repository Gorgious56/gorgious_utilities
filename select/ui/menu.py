import bpy


def draw_select_used_booleans(self, context):
    self.layout.operator("select.used_booleans")


def draw_select_by_property(self, context):
    self.layout.operator("select.by_property")


menus_appends = {
    bpy.types.VIEW3D_MT_select_object: draw_select_used_booleans,
    bpy.types.VIEW3D_MT_select_object: draw_select_by_property,
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
