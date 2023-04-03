import bpy


class GU_OT_select_and_set_active(bpy.types.Operator):
    bl_idname = "gu.select_and_set_active"
    bl_label = "Select By Property"
    object_name: bpy.props.StringProperty()

    def execute(self, context):
        previous_object = context.active_object
        previous_object.select_set(False)
        active_object = bpy.data.objects.get(self.object_name)
        context.view_layer.objects.active = active_object
        active_object.select_set(True)

        return {"FINISHED"}
