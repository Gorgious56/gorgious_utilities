import bpy
from gorgious_utilities.core.menu import GU_Menu


def draw_custom_render(self, _):
    layout = self.layout
    layout.operator("cameras.render_selected", icon="CAMERA_DATA")


class GU_Menu_Camera(GU_Menu):
    appends = {
        bpy.types.TOPBAR_MT_render: draw_custom_render,
    }


def register():
    GU_Menu_Camera.register()


def unregister():
    GU_Menu_Camera.unregister()
