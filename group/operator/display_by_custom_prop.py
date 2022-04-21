from collections import defaultdict
import numpy as np
from mathutils import Color
from bpy.types import Operator
from bpy.props import EnumProperty, StringProperty


class GU_OT_display_by_custom_prop(Operator):
    bl_idname = "group.display_by_custom_prop"
    bl_label = "Display By Group"
    bl_options = {"UNDO", "REGISTER"}

    display_type: EnumProperty(
        name="Display On",
        items=(("color", "Object Color", "Change Object Color"),),
        default="color",
    )
    prop_name: StringProperty(name="Custom Property Name")

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        groups = defaultdict(list)
        for obj in context.selected_objects:
            if self.prop_name not in obj:
                continue
            groups[obj[self.prop_name]].append(obj)
        hsv_base = Color((1, 0, 0))
        for objects, hue in zip(groups.values(), np.linspace(0, 1, len(groups.keys()) + 1)):
            hsv = hsv_base.copy()
            hsv.h = hue
            for obj in objects:
                setattr(obj, self.display_type, (hsv.r, hsv.g, hsv.b, 1))
        return {"FINISHED"}
