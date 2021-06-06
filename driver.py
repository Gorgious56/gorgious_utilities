import bpy
import mathutils.geometry
from mathutils import Vector


def get_clip_plane(bbox, mx, plane_idx):
    mw = mx
    vs = [mw @ Vector(v) for v in bbox]

    #          2-----------6
    #         /           /|
    #       1-----------5  |
    #       |           |  |
    #       |           |  |
    #       |  3        |  7
    #       |           | /
    #       0-----------4

    fs = (
        (0, 4, 5, 1),  # front
        (3, 2, 6, 7),  # back
        (1, 5, 6, 2),  # top
        (0, 3, 7, 4),  # bottom
        (0, 1, 2, 3),  # left
        (4, 7, 6, 5),  # right
    )

    quads = [vs[fs[plane_idx][j]] for j in range(4)]
    n = mathutils.geometry.normal(quads)
    n.negate()

    v = quads[0]
    d = mathutils.geometry.distance_point_to_plane(Vector(), v, n)

    return n.to_tuple() + (d,)


@bpy.app.handlers.persistent
def setup_driver_namespace(*args):
    bpy.app.driver_namespace["get_clip_plane"] = get_clip_plane


def register():
    bpy.app.handlers.load_post.append(setup_driver_namespace)


def unregister():
    bpy.app.handlers.load_post.remove(setup_driver_namespace)
