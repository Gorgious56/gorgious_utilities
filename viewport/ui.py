import bpy


def draw_menu_appends(self, context):
    self.layout.operator("gu.viewport_setup_overlays")


def register():
    bpy.types.VIEW3D_PT_shading.append(draw_menu_appends)


def unregister():
    bpy.types.VIEW3D_PT_shading.remove(draw_menu_appends)
