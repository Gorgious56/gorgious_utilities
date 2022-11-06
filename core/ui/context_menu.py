import bpy


def register():
    if hasattr(bpy.types, "UI_MT_button_context_menu"):
        pass


def unregister():
    if hasattr(bpy.types, "UI_MT_button_context_menu"):
        pass
