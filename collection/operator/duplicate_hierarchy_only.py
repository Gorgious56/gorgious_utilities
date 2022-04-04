import bpy
from gorgious_utilities.collection.helper import (
    get_tree,
    get_parent,
    copy_collection_attributes,
    copy_layer_collection_attributes,
)

class GU_OT_collection_duplicate_hierarchy_only(bpy.types.Operator):
    bl_idname = "collection.duplicate_hierarchy_only"
    bl_label = "Duplicate Collection Hierarchy Only"
    bl_options = {"REGISTER", "UNDO"}
    replace_from: bpy.props.StringProperty(name="Replace")
    replace_to: bpy.props.StringProperty(name="By")

    @classmethod
    def poll(cls, context):
        return context.collection

    def invoke(self, context, event):
        self.replace_from = context.collection.name
        self.replace_to = context.collection.name
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        tree, all_colls = get_tree(context.collection)

        new_colls = []
        for coll in all_colls:
            new_coll = bpy.data.collections.new("")
            new_colls.append(new_coll)
            copy_collection_attributes(coll, new_coll)
            if self.replace_from != self.replace_to:
                new_coll.name = coll.name.replace(self.replace_from, self.replace_to)

        for old_col_parent, old_cols in tree.items():
            for old_col in old_cols:
                child = new_colls[all_colls.index(old_col)]
                if old_col_parent is None:
                    parent = get_parent(old_col)
                    if parent is None:
                        parent = context.scene.collection
                else:
                    parent = new_colls[all_colls.index(old_col_parent)]
                parent.children.link(child)
        
        # for i in range(len(all_colls)):
        #     coll = all_colls[i]
        #     new_coll = new_colls[i]
        #     copy_layer_collection_attributes(context.scene.view_layers, coll, new_coll)
        #     if self.replace_from != self.replace_to:
        #         new_coll.name = coll.name.replace(self.replace_from, self.replace_to)


        return {"FINISHED"}
