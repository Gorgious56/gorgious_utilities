import bpy
from gorgious_utilities.custom_property.helper import (
    retrieve_props,
    copy_custom_prop,
)

class GU_OT_property_copy(bpy.types.Operator):
    """Copy Property"""

    bl_idname = "property.copy_any"
    bl_label = "Copy Any Property from active to selected"
    bl_settings = {"INTERNAL"}
    bl_options = {"UNDO", "REGISTER"}

    prop_copy: bpy.props.EnumProperty(
        name="Copy Property",
        description="Choose which property to copy from active to selected.\n Silently passes if target object doesn't have property",
        items=retrieve_props,
    )

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and len(context.selected_objects) > 0

    def invoke(self, context, event):
        # Reset prop to prevent random mishaps :
        self.prop_copy = retrieve_props.no_copy
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        if self.prop_copy == retrieve_props.no_copy:
            return {"FINISHED"}
        ao = context.active_object
        if self.prop_copy in ao.keys():
            for obj in context.selected_objects:
                if ao == obj:
                    continue
                copy_custom_prop(ao, obj, self.prop_copy)
        else:
            value = getattr(ao, self.prop_copy, None)
            for obj in context.selected_objects:
                if ao == obj:
                    continue
                try:
                    setattr(obj, self.prop_copy, value)
                except TypeError as e:
                    # Edge case : Only empties can have an instance_type of 'COLLECTION'
                    print(f"Could not copy property from {ao.name} to {obj.name}\n{e}")
                except AttributeError as e:
                    # For some reason some properties are readonly despite is_readonly being False
                    print(f"Could not copy property from {ao.name} to {obj.name}\n{e}")

        return {"FINISHED"}
