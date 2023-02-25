import bpy
import bmesh

from gorgious_utilities.attribute.util import get_bmesh_domain


class GU_OT_attribute_set(bpy.types.Operator):
    bl_idname = "gu.attribute_set"
    bl_label = "Set attribute"
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

        if active_object.mode == "OBJECT":
            bm = bmesh.new()
            bm.from_mesh(active_object.data)
        else:
            bm = bmesh.from_edit_mesh(active_object.data)

        attribute = active_object.data.attributes[attribute_name]

        props = active_object.GUProps.attribute
        new_value = getattr(props, attribute.data_type)

        domain = get_bmesh_domain(bm, attribute.domain)
        first_attribute = attribute.data[0]
        for attr_name in ("value", "vector", "color"):
            if hasattr(first_attribute, attr_name):
                break
        else:
            return {"FINISHED"}

        existing_value = getattr(first_attribute, attr_name)
        if isinstance(existing_value, str):
            size = 1
        else:
            try:
                size = len(existing_value)
            except TypeError:
                size = 1

        values = [None] * len(domain) * size
        attribute.data.foreach_get(attr_name, values)
        for i, vef in enumerate(domain):
            if not vef.select:
                continue
            if size > 1:
                for s in range(size):
                    values[i * size + s] = new_value[s]
            else:
                values[i] = new_value
        attribute.data.foreach_set(attr_name, values)

        active_object.data.update()

        if not was_in_object_mode:
            bpy.ops.object.editmode_toggle()

        return {"FINISHED"}
