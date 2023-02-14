import bpy


class GU_OT_collection_remove_selected_from_this(bpy.types.Operator):
    bl_idname = "gu.collection_remove_selected_from_this"
    bl_label = "Remove selected objects from this collection"
    bl_options = {"UNDO"}
    collection: bpy.props.StringProperty(default="")

    def execute(self, context):
        target_col = context.collection if self.collection == "" else bpy.data.collections[self.collection]
        objs = set()
        objs.add(context.active_object)
        objs.update(context.selected_objects)
        for obj in (o for o in objs if o):
            if obj.name not in target_col.objects:
                continue
            target_col.objects.unlink(obj)
        self.collection = ""
        return {"FINISHED"}
