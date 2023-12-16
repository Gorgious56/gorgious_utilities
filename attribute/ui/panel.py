import bmesh
from bpy.types import Panel
from gorgious_utilities.attribute.operator.attribute_viewer import node_group_name


class GU_PT_attribute_properties(Panel):
    bl_label = "Attribute"
    bl_idname = "GU_PT_attribute_properties"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Item"

    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.type == "MESH"

    def draw(self, context):
        layout = self.layout
        active_object = context.active_object
        if not active_object.mode == "EDIT":
            layout.label(text="Please Go Into Edit Mode", icon="INFO")
            return
        attributes = active_object.data.attributes
        if attributes:
            props = active_object.GUProps.attribute
            active_attribute = props.active_attribute
            mesh_select_mode = context.scene.tool_settings.mesh_select_mode
            if not active_attribute:
                layout.label(text="No Active Attribute", icon="INFO")
            layout.template_list(
                "ATTRIBUTE_UL_gu_display",
                "",
                active_object.data,
                "attributes",
                props,
                "active_attribute_index",
            )
            if (
                (active_attribute.domain == "POINT" and mesh_select_mode[0])
                or (active_attribute.domain == "EDGE" and mesh_select_mode[1])
                or (active_attribute.domain == "FACE" and mesh_select_mode[2])
            ):
                bm = bmesh.from_edit_mesh(active_object.data)
                if bm.select_history.active is None:
                    layout.label(text="No Active Mesh Item", icon="INFO")
                    return

                row = layout.row(align=True)
                row.prop(
                    props,
                    active_attribute.data_type,
                    text=active_attribute.data_type.title(),
                )
                row.enabled = context.active_object.mode == "EDIT"

                op = row.operator("gu.attribute_set", icon="CHECKMARK", text="")
                op = row.operator("gu.attribute_copy", icon="COPYDOWN", text="")
                op = row.operator("gu.attribute_paste", icon="PASTEDOWN", text="")

                row = layout.row(align=True)
                if any(
                    m
                    for m in active_object.modifiers
                    if m.name == node_group_name and m.type == "NODES"
                ):
                    icon = "MODIFIER_OFF"
                else:
                    icon = "MODIFIER_ON"
                op = row.operator("gu.attribute_viewer", icon=icon, text="")
                op.attribute_name = active_attribute.name
                op = row.operator("gu.attribute_viewer", icon="VIEWZOOM", text="")
                op.attribute_name = active_attribute.name
                op.update = True
            else:
                self.layout.label(text="No Attribute in this mode", icon="INFO")
