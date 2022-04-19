import bpy
from math import cos, sin, radians
from gorgious_utilities.grease_pencil.helper.util import init_grease_pencil
from gorgious_utilities.grease_pencil.helper.layer import get_grease_pencil_layer
from gorgious_utilities.grease_pencil.helper.draw import draw_line


_LAYERS = (
    ("50", "5 Degrees", ""),
    ("10", "1 Degree", ""),
    ("1", "0.1 Degrees", ""),
)


class GU_OT_gpencil_create_perspective_lines(bpy.types.Operator):
    bl_idname = "gpencil.create_perspective_lines"
    bl_label = "Create Perspective Lines"
    bl_options = {"REGISTER", "UNDO"}

    increments: bpy.props.EnumProperty(
        name="Layers",
        items=_LAYERS,
        options={"ENUM_FLAG"},
        default={"50", "10"},
    )

    def execute(self, context):
        gpencil = init_grease_pencil(context, "GU_Perspective_Lines")
        for increment, layer_name, _ in _LAYERS:
            gp_layer = get_grease_pencil_layer(gpencil, layer_name, clear_layer=True)
            gp_frame = gp_layer.frames.new(0)

            gp_layer.hide = increment not in self.increments

            increment = int(increment)
            for a in range(0, 3600, increment):
                draw_line(gp_frame, (0, 0), (cos(radians(a / 10)) * 5000, sin(radians(a / 10)) * 5000), width=20)


        return {"FINISHED"}
