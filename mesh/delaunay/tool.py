import bpy
import bmesh
import numpy as np


def delaunay(obj, activate_new_object=True):
    from scipy.spatial import Delaunay

    if obj is None or obj.type != "MESH":
        print("No active mesh object selected.")
        return
    vertices = np.array([v.co for v in obj.data.vertices])

    mesh = bpy.data.meshes.new(name="DelaunayMesh")
    delaunay_obj = bpy.data.objects.new("DelaunayObj", mesh)

    obj.users_collection[0].objects.link(delaunay_obj)
    delaunay_obj.matrix_world = obj.matrix_world

    bm = bmesh.new()
    for v in vertices:
        bm.verts.new(v)
    bm.verts.ensure_lookup_table()
    tri = Delaunay([v[:2] for v in vertices])  # Use only x, y for triangulation
    # Create faces based on Delaunay triangulation
    for simplex in tri.simplices:
        bm.faces.new([bm.verts[i] for i in simplex])
    bm.to_mesh(mesh)
    bm.free()

    if activate_new_object:
        bpy.ops.object.select_all(action="DESELECT")
        delaunay_obj.select_set(True)
        bpy.context.view_layer.objects.active = delaunay_obj


if __name__ == "__main__":
    delaunay()
