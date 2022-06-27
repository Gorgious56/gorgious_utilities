import bpy
from gorgious_utilities.nodes.tool import init_gn_node_tree


class GU_OT_convert_scene_to_mesh(bpy.types.Operator):
    bl_idname = "gu.convert_scene_to_mesh"
    bl_label = "Convert Scene To Mesh"
    bl_options = {"UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        bpy.ops.object.make_single_user(object=True, obdata=True)
        bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')

        gn_tree = bpy.data.node_groups.new(name="GN", type=bpy.types.GeometryNodeTree.__name__)
        init_gn_node_tree(gn_tree)
        realize = gn_tree.nodes.new(type=bpy.types.GeometryNodeRealizeInstances.__name__)
        gn_tree.links.new(next(n for n in gn_tree.nodes if isinstance(n, bpy.types.NodeGroupInput)).outputs[0], realize.inputs[0])
        gn_tree.links.new(realize.outputs[0], next(n for n in gn_tree.nodes if isinstance(n, bpy.types.NodeGroupOutput)).inputs[0])

        for obj in bpy.data.objects:
            if obj.type != "MESH":
                continue
            mod = obj.modifiers.new(type="NODES", name="REALIZE")
            mod.node_group = gn_tree
        
        bpy.ops.object.convert(target='MESH')
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

        return {"FINISHED"}