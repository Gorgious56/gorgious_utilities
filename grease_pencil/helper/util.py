import bpy
from gorgious_utilities.grease_pencil.helper.layer import clear_layers as tool_clear_layers
from gorgious_utilities.grease_pencil.helper.object import get_grease_pencil
from gorgious_utilities.grease_pencil.helper.material import get_or_create_gp_mat

def init_grease_pencil(
    context,
    gpencil_obj_name="GPencil",
    clear_layers=True,
    force_new=False,
) -> bpy.types.GPencilLayer:

    gpencil = get_grease_pencil(context, gpencil_obj_name, force_new)
    if "GU_Perspective_Lines" not in gpencil.data.materials:
        gpencil_mat = get_or_create_gp_mat("GU_Perspective_Lines")
        gpencil.data.materials.append(gpencil_mat)
    if clear_layers:
        tool_clear_layers(gpencil)
    return gpencil

