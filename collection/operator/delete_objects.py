import bpy


class GU_OT_collection_delete_objects(bpy.types.Operator):
    """Deletes all objects"""

    bl_idname = "collection.delete_objects"
    bl_label = "Delete All Objects"
    bl_options = {"UNDO", "REGISTER"}
    recursive: bpy.props.BoolProperty(default=True)

    def execute(self, context):
        if hasattr(context, "selected_ids"):
            cols = (_id for _id in context.selected_ids if isinstance(_id, bpy.types.Collection))
        else:
            cols = (context.collection, )
        for col in cols:
            if self.recursive:
                bpy.data.batch_remove(col.all_objects)
            else:
                bpy.data.batch_remove(col.objects)

        return {"FINISHED"}
