import bpy


def draw_gpu(self, context):
    if hasattr(context.scene, "GUProps"):
        self.layout.prop(context.scene.GUProps.gpu, "draw_mesh", toggle=True, icon="MOD_MESHDEFORM", text="")


def register():
    bpy.types.VIEW3D_HT_header.append(draw_gpu)


def unregister():
    bpy.types.VIEW3D_HT_header.remove(draw_gpu)
