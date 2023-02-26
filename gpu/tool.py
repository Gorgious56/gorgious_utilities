# Code inspired by the BlenderBIM addon (C) Dion Moult 2020, 2021, modified by Nathan HILD 2023
# https://github.com/IfcOpenShell/IfcOpenShell/blob/v0.7.0/src/blenderbim/blenderbim/bim/module/model/opening.py

import bpy
import gpu
import bgl
import bmesh
from gpu_extras.batch import batch_for_shader
from gorgious_utilities.core.preferences.tool import get_preferences


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

    def batch_shader(self, color, size, *args, **kwargs):
        if args[0] == "LINES":
            bgl.glLineWidth(int(size))
        elif args[0] == "POINTS":
            bgl.glPointSize(int(size))
        batch = batch_for_shader(self.shader, *args, **kwargs)
        self.shader.uniform_float("color", color)
        batch.draw(self.shader)

    def init_global(self, context):
        bgl.glEnable(bgl.GL_BLEND)
        bgl.glEnable(bgl.GL_LINE_SMOOTH)

        self.depsgraph = context.evaluated_depsgraph_get()
        self.shader = gpu.shader.from_builtin("3D_UNIFORM_COLOR")

        self.unselected_point_size = 4

        self.gpu_preferences = get_preferences().gpu

    def init_for_obj(self, obj):
        self.select_mode = set()
        self.verts = []
        self.selected_edges = []
        self.unselected_edges = []
        self.selected_vertices = []
        self.unselected_vertices = []
        self.selected_face_centers = []
        self.unselected_face_centers = []
        self.matrix_world = obj.matrix_world

    def is_obj_valid(self, obj):
        return obj is not None and obj.type in ("MESH", "CURVE")

    def calc_obj_and_mesh_eval(self, obj):
        self.obj_eval = obj.evaluated_get(self.depsgraph)
        self.mesh_eval = self.obj_eval.data
        if self.obj_eval.type != "MESH":
            self.mesh_eval = self.obj_eval.to_mesh()

    def create_bmesh(self):
        if self.obj_eval.mode == "EDIT":
            if not self.obj_eval.GUProps.gpu.draw_mesh_edit_mode:
                self.bm = None
                return
            if self.obj_eval.type == "MESH":
                self.bm = bmesh.from_edit_mesh(self.mesh_eval)
            else:
                self.bm = bmesh.new()
                self.bm.from_mesh(self.mesh_eval)
        elif self.obj_eval.mode == "OBJECT":
            if not self.obj_eval.GUProps.gpu.draw_mesh_object_mode:
                self.bm = None
                return
            self.bm = bmesh.new()
            self.bm.from_mesh(self.mesh_eval)
        else:
            self.bm = None
            return
        if self.bm is not None:
            self.select_mode = self.bm.select_mode

    def process_verts(self, color_selected):
        for vertex in self.bm.verts:
            co = self.matrix_world @ vertex.co
            self.verts.append(co)
            if vertex.hide:
                continue
            if self.obj_eval.mode == "OBJECT" or not vertex.select:
                self.unselected_vertices.append(co)
            else:
                self.selected_vertices.append(co)
        self.batch_shader(
            self.gpu_preferences.color_unselected,
            self.unselected_point_size,
            "POINTS",
            {"pos": self.unselected_vertices},
        )
        if "VERT" in self.select_mode:
            self.batch_shader(color_selected, 8, "POINTS", {"pos": self.selected_vertices})

    def process_edges(self, color_selected):
        for edge in self.bm.edges:
            edge_indices = [v.index for v in edge.verts]
            if edge.hide:
                continue
            if self.obj_eval.mode == "OBJECT" or not edge.select:
                self.unselected_edges.append(edge_indices)
            else:
                self.selected_edges.append(edge_indices)
        self.batch_shader(
            self.gpu_preferences.color_unselected, 2, "LINES", {"pos": self.verts}, indices=self.unselected_edges
        )
        self.batch_shader(color_selected, 3, "LINES", {"pos": self.verts}, indices=self.selected_edges)

    def process_faces(self, color_selected_dot, color_selected_face):
        if "FACE" not in self.select_mode:
            return
        selected_faces = []
        for face in self.bm.faces:
            if face.hide:
                continue
            if self.obj_eval.mode == "OBJECT" or not face.select:
                self.unselected_face_centers.append(self.matrix_world @ face.calc_center_median())
            else:
                selected_faces.append(face.index)
                self.selected_face_centers.append(self.matrix_world @ face.calc_center_median())

        if selected_faces:
            bm_tri = self.bm.copy()
            bm_tri.faces.ensure_lookup_table()
            bmesh.ops.triangulate(bm_tri, faces=[bm_tri.faces[i] for i in selected_faces])
            for face in bm_tri.faces:
                if len(face.verts) != 3:
                    continue
                self.batch_shader(
                    color_selected_face, -1, "TRIS", {"pos": [self.matrix_world @ v.co for v in face.verts]}
                )

        self.batch_shader(self.gpu_preferences.color_unselected, 5, "POINTS", {"pos": self.unselected_face_centers})
        self.batch_shader(color_selected_dot, 8, "POINTS", {"pos": self.selected_face_centers})

    def __call__(self, context):
        self.init_global(context)
        for obj in context.selected_objects:
            self.init_for_obj(obj)
            if not self.is_obj_valid(obj):
                continue
            self.calc_obj_and_mesh_eval(obj)
            self.create_bmesh()
            if self.bm is None:
                continue

            self.process_verts(color_selected=context.preferences.themes[0].view_3d.vertex_select[:] + (1,))
            self.process_edges(color_selected=context.preferences.themes[0].view_3d.edge_select[:] + (1,))
            self.process_faces(
                color_selected_dot=context.preferences.themes[0].view_3d.face_dot[:] + (1,),
                color_selected_face=context.preferences.themes[0].view_3d.face_select[:],
            )
            self.process_curve_handles()

        self.shader.bind()

    def add_handle(self, point, handle, selected=True):
        selection_verts, edges = (
            (self.selected_vertices, self.selected_edges)
            if selected
            else (self.unselected_vertices, self.unselected_edges)
        )
        if self.obj.mode == "OBJECT":
            selection_verts = self.unselected_vertices
            edges = self.unselected_edges
        self.verts.append(self.matrix_world @ handle)
        self.verts.append(self.matrix_world @ point)
        edges.append([len(self.verts) - 1, len(self.verts) - 2])
        if selected:
            selection_verts.append(self.matrix_world @ handle)
            selection_verts.append(self.matrix_world @ point)

    def process_curve_handles(self):
        if self.obj_eval.type != "CURVE" or self.obj_eval.mode != "EDIT":
            return
        self.select_mode = ("VERT",)
        for spline in self.obj.data.splines:
            for point in spline.bezier_points:
                if point.hide:
                    continue
                self.add_handle(point.co, point.handle_right, selected=True)
                self.add_handle(point.co, point.handle_left, selected=True)
            for point in spline.points:
                # For some reason there is a 4th component to point coordinates
                if self.obj.mode == "OBJECT" or not point.select:
                    self.unselected_vertices.append(self.matrix_world @ point.co.xyz)
                else:
                    self.selected_vertices.append(self.matrix_world @ point.co.xyz)
