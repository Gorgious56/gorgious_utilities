import bpy
from gorgious_utilities.cleaning.helper import (
    retrieve_data_to_clear,
)


class GU_OT_remove_fake_users(bpy.types.Operator):
    """Remove 'use fake user' properties from selected data containers"""

    bl_idname = "clean.remove_fake_users"
    bl_label = "Remove Fake Users"
    bl_options = {"UNDO"}

    data_to_clear: bpy.props.EnumProperty(
        name="Data to Clear",
        description="Choose which data container to clear all fake users",
        items=retrieve_data_to_clear,)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        cols_to_clear = []
        if self.data_to_clear == retrieve_data_to_clear.all:
            for d in dir(bpy.data):
                if "bpy_prop_collection" in str(type(getattr(bpy.data, d))):
                    cols_to_clear.append(d)
        else:
            cols_to_clear.append(self.data_to_clear)
        for col in cols_to_clear:
            for e in getattr(bpy.data, col):
                if hasattr(e, "use_fake_user"):
                    e.use_fake_user = False
        return {"FINISHED"}
