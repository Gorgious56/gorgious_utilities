import bpy
import bmesh


class GU_OT_attribute_get(bpy.types.Operator):
    bl_idname = "gu.attribute_sample"
    bl_label = "Sample attribute"
    bl_options = {"UNDO", "REGISTER"}
    mode: bpy.props.BoolVectorProperty()
    attribute_name: bpy.props.StringProperty()

    def execute(self, context):
        active_object = context.active_object
        attribute_name = (
            active_object.data.attributes.active.name if self.attribute_name is None else self.attribute_name
        )
        was_in_object_mode = active_object.mode == "OBJECT"
        if not was_in_object_mode:
            bpy.ops.object.editmode_toggle()

        bm = bmesh.new()
        bm.from_mesh(active_object.data)
        attribute = active_object.data.attributes[attribute_name]

        props = active_object.GUProps.attribute
        first_attribute = attribute.data[0]
        for attr_name in ("value", "vector", "color"):
            if hasattr(first_attribute, attr_name):
                break
        else:
            return {"FINISHED"}

        selected = bm.select_history.active
        value = getattr(attribute.data[selected.index], attr_name)
        setattr(props, attribute.data_type, value)

        if not was_in_object_mode:
            bpy.ops.object.editmode_toggle()

        return {"FINISHED"}
