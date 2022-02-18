import bpy


def draw_modifiers_properties(self, context):
    layout = self.layout
    row = layout.row(align=True)
    row.operator("modifier.replace_gn_a_with_gn_b", icon="NODETREE")
    row.operator("modifier.replace_output_name", icon="GROUP_VCOL")

    row = layout.row(align=True)
    sub_row = row.row(align=True)
    op = sub_row.operator("object.make_links_data", text="Copy", icon="PASTEDOWN")
    op.type = "MODIFIERS"
    sub_row.operator("modifier.drive", icon="DECORATE_DRIVER")
    sub_row.operator("modifier.sync", text="Synch", icon="UV_SYNC_SELECT")
    sub_row.enabled = bool(len(context.view_layer.objects.selected) > 1 and context.active_object)
    row.operator("modifier.desync", text="Desynch", icon="UNLINKED")


def draw_select_used_booleans(self, context):
    self.layout.operator("modifier.select_used_booleans")


menus_appends = {
    bpy.types.VIEW3D_MT_select_object: draw_select_used_booleans,
}
menus_prepends = {
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
