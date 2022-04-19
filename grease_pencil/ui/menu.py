import bpy
from gorgious_utilities.core.ui.menu_factory import GU_Menu


def draw_hatches(self, _):
    layout = self.layout
    layout.operator("gpencil.generate_hatches", icon="TEXTURE_DATA")


def draw_reset_camera(self, context):
    if context.mode != 'PAINT_GPENCIL':
        return
    cam = context.scene.camera
    if not cam:
        return
    self.layout.operator("gpencil.reset_canvas_rotation", text="", icon="VIEW_CAMERA")
    self.layout.prop(cam, "rotation_euler", text="Rotation", index=1)


class GU_Menu_GP(GU_Menu):
    appends = {
        bpy.types.GPENCIL_MT_material_context_menu: draw_hatches,
        bpy.types.VIEW3D_MT_editor_menus: draw_reset_camera,
    }


def register():
    GU_Menu_GP.register()


def unregister():
    GU_Menu_GP.unregister()
