import bpy


class GU_OT_mesh_empty_add(bpy.types.Operator):
    """Add a mesh object with no geometry"""

    bl_idname = "mesh.add_empty"
    bl_label = "Empty"
    bl_options = {"REGISTER", "UNDO"}

    use_cursor_location: bpy.props.BoolProperty(name="Instance at Cursor Location", default=True)

    def execute(self, context):
        obj = bpy.data.objects.new(name="Empty Mesh", object_data=bpy.data.meshes.new(name="Empty Mesh"))
        context.collection.objects.link(obj)
        bpy.ops.object.select_all(action="DESELECT")
        context.view_layer.objects.active = obj
        obj.select_set(True)
        if self.use_cursor_location:
            obj.location = context.scene.cursor.location
        return {"FINISHED"}
