import bpy


def draw_custom_properties_ops(self, _):
    row = self.layout.row(align=True)
    row.operator("property.copy_any", text="", icon="EYEDROPPER")
    row.operator("material.init_custom_properties", text="", icon="MATERIAL").overwrite = False
    row.operator("material.init_custom_properties", text="", icon="NODE_MATERIAL").overwrite = True
    row.operator("object.remove_all_custom_props", text="", icon="TRASH")

def draw_custom_props_links(self, _):
    self.layout.operator("property.copy_all", text="Copy Custom Properties")
    self.layout.operator("property.copy_any", text="Copy ANY Property")

menus_appends = {
    bpy.types.OBJECT_PT_custom_props: draw_custom_properties_ops,
    bpy.types.VIEW3D_MT_make_links: draw_custom_props_links,
}
menus_prepends = {
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