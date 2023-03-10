from bpy.types import Operator
from bpy.props import StringProperty, IntProperty


class GU_OT_collection_property_operations(Operator):
    bl_idname = "gu.collection_property_operations"
    bl_label = ""
    collection_property_name: StringProperty()
    operation: StringProperty()
    index: IntProperty(default=-1)

    def execute(self, context):
        collection_property = getattr(context.collection_property_holder, self.collection_property_name)
        if self.operation == "ADD":
            collection_property.add()
        else:
            collection_property.remove(self.index)
        return {"FINISHED"}
