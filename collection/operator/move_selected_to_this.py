import bpy


class GU_OT_collection_move_selected_to_this(bpy.types.Operator):
    """Toggle Visibility of Boolean Collections"""

    bl_idname = "collection.move_selected_to_this"
    bl_label = "Move selected objects to this collection"
    bl_options = {"UNDO"}
    unlink_others: bpy.props.BoolProperty(default=True)

    def execute(self, context):
        target_col = context.collection
        objs = set()
        objs.add(context.active_object)
        objs.update(context.selected_objects)
        for obj in (o for o in objs if o):
            already_linked = False
            for col in obj.users_collection:
                if col == target_col:
                    already_linked = True
                else:
                    if self.unlink_others:
                        col.objects.unlink(obj)
            if not already_linked:
                target_col.objects.link(obj)

        return {"FINISHED"}
