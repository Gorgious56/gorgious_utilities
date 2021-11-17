import bpy
from gorgious_utilities.collection.helper import (
    get_all_children,
)



class GU_OT_collection_replace_in_name(bpy.types.Operator):    
    bl_idname = "collection.replace_in_name"
    bl_label = "Replace in collection names"
    bl_options = {"REGISTER", "UNDO"}

    replace_from: bpy.props.StringProperty(name="Replace")
    replace_to: bpy.props.StringProperty(name="By")
    replace_children: bpy.props.BoolProperty(name="Replace in children", default=True)

    def invoke(self, context, event):
        self.replace_from = context.collection.name
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        if not self.replace_from:
            return {"FINISHED"}
        cols = set()

        for col in context.selected_ids:
            if not isinstance(col, bpy.types.Collection):
                continue          
            cols.add(col)  
            if self.replace_children:
                cols.update(get_all_children(col))
        for col in cols:
            col.name = col.name.replace(self.replace_from, self.replace_to)
        return {"FINISHED"}

