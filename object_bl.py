import bpy
from bpy.types import(
    Operator,
)

from .property import copy_all_custom_props


class GU_OT_material_init_custom_props(Operator):
    r"""Link Attributes as Custom Properties
    Make sure the prop name in the Attribute node ends with 'fac' or 'color' to initialize correct type
    Add a value or RGB node with the same name (/!\ NOT the Label) as the attribute to initialize default
    Also set to Attribute node type to 'Object'"""
    bl_idname = "material.init_custom_properties"
    bl_label = "Link Props"
    bl_settings = {"INTERNAL"}
    bl_options = {"UNDO"}
    overwrite: bpy.props.BoolProperty(default=False)

    @classmethod
    def poll(cls, context):
        return (
            context.active_object is not None
            and hasattr(context.active_object, "data")
            and hasattr(context.active_object.data, "materials")
        )

    def execute(self, context):
        # RNA_UI = "_RNA_UI"
        for obj in context.selected_objects:
            if not hasattr(obj, "data") or not hasattr(obj.data, "materials"):
                continue

            materials_to_init = set()

            # Traverse object materials
            materials_to_init.update(
                [m for m in obj.data.materials if m and m.use_nodes and m.node_tree and m.node_tree.nodes]
            )
            # Traverse GN modifiers to see if materials are added to the geometry
            for tree in (m.node_group for m in obj.modifiers if m.type == "NODES"):
                for node in tree.nodes:
                    if node.type == "MATERIAL_ASSIGN":
                        print(node.inputs[1].default_value)
                        materials_to_init.add(node.inputs[1].default_value)
                    if node.type == "MATERIAL_REPLACE":
                        materials_to_init.add(node.inputs[2].default_value)

            for mat in materials_to_init:
                if mat is None or not mat.use_nodes:
                    continue
                nodes = mat.node_tree.nodes
                for attr_node in (n for n in nodes if n.type == "ATTRIBUTE" and n.attribute_type == "OBJECT"):
                    attr_name = attr_node.attribute_name
                    default_value_node = nodes.get(attr_name)
                    if attr_name.endswith("fac"):
                        default = default_value_node.outputs[0].default_value if default_value_node else 1.0
                    elif attr_name.endswith("color"):
                        default = (
                            default_value_node.outputs[0].default_value[0:4] if default_value_node else (0.0,) * 4
                        )
                    else:
                        continue
                    if obj.get(attr_name) is None or self.overwrite:
                        obj[attr_name] = default
                        prop_data = obj.id_properties_ui(attr_name)
                        prop_data.update(min=0, max=1, default=default)
                        if not isinstance(default, float):
                            prop_data.update(subtype="COLOR")

        return {"FINISHED"}


class GU_OT_copy_custom_props(Operator):
    """Copies all custom props from active to selected objects"""
    bl_idname = "object.copy_all_custom_props"
    bl_label = "Copy ALL Props"
    bl_options = {"UNDO"}

    @ classmethod
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
    visibility_settings = ("camera", "diffuse", "glossy", "transmission", "volume_scatter", "shadow")

    @ classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        toggle = context.active_object.hide_render
        for obj in context.selected_objects:
            obj.hide_render = not toggle
            for attr in self.visibility_settings:
                setattr(obj, "visible_" + attr, toggle)
            obj.display_type = 'TEXTURED' if toggle else 'WIRE'
        return {'FINISHED'}


class GU_OT_remove_custom_props(Operator):
    """Removes all custom properties from selected objects"""
    bl_idname = "object.remove_all_custom_props"
    bl_label = "Remove All Properties"
    bl_options = {"UNDO"}

    @ classmethod
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
        obj = bpy.data.objects.new(name="Empty Mesh", object_data=bpy.data.meshes.new(name="Empty Mesh"))
        context.collection.objects.link(obj)
        bpy.ops.object.select_all(action='DESELECT')
        context.view_layer.objects.active = obj
        obj.select_set(True)
        if self.use_cursor_location:
            obj.location = context.scene.cursor.location
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
        context.view_layer.objects.active = obj
        obj.select_set(True)
        if self.use_cursor_location:
            obj.location = context.scene.cursor.location
        return {'FINISHED'}
