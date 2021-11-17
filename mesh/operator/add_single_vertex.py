import bpy


class GU_OT_mesh_add_single_vertex(bpy.types.Operator):
    """Add a mesh object with a single vertex at origin"""

    bl_idname = "mesh.add_single_vertex"
    bl_label = "Single Vertex"
    bl_options = {"REGISTER", "UNDO"}

    use_cursor_location: bpy.props.BoolProperty(name="Instance at Cursor Location", default=True)

    def execute(self, context):
        mesh = bpy.data.meshes.new(name="Single Vertex")
        mesh.from_pydata(((0, 0, 0),), (), ())
        obj = bpy.data.objects.new(name="Single Vertex", object_data=mesh)
        context.collection.objects.link(obj)
        bpy.ops.object.select_all(action="DESELECT")
        context.view_layer.objects.active = obj
        obj.select_set(True)
        if self.use_cursor_location:
            obj.location = context.scene.cursor.location
        return {"FINISHED"}
