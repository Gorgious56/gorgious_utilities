import bpy


def get_geometry_nodes_groups(self, context):
    get_geometry_nodes_groups.groups = []
    for ng in [ng for ng in bpy.data.node_groups if ng.bl_idname == "GeometryNodeTree"]:
        get_geometry_nodes_groups.groups.append((ng.name, ) * 3)
    return get_geometry_nodes_groups.groups
