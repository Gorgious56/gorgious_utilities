import bpy
from bpy.props import StringProperty


class GU_OT_modifier_show_input_in_viewport(bpy.types.Operator):
    bl_idname = "gu.modifier_show_input_in_viewport"
    bl_label = "Show Modifier Input in Viewort"
    bl_options = {"REGISTER", "UNDO"}

    modifier_name: StringProperty()
    input_identifier: StringProperty(default="")

    def execute(self, context):
        props = context.active_object.GUProps.modifier.modifier_inputs
        props_mod = props.get(self.modifier_name)
        if not props_mod:
            props_mod = props.add()
            props_mod.name = self.modifier_name
        if self.input_identifier:
            inp = props_mod.inputs.get(self.input_identifier)
            if not inp:
                inp = props_mod.inputs.add()
                inp.name = self.input_identifier
            inp.show = False
        else:
            for inp in props_mod.inputs:
                inp.show = True

        self.remove_unused(context, props)

        return {"FINISHED"}

    def remove_unused(self, context, props):
        mod_names = [mod.name for mod in context.active_object.modifiers if mod.type == "NODES"]
        for i in range(len(props) - 1, -1, -1):
            if props[i].name not in mod_names:
                props.remove(i)
