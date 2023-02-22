import bpy


class GU_OT_collection_select_all_objects(bpy.types.Operator):
    bl_idname = "gu.collection_select_all_objects"
    bl_label = "Select all objects linked in this collection"
    bl_options = {"UNDO"}
    collection: bpy.props.StringProperty(default="")

    def execute(self, context):
        target_col = context.collection if self.collection == "" else bpy.data.collections[self.collection]
        for obj in target_col.all_objects:
            obj.select_set(True)
        return {"FINISHED"}
