import bpy
from gorgious_utilities.attribute.operator.attribute_viewer import node_group_name


class GU_PT_attribute_properties(bpy.types.Panel):
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
            if any(m for m in active_object.modifiers if m.name == node_group_name and m.type == "NODES"):
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


# def update_attribute(fields, context, data_type, value_name):
#     obj = context.object
#     mesh = obj.data
#     value = getattr(fields, data_type)
#     attribute = context.attribute
#     if value_name == "value":
#         attribute.data.foreach_set(value_name, [value for _ in range(len(attribute.data))])
#     else:
#         values = [value for _ in range(len(attribute.data))]
#         attribute.data.foreach_set(value_name, [value for vector in values for value in vector])
#     mesh.update()


# class AttributeSetField(bpy.types.PropertyGroup):
#     FLOAT: bpy.props.FloatProperty(update=lambda self, context: update_attribute(self, context, "FLOAT", "value"))
#     INT: bpy.props.IntProperty(update=lambda self, context: update_attribute(self, context, "INT", "value"))
#     FLOAT_VECTOR: bpy.props.FloatVectorProperty(
#         update=lambda self, context: update_attribute(self, context, "FLOAT_VECTOR", "vector")
#     )
#     FLOAT_COLOR: bpy.props.FloatVectorProperty(
#         subtype="COLOR",
#         size=4,
#         min=0,
#         soft_max=1,
#         update=lambda self, context: update_attribute(self, context, "FLOAT_COLOR", "color"),
#     )


# class GU_PT_attribute_set(bpy.types.Panel):
#     bl_label = "Attribute Set"
#     bl_space_type = "PROPERTIES"
#     bl_region_type = "WINDOW"
#     bl_context = "data"

#     def draw(self, context):
#         layout = self.layout
#         if context.object.type != "MESH" or context.object.mode != "OBJECT":
#             layout.label(text="Please select a MESH object in OBJECT mode", icon="ERROR")
#             return
#         attribute = context.object.data.attributes.active
#         row = layout.row(align=True)
#         row.label(text=attribute.name)
#         row.context_pointer_set("attribute", attribute)
#         row.prop(context.scene.my_attribute_set_field, attribute.data_type, text="")


# def attribute_changed(*args):
#     print("The active attribute has changed!")



# def register():
#     # bpy.utils.register_class(AttributeSetField)
#     # bpy.utils.register_class(GU_PT_attribute_set)
#     bpy.types.Scene.my_attribute_set_field = bpy.props.PointerProperty(type=AttributeSetField)


