import bpy
from bpy.types import Panel, NodesModifier


class GU_PT_modifier_properties(Panel):
    bl_label = "GN Inputs"
    bl_idname = "GU_PT_modifier_properties"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Item"

    @classmethod
    def poll(cls, context):
        return context.active_object and any(
            m for m in context.active_object.modifiers if isinstance(m, NodesModifier)
        )

    def draw(self, context):
        layout = self.layout
        props = context.active_object.GUProps.modifier.modifier_inputs
        for mod in context.active_object.modifiers:
            if not isinstance(mod, NodesModifier):
                continue
            props_mod = props.get(mod.name)
            box = layout.box()
            tree = mod.node_group
            if tree is None:
                continue
            row = box.row(align=True)
            row.prop(mod, "show_expanded", text="")
            row.prop(mod, "name", text="")
            op_show_all = row.operator(
                "gu.modifier_show_input_in_viewport", icon="HIDE_OFF", text=""
            )
            op_show_all.modifier_name = mod.name
            op_show_all.input_identifier = ""
            if not mod.show_expanded:
                continue
            col = box.column(align=True)
            for inp in tree.inputs:
                if inp.in_out != "INPUT":
                    continue
                if inp.identifier == "Socket_0":
                    continue  # First input is the source geometry. Don't show that
                row = col.row(align=True)
                input_id = inp.identifier
                if props_mod:
                    props_input = props_mod.inputs.get(inp.identifier)
                    if props_input is not None and not props_input.show:
                        continue
                input_use_attribute_path = input_id + "_use_attribute"
                if input_use_attribute_path in mod and mod[input_use_attribute_path]:
                    row.prop(mod, f'["{input_id}_attribute_name"]', text=inp.name)
                else:
                    row.prop(mod, f'["{input_id}"]', text=inp.name)
                if input_use_attribute_path in mod:
                    toggle_attribute = row.operator(
                        "object.geometry_nodes_input_attribute_toggle",
                        text="",
                        icon="SPREADSHEET",
                    )
                    toggle_attribute.input_name = input_id
                    toggle_attribute.modifier_name = mod.name
                op_show = row.operator(
                    "gu.modifier_show_input_in_viewport", icon="HIDE_ON", text=""
                )
                op_show.modifier_name = mod.name
                op_show.input_identifier = input_id
