import bpy
from gorgious_utilities.collection.helper import (
    get_family_down,
)



class GU_OT_collection_replace_in_name(bpy.types.Operator):    
    bl_idname = "collection.replace_in_name"
    bl_label = "Replace in collection names"
    bl_options = {"REGISTER", "UNDO"}

    replace_from: bpy.props.StringProperty(name="Replace")
    replace_to: bpy.props.StringProperty(name="With")
    max_occurences: bpy.props.IntProperty(name="Replace Occurences", default=1) 
    replace_children: bpy.props.BoolProperty(name="Replace in children", default=True)
    replace_objects: bpy.props.BoolProperty(name="Replace in objects", default=False)
    remove_trailing_numbers: bpy.props.BoolProperty(name="Remove trailing numbers", default=True)

    def invoke(self, context, event):
        self.replace_from = self.replace_to = context.collection.name
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        if not self.replace_from:
            return {"FINISHED"}
        cols = set()
        if hasattr(context, "selected_ids"):
            selected_cols = (_id for _id in context.selected_ids if isinstance(_id, bpy.types.Collection))
        else:
            selected_cols = (context.collection, )
        for col in selected_cols:
            if not isinstance(col, bpy.types.Collection):
                continue          
            cols.add(col)
            if self.replace_children:
                cols.update(get_family_down(col))
        for col in cols:
            col.name = col.name.replace(self.replace_from, self.replace_to, self.max_occurences)

        if self.replace_objects:
            objs = set()
            for col in selected_cols:
                objs.update(col.all_objects)
            for obj in objs:
                obj.name = obj.name.replace(self.replace_from, self.replace_to, self.max_occurences)

        if self.remove_trailing_numbers:
            bpy.ops.collection.rename_objects(remove_trailing_numbers=True)
        return {"FINISHED"}

