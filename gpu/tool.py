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
        bgl.glLineWidth(2)
        bgl.glPointSize(6)
        bgl.glEnable(bgl.GL_BLEND)
        bgl.glEnable(bgl.GL_LINE_SMOOTH)

        obj = context.active_object
        if obj is None or obj.type != "MESH" or not obj.GUProps.gpu.draw_mesh:
            return

        white = (1, 1, 1, 1)
        white_t = (1, 1, 1, 0.1)
        green = (0.545, 0.863, 0, 1)
        red = (1, 0.2, 0.322, 1)
        red_t = (1, 0.2, 0.322, 0.1)
        blue = (0.157, 0.565, 1, 1)
        blue_t = (0.157, 0.565, 1, 0.1)
        grey = (0.2, 0.2, 0.2, 1)
        black = (0, 0, 0, 1)

        self.shader = gpu.shader.from_builtin("3D_UNIFORM_COLOR")

        verts = []
        selected_edges = []
        unselected_edges = []
        selected_vertices = []
        unselected_vertices = []

        if obj.mode == "EDIT":
            bm = bmesh.from_edit_mesh(obj.data)

            for vertex in bm.verts:
                co = tuple(obj.matrix_world @ vertex.co)
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

            batch = batch_for_shader(self.shader, "LINES", {"pos": verts}, indices=unselected_edges)
            self.shader.bind()
            self.shader.uniform_float("color", black)
            batch.draw(self.shader)

            batch = batch_for_shader(self.shader, "LINES", {"pos": verts}, indices=selected_edges)
            self.shader.uniform_float("color", red)
            batch.draw(self.shader)

            batch = batch_for_shader(self.shader, "POINTS", {"pos": unselected_vertices})
            self.shader.uniform_float("color", black)
            batch.draw(self.shader)

            batch = batch_for_shader(self.shader, "POINTS", {"pos": selected_vertices})
            self.shader.uniform_float("color", red)
            batch.draw(self.shader)
