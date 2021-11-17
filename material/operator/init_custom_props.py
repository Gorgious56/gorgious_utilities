import bpy
from gorgious_utilities.custom_property.helper import (
    get_all_ui_props,
)


class GU_OT_material_init_custom_props(bpy.types.Operator):
    r"""Link Attributes as Custom Properties
    Make sure the prop name in the Attribute node ends with 'fac' or 'color' to initialize correct type
    Add a value or RGB node with the same name (/!\ NOT the Label) as the attribute to initialize default
    Also set to Attribute node type to 'Object'"""
    bl_idname = "material.init_custom_properties"
    bl_label = "Link Props"
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
        def traverse_all_node_trees(node_tree):
            for n in node_tree.nodes:
                if n.type == "GROUP":
                    yield from traverse_all_node_trees(n.node_tree)
            yield node_tree

        for obj in context.selected_objects:
            if not hasattr(obj, "data") or not hasattr(obj.data, "materials"):
                continue

            materials_to_init = set()

            # Traverse object materials
            materials_to_init.update(
                [m for m in obj.data.materials if m and m.use_nodes and m.node_tree and m.node_tree.nodes]
            )
            # Traverse GN modifiers to see if materials are added to the geometry
            for mod in (m for m in obj.modifiers if m.type == "NODES"):
                for inp in get_all_ui_props(mod):
                    value = mod[f"{inp}"]
                    if value and isinstance(value, bpy.types.Material):
                        materials_to_init.add(value)

                for node in mod.node_group.nodes:
                    if node.type in ("SET_MATERIAL", "REPLACE_MATERIAL"):
                        mat = node.inputs[2].default_value
                        if mat:
                            materials_to_init.add(mat)

            for mat in materials_to_init:
                if mat is None or not mat.use_nodes:
                    continue

                for node_tree in traverse_all_node_trees(mat.node_tree):
                    nodes = node_tree.nodes
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
