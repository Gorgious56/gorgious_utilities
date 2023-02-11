import bpy


def draw_gpu(self, context):
    if not context.active_object:
        return
    if context.active_object.mode == "EDIT":
        self.layout.prop(
            context.active_object.GUProps.gpu, "draw_mesh_edit_mode", toggle=True, icon="MOD_MESHDEFORM", text=""
        )
    if context.active_object.mode == "OBJECT":
        self.layout.prop(
            context.active_object.GUProps.gpu, "draw_mesh_object_mode", toggle=True, icon="MOD_MESHDEFORM", text=""
        )


def register():
    bpy.types.VIEW3D_HT_header.append(draw_gpu)


def unregister():
    bpy.types.VIEW3D_HT_header.remove(draw_gpu)
