import bpy


def get_grease_pencil(context, gpencil_obj_name="GPencil", force_new=False) -> bpy.types.GreasePencil:
    gpencil = context.scene.objects.get(gpencil_obj_name)
    if not gpencil or force_new:
        bpy.ops.object.gpencil_add(align="WORLD", location=(0, 0, 0), type="EMPTY")
        gpencil = context.active_object
        gpencil.name = gpencil_obj_name

    return gpencil
