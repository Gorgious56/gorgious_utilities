# Code inspired by the BlenderBIM addon (C) Dion Moult 2020, 2021, modified by Nathan HILD 2023
# https://github.com/IfcOpenShell/IfcOpenShell/blob/v0.7.0/src/blenderbim/blenderbim/bim/module/model/opening.py

import bpy
import gpu
import bgl
import bmesh
from gpu_extras.batch import batch_for_shader


class MeshDrawer:
    installed = None

    @classmethod
    def install(cls, context):
        if cls.installed:
            cls.uninstall()
        handler = cls()
        cls.installed = bpy.types.SpaceView3D.draw_handler_add(handler, (context,), "WINDOW", "POST_VIEW")

    @classmethod
    def uninstall(cls):
        try:
            bpy.types.SpaceView3D.draw_handler_remove(cls.installed, "WINDOW")
        except ValueError:
            pass
        cls.installed = None

    def __call__(self, context):
        bgl.glEnable(bgl.GL_BLEND)
        bgl.glEnable(bgl.GL_LINE_SMOOTH)

        obj = context.active_object
        if obj is None or obj.type not in ("MESH", "CURVE"):
            return

        depsgraph = context.evaluated_depsgraph_get()
        obj = obj.evaluated_get(depsgraph)
        mesh = obj.data
        if obj.type != "MESH":
            mesh = obj.to_mesh()

        def bmesh_object_mode():
            bm = bmesh.new()
            bm.from_mesh(mesh)
            return bm

        if obj.mode == "EDIT":
            if not obj.GUProps.gpu.draw_mesh_edit_mode:
                return
            if obj.type == "MESH":
                bm = bmesh.from_edit_mesh(mesh)
            else:
                bm = bmesh_object_mode()
        elif obj.mode == "OBJECT":
            if not obj.GUProps.gpu.draw_mesh_object_mode:
                return
            bm = bmesh_object_mode()
        else:
            return

        white = (1, 1, 1, 1)
        white_t = (1, 1, 1, 0.1)
        green = (0.545, 0.863, 0, 1)
        red = (1, 0.2, 0.322, 1)
        red_t = (1, 0.2, 0.322, 0.1)
        blue = (0.157, 0.565, 1, 1)
        blue_t = (0.157, 0.565, 1, 0.1)
        grey = (0.4, 0.4, 0.4, 1)
        black = (0, 0, 0, 1)
        orange = (1, 0.62, 0, 1)
        pink = (0.8, 0.3, 0.8, 1)

        color_unselected = pink
        color_selected = red

        self.shader = gpu.shader.from_builtin("3D_UNIFORM_COLOR")

        verts = []
        selected_edges = []
        unselected_edges = []
        selected_vertices = []
        unselected_vertices = []
        selected_face_centers = []
        unselected_face_centers = []

        unselected_point_size = 4 if obj.type == "MESH" else 1

        depsgraph = context.evaluated_depsgraph_get()
        obj = obj.evaluated_get(depsgraph)

        matrix_world = obj.matrix_world

        for vertex in bm.verts:
            co = matrix_world @ vertex.co
            verts.append(co)
            if vertex.hide:
                continue

            if vertex.select:
                selected_vertices.append(co)
            else:
                unselected_vertices.append(co)

        for edge in bm.edges:
            edge_indices = [v.index for v in edge.verts]
            if edge.hide:
                continue
            if edge.select:
                selected_edges.append(edge_indices)
            else:
                unselected_edges.append(edge_indices)

        select_mode = bm.select_mode
        if obj.type == "CURVE" and obj.mode == "EDIT":  # Display handles
            select_mode = "VERT"

            def add_handle(point, handle, selected=True):
                selection_verts, edges = (
                    (selected_vertices, selected_edges) if selected else (unselected_vertices, unselected_edges)
                )
                verts.append(matrix_world @ handle)
                verts.append(matrix_world @ point)
                edges.append([len(verts) - 1, len(verts) - 2])
                if selected:
                    selection_verts.append(matrix_world @ handle)
                    selection_verts.append(matrix_world @ point)

            for spline in obj.data.splines:
                for point in spline.bezier_points:
                    if point.hide:
                        continue
                    add_handle(point.co, point.handle_right, selected=True)
                    add_handle(point.co, point.handle_left, selected=True)

        def batch_shader(color, size, *args, **kwargs):
            if args[0] == "LINES":
                bgl.glLineWidth(size)
            elif args[0] == "POINTS":
                bgl.glPointSize(size)
            batch = batch_for_shader(self.shader, *args, **kwargs)
            self.shader.uniform_float("color", color)
            batch.draw(self.shader)

        batch_shader(color_unselected, 2, "LINES", {"pos": verts}, indices=unselected_edges)
        batch_shader(color_selected, 3, "LINES", {"pos": verts}, indices=selected_edges)

        batch_shader(black, unselected_point_size, "POINTS", {"pos": unselected_vertices})
        if "VERT" in select_mode:
            batch_shader(color_selected, 8, "POINTS", {"pos": selected_vertices})

        if "FACE" in select_mode:
            for face in bm.faces:
                if face.hide:
                    continue
                if face.select:
                    selected_face_centers.append(matrix_world @ face.calc_center_median())
                else:
                    unselected_face_centers.append(matrix_world @ face.calc_center_median())

            batch_shader(color_unselected, 5, "POINTS", {"pos": unselected_face_centers})
            batch_shader(color_selected, 8, "POINTS", {"pos": selected_face_centers})

        self.shader.bind()
