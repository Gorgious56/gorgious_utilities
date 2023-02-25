import bpy


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
    attribute_set = row.operator("gu.attribute_set", icon="CHECKMARK", text="")
    attribute_set.mode = mesh_select_mode


def register():
    bpy.types.DATA_PT_mesh_attributes.append(draw_attribute_set)


def unregister():
    bpy.types.DATA_PT_mesh_attributes.remove(draw_attribute_set)
