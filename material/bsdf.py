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

    def get_texture_maps(self):
        texture_maps = {}
        for input in self.bsdf_node.inputs:
            if not input.links:
                continue
            texture_node = input.links[0].from_socket.node
            if input.name == "Normal":
                texture_maps["Normal Map"] = texture_node
                texture_node = texture_node.inputs["Color"].links[0].from_socket.node
            texture_maps[input.name] = texture_node
        return texture_maps

    def bake_all_maps(self, source, obj_target, obj_source, props):
        texture_nodes = []
        texture_maps = self.get_texture_maps()
        for source_input in source.bsdf_node.inputs:
            if not source_input.links:
                if source_input.name != "Normal":
                    self.bsdf_node.inputs[source_input.name].default_value = source_input.default_value
                    continue
            texture_settings = obj_target.GUProps.lod.bake_settings.texture_settings
            for texture_setting in texture_settings:
                if texture_setting.name == source_input.name:
                    break
            else:
                texture_setting = None
            if texture_setting and not texture_setting.bake_me:
                continue
            node_texture = texture_maps.get(source_input.name)
            if node_texture is None:
                node_texture = self.node_tree.nodes.new(type="ShaderNodeTexImage")
            texture_nodes.append(node_texture)
            if texture_setting and texture_setting.active:
                img_size = texture_setting.pixel_size
                use_alpha = texture_setting.use_alpha
            else:
                img_size = props.pixel_size
                use_alpha = False
            new_img = create_image(
                name=self.name + "_" + source_input.name,
                width=img_size,
                height=img_size,
                alpha=use_alpha,
            )
            node_texture.image = new_img
            node_texture.location = (-300, 600 - (len(texture_nodes) * 300))
            if source_input.type != "RGBA":
                new_img.colorspace_settings.name = "Non-Color"
            if source_input.name == "Normal":
                node_normal_map = texture_maps.get("Normal Map")
                if node_normal_map is None:
                    node_normal_map = self.node_tree.nodes.new(type="ShaderNodeNormalMap")
                    node_normal_map.location = node_texture.location
                self.node_tree.links.new(node_texture.outputs[0], node_normal_map.inputs[1])
                self.node_tree.links.new(node_normal_map.outputs[0], self.bsdf_node.inputs["Normal"])
                if source_input.links:
                    source_input = source_input.links[0].from_socket.node.inputs["Color"]
                else:
                    self.select_node(node_texture)
                    bake(obj_source, obj_target, type="NORMAL")
                    continue
            else:
                self.node_tree.links.new(node_texture.outputs[0], self.bsdf_node.inputs[source_input.name])
                if source_input.name == "Base Color" and use_alpha:
                    self.node_tree.links.new(node_texture.outputs[1], self.bsdf_node.inputs["Alpha"])

            source.links.new(source_input.links[0].from_socket, source.socket_input_output)
            self.select_node(node_texture)
            bake(obj_source, obj_target)
        source.links.new(source.socket_bsdf_output, source.socket_input_output)
        if texture_nodes:
            self.select_node(texture_nodes[0])  # Select the base color texture so it displays in solid mode
            bpy.ops.image.save_all_modified()
