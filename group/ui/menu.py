import bpy


def draw_group_ops(self, _):
    layout = self.layout
    layout.operator("group.by_custom_prop", text="Group by Custom Prop", icon="GROUP")
    layout.operator("group.copy_to_selected", text="Copy Group to Selected", icon="EYEDROPPER")    
    layout.operator("group.display_by_custom_prop", text="Display by Custom Prop", icon="COLLECTION_COLOR_01")

menus_appends = {
    bpy.types.VIEW3D_MT_object_relations: draw_group_ops,
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
