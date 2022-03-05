import bpy


class ColorViewport:
    def __init__(self, diffuse_color, metallic, roughness) -> None:
        self.diffuse_color = diffuse_color
        self.metallic = metallic
        self.roughness = roughness


def update_viewport_color(material: bpy.types.Material) -> None:
    color_viewport = get_main_color(material)
    if color_viewport is not None:
        for key, value in color_viewport.__dict__.items():
            setattr(material, key, value)


def get_main_color(material: bpy.types.Material) -> None:
    if not material.use_nodes:
        return None
    nodes = material.node_tree.nodes
    for node in nodes:
        if isinstance(node, bpy.types.ShaderNodeBsdfPrincipled):
            return ColorViewport(
                diffuse_color=node.inputs[0].default_value,
                metallic=node.inputs[6].default_value,
                roughness=node.inputs[9].default_value,
            )
        elif isinstance(node, (bpy.types.ShaderNodeBsdfDiffuse, bpy.types.ShaderNodeBsdfGlossy)):
            return ColorViewport(
                diffuse_color=node.inputs[0].default_value,
                metallic=0,
                roughness=node.inputs[1].default_value,
            )
        elif isinstance(node, (bpy.types.ShaderNodeEmission, bpy.types.ShaderNodeBsdfTransparent)):
            return ColorViewport(
                diffuse_color=node.inputs[0].default_value,
                metallic=0,
                roughness=0.4,
            )
