import bpy
from bpy.types import Panel


class GU_PT_attribute_properties(Panel):
    bl_label = "Attribute"
    bl_idname = "GU_PT_attribute_properties"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Item"

    @classmethod
    def poll(cls, context):
        return (
            context.active_object
            and context.active_object.data
            and any(a for a in context.active_object.data.attributes if not a.name.startswith("."))
        )

    def draw(self, context):
        if context.active_object.data.attributes:
            self.layout.template_list(
                "MESH_UL_attributes",
                "attributes",
                context.active_object.data,
                "attributes",
                context.active_object.data.attributes,
                "active_index",
                rows=3,
            )
        if context.active_object.data.attributes.active:
            draw_attribute_set(self, context)


def draw_attribute_set(self, context):
    active_object = context.active_object
    if not active_object:
        return
    attribute = active_object.data.attributes.active
    if not attribute:
        return
    layout = self.layout
    # https://blender.stackexchange.com/a/40319/86891
    mesh_select_mode = context.scene.tool_settings.mesh_select_mode  # (Bool(Vertex), Bool(Edge), Bool(Face))
    props = active_object.GUProps.attribute

    row = layout.row(align=True)
    row.prop(props, attribute.data_type, text=attribute.data_type.title())
    op = row.operator("gu.attribute_set", icon="CHECKMARK", text="")
    op.mode = mesh_select_mode
    op.attribute_name = attribute.name
    op = row.operator("gu.attribute_copy", icon="COPYDOWN", text="")
    op.mode = mesh_select_mode
    op.attribute_name = attribute.name
    op = row.operator("gu.attribute_sample", icon="EYEDROPPER", text="")
    op.mode = mesh_select_mode
    op.attribute_name = attribute.name


def register():
    bpy.types.DATA_PT_mesh_attributes.append(draw_attribute_set)


def unregister():
    bpy.types.DATA_PT_mesh_attributes.remove(draw_attribute_set)
