import bpy


class GU_OT_attribute_copy(bpy.types.Operator):
    bl_idname = "gu.attribute_copy"
    bl_label = "copy attribute from active to selected"
    bl_options = {"UNDO", "REGISTER"}
    mode: bpy.props.BoolVectorProperty()
    attribute_name: bpy.props.StringProperty()

    def execute(self, context):
        attribute_name = (
            context.active_object.data.attributes.active.name if self.attribute_name is None else self.attribute_name
        )
        bpy.ops.gu.attribute_sample(mode=self.mode, attribute_name=attribute_name)
        bpy.ops.gu.attribute_set(mode=self.mode, attribute_name=attribute_name)

        return {"FINISHED"}
