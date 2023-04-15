from bpy.types import Operator
from bpy.props import StringProperty, IntProperty


class GU_OT_collection_property_operations(Operator):
    bl_idname = "gu.collection_property_operations"
    bl_label = ""
    collection_property_name: StringProperty()
    operation: StringProperty()
    index: IntProperty(default=-1)
    item_name: StringProperty()

    def execute(self, context):
        collection_property = getattr(context.collection_property_holder, self.collection_property_name)
        if self.operation == "ADD":
            new = collection_property.add()
            if self.item_name:
                new.name = self.item_name
            if hasattr(new, "on_add"):
                new.on_add()
        elif self.operation == "REMOVE":
            collection_property.remove(self.index)
        return {"FINISHED"}
