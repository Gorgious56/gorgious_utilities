import bpy
from gorgious_utilities.bake.tool import bake
from gorgious_utilities.image.tool import create_image
from .tool import create_new_material


class BSDFMaterial:
    def __init__(self, name, material=None):
        self.name = name
        if material is None:
            self.material = create_new_material(self.name, use_nodes=True)
        else:
            self.material = material
        self.node_tree = self.material.node_tree
        self.links = self.node_tree.links
        self.bsdf_node = self.node_tree.nodes["Principled BSDF"]
        self.socket_bsdf_output = self.bsdf_node.outputs[0]

    def select_node(self, node):
        node.select = True
        self.node_tree.nodes.active = node

    @property
    def socket_input_output(self):
        return self.node_tree.nodes["Material Output"].inputs[0]

    def bake_all_maps(self, source, obj_target, obj_source, img_size):
        texture_nodes = 0
        for i, source_input in enumerate(source.bsdf_node.inputs):
            if not source_input.links:
                continue
            if source_input.name == "Normal":
                if not source_input.links[0].from_socket.node.inputs["Color"].links:
                    continue
            texture_nodes += 1
            node_texture = self.node_tree.nodes.new(type="ShaderNodeTexImage")
            new_img = create_image(name=self.name + "_" + source_input.name, width=img_size, height=img_size)
            node_texture.image = new_img
            node_texture.location = (-300, 600 - (texture_nodes * 300))
            if source_input.type != "RGBA":
                new_img.colorspace_settings.name = "Non-Color"
            if source_input.name == "Normal":
                node_normal_map = self.node_tree.nodes.new(type="ShaderNodeNormalMap")
                node_normal_map.location = node_texture.location
                self.node_tree.links.new(node_texture.outputs[0], node_normal_map.inputs[1])
                self.node_tree.links.new(node_normal_map.outputs[0], self.bsdf_node.inputs["Normal"])
                source_input = source_input.links[0].from_socket.node.inputs["Color"]
                if not source_input.links:
                    continue
            else:
                self.node_tree.links.new(node_texture.outputs[0], self.bsdf_node.inputs[source_input.name])

            source.links.new(source_input.links[0].from_socket, source.socket_input_output)
            self.select_node(node_texture)
            bake(obj_source, obj_target)
        source.links.new(source.socket_bsdf_output, source.socket_input_output)
        bpy.ops.image.save_all_modified()
