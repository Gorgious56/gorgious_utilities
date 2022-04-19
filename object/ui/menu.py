import bpy
from gorgious_utilities.core.ui.menu_factory import GU_Menu


def draw_toggle_render_object_context(self, _):
    self.layout.operator("object.toggle_render", text="Toggle Render")


class GU_Menu_Object(GU_Menu):
    appends = {
        bpy.types.VIEW3D_MT_object_context_menu: draw_toggle_render_object_context,
    }


def register():
    GU_Menu_Object.register()


def unregister():
    GU_Menu_Object.unregister()
