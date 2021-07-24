import bpy
from bpy.types import(
    Operator,
)

from .property import copy_all_custom_props

class GU_OT_copy_custom_props(Operator):
    """Copies all custom props from active to selected objects"""
    bl_idname = "object.copy_all_custom_props"
    bl_label = "Copy ALL Props"
    bl_options = {"UNDO"}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and len(context.selected_editable_objects) > 1

    def execute(self, context):
        ao = context.active_object
        for ob in context.selected_editable_objects:
            if ob == ao:
                    continue
            copy_all_custom_props(ao, ob)
        return {'FINISHED'}


class GU_OT_toggle_object_render(Operator):
    """Tooltip"""
    bl_idname = "object.toggle_render"
    bl_label = "Toggle Render"
    bl_options = {"UNDO"}
    visibility_settings = ("camera", "diffuse", "glossy",
                           "transmission", "scatter", "shadow")

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        toggle = context.active_object.hide_render
        for obj in context.selected_objects:
            obj.hide_render = not toggle
            [setattr(obj.cycles_visibility, attr, toggle)
             for attr in self.visibility_settings]

            obj.display_type = 'TEXTURED' if toggle else 'WIRE'
        return {'FINISHED'}


class GU_OT_remove_custom_props(Operator):
    """Removes all custom properties from selected objects"""
    bl_idname = "object.remove_all_custom_props"
    bl_label = "Remove All Properties"
    bl_options = {"UNDO"}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and len(context.selected_editable_objects) > 0

    def execute(self, context):
        for obj in context.selected_editable_objects:
            props = [*obj.keys()]
            for i in range(len(props) - 1, -1, -1):
                del obj[props[i]]
        return {'FINISHED'}


class GU_OT_mesh_empty_add(Operator):
    """Add a mesh object with no geometry"""
    bl_idname = "mesh.empty_add"
    bl_label = "Empty"
    bl_options = {'REGISTER', 'UNDO'}

    use_cursor_location: bpy.props.BoolProperty(
        name="Instance at Cursor Location", default=True)

    def execute(self, context):
        obj = bpy.data.objects.new(
            name="Empty Mesh", object_data=bpy.data.meshes.new(name="Empty Mesh"))
        context.collection.objects.link(obj)
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        if self.use_cursor_location:
            obj.location = bpy.context.scene.cursor.location
        return {'FINISHED'}


class GU_OT_mesh_single_vertex_add(Operator):
    """Add a mesh object with a single vertex at origin"""
    bl_idname = "mesh.single_vertex_add"
    bl_label = "Single Vertex"
    bl_options = {'REGISTER', 'UNDO'}

    use_cursor_location: bpy.props.BoolProperty(
        name="Instance at Cursor Location", default=True)

    def execute(self, context):
        mesh = bpy.data.meshes.new(name="Single Vertex")
        mesh.from_pydata(((0, 0, 0),), (), ())
        obj = bpy.data.objects.new(name="Single Vertex", object_data=mesh)
        context.collection.objects.link(obj)
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        if self.use_cursor_location:
            obj.location = bpy.context.scene.cursor.location
        return {'FINISHED'}

