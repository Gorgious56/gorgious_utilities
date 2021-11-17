import bpy
from gorgious_utilities.collection.helper import (
    rename_children_and_self_objects,
)


class GU_OT_collection_rename_objects_as_me(bpy.types.Operator):
    """Rename each object in the collection as the collection name"""

    bl_idname = "collection.rename_objects_as_me"
    bl_label = "Rename each object in the collection as the collection name"
    bl_options = {"UNDO"}

    def execute(self, context):
        rename_children_and_self_objects(context.collection)
        return {"FINISHED"}
