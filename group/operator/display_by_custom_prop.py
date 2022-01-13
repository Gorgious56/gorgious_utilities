from random import uniform, random, seed
import bpy
from bpy.types import Operator, Collection
from bpy.props import EnumProperty, StringProperty, PointerProperty


class GU_OT_display_by_custom_prop(Operator):
    bl_idname = "group.display_by_custom_prop"
    bl_label = "Display By Group"
    bl_options = {"UNDO", "REGISTER"}

    display_type: EnumProperty(
        name="Display On", items=(("color", "Object Color", "Change Object Color"),), default="color"
    )
    prop_name: StringProperty(name="Custom Property Name")

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        for obj in context.selected_objects:
            if self.prop_name in obj:
                seed(hash(obj[self.prop_name]))
                switch = random()
                if switch < 0.333:
                    r = uniform(0, 0.8)
                    g = uniform(r, 1)
                    b = 1 - g - r
                elif switch < 0.666:
                    g = uniform(0, 0.8)
                    b = uniform(g, 1)
                    r = 1 - g - b
                else:
                    b = uniform(0, 0.8)
                    r = uniform(b, 1)
                    g = 1 - r - b
                setattr(obj, self.display_type, (r, g, b, 1))
        return {"FINISHED"}
