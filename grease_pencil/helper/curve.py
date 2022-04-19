import bpy

def new_convert_mesh_object(collection, name, gpencil_object):
    mesh = bpy.data.meshes.new(name=name)
    convert_object = bpy.data.objects.new(name=name, object_data=mesh)
    collection.objects.link(convert_object)
    convert_object.matrix_world = gpencil_object.matrix_world
    return convert_object


def new_convert_curve_object(collection, name, gpencil_object):
    curve = bpy.data.curves.new(name=name, type="CURVE")
    curve.dimensions = "3D"
    convert_object = bpy.data.objects.new(name=name, object_data=curve)
    collection.objects.link(convert_object)
    convert_object.matrix_world = gpencil_object.matrix_world
    return convert_object


def convert_gpencil_to_mesh(gpencil_object, flatten_layers=True, collection=None):
    gp_col = gpencil_object.users_collection[0] if collection is None else collection
    gp = gpencil_object.data
    if flatten_layers:
        obj = new_convert_mesh_object(gp_col, gpencil_object.name + "_mesh", gpencil_object)
        yield obj
        vertices = []
        edges = []
    for layer in gp.layers:
        if not flatten_layers:
            obj = new_convert_mesh_object(gp_col, f"{gpencil_object.name}_mesh_layer_{layer.info}", gpencil_object)
            yield obj
            vertices = []
            edges = []
        for frame in layer.frames:
            for stroke in frame.strokes:
                for i, point in enumerate(stroke.points):
                    vertices.append(point.co)
                    if i > 0:
                        edges.append((len(vertices) - 1, len(vertices) - 2))
        if not flatten_layers:
            obj.data.from_pydata(vertices, edges, ())
    if flatten_layers:
        obj.data.from_pydata(vertices, edges, ())


def convert_gpencil_to_curve(gpencil_object, flatten_layers=True, collection=None):
    gp_col = gpencil_object.users_collection[0] if collection is None else collection
    gp = gpencil_object.data
    if flatten_layers:
        obj = new_convert_curve_object(gp_col, gpencil_object.name + "_curve", gpencil_object)
        yield obj
    for layer in gp.layers:
        if not flatten_layers:
            obj = new_convert_curve_object(gp_col, f"{gpencil_object.name}_curve_layer_{layer.info}", gpencil_object)
            yield obj
        for frame in layer.frames:
            for stroke in frame.strokes:
                spline = obj.data.splines.new(type="POLY")
                spline.points.add(len(stroke.points) - 1)  # Spline starts with 1 point
                for i, point in enumerate(stroke.points):
                    spline.points[i].co = [v for v in point.co] + [1]
