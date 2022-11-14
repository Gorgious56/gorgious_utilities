import bpy


def draw_object_context_menu_appends(self, context):
    layout = self.layout
    active_obj = context.active_object
    if active_obj:
        layout.separator()

        op = layout.operator("gu.collections_state_toggle", text="Hide All Collections", icon="HIDE_OFF")
        op.state = True
        op.attribute = "hide_viewport"


def register():
    if hasattr(bpy.types, "UI_MT_button_context_menu"):
        pass
    bpy.types.VIEW3D_MT_object_context_menu.append(draw_object_context_menu_appends)


def unregister():
    if hasattr(bpy.types, "UI_MT_button_context_menu"):
        pass
    bpy.types.VIEW3D_MT_object_context_menu.remove(draw_object_context_menu_appends)
