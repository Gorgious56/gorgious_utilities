from bpy.types import (
    Operator,
)


class GU_OT_material_init_custom_props(Operator):
    """Link Attributes as Custom Properties"""

    bl_idname = "material.init_custom_properties"
    bl_label = "Link Props"
    bl_settings = {"INTERNAL"}
    bl_options = {"UNDO"}

    @classmethod
    def poll(cls, context):
        return (
            context.active_object is not None
            and hasattr(context.active_object, "data")
            and hasattr(context.active_object.data, "materials")
        )

    def execute(self, context):
        RNA_UI = "_RNA_UI"
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
                    if obj.get(attr_name) is not None:
                        continue
                    default_value_node = nodes.get(attr_name)
                    if RNA_UI not in obj.keys():
                        obj[RNA_UI] = {}
                    if attr_name.endswith("fac"):
                        default = default_value_node.outputs[0].default_value if default_value_node else 1.0
                        obj[attr_name] = default
                        obj[RNA_UI][attr_name] = {"min": 0, "max": 1, "default": default}
                    elif attr_name.endswith("color"):
                        default = (
                            default_value_node.outputs[0].default_value[0:3] if default_value_node else [0.0, 0.0, 0.0]
                        )
                        obj[attr_name] = default
                        obj[RNA_UI][attr_name] = {"min": 0, "max": 1, "default": default, "subtype": "COLOR"}

        return {"FINISHED"}
