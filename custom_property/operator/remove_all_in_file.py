import bpy


class GU_OT_property_remove_all_in_file(bpy.types.Operator):
    bl_idname = "property.remove_all_in_file"
    bl_label = "Remove ALL Custom Properties from the file"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        for attr in dir(bpy.data):
            if "bpy_prop_collection" in str(type(getattr(bpy.data, attr))):
                for obj in getattr(bpy.data, attr):
                    for custom_prop_name in list(obj.keys()):
                        del obj[custom_prop_name]
        return {"FINISHED"}


if __name__ == "__main__":
    bpy.utils.register_class(GU_OT_property_remove_all_in_file)
