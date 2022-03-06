import bpy
from gorgious_utilities.custom_property.helper import retrieve_props


class GU_OT_select_by_property(bpy.types.Operator):
    bl_idname = "select.by_property"
    bl_label = "Select By Property"

    prop_name: bpy.props.EnumProperty(
        name="Property Name",
        items=retrieve_props,
    )

    @classmethod
    def poll(cls, context):
        return context.active_object

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        if self.prop_name != retrieve_props.no_copy:
            prop_value = getattr(context.active_object, self.prop_name)
            for obj in context.selectable_objects:
                if obj == context.active_object:
                    continue
                obj.select_set(getattr(obj, self.prop_name) == prop_value)

        return {"FINISHED"}
