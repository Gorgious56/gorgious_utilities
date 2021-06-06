import bpy.types
from .object_bl import (
    GU_OT_mesh_empty_add,
    GU_OT_mesh_single_vertex_add,
    GU_OT_copy_custom_props,
    GU_OT_remove_custom_props,
    GU_OT_toggle_object_render,
)
from .mesh import (
    GU_OT_print_highest_mesh_count,
)
from .material import (
    GU_OT_material_init_custom_props,
)
from .collection import (
    GU_OT_collection_move_to_this,
    GU_OT_collection_rename_objects,
    GU_OT_collection_toggle_object_visibility,
    GU_OT_destructively_join_meshes,
    get_collection_layers_from_collections,
)
from .property import(
    GU_OT_property_copy,
)


def draw_new_mesh_objects(self, _):
    self.layout.operator(GU_OT_mesh_empty_add.bl_idname, text="Empty", icon='GHOST_ENABLED')
    self.layout.operator(GU_OT_mesh_single_vertex_add.bl_idname, text="Single Vertex", icon='DOT')


def draw_custom_properties_ops(self, _):
    row = self.layout.row(align=True)
    row.operator(GU_OT_copy_custom_props.bl_idname, text="", icon='EYEDROPPER')
    row.operator(GU_OT_material_init_custom_props.bl_idname, text="", icon='MATERIAL')
    row.operator(GU_OT_remove_custom_props.bl_idname, text="", icon='TRASH')


def draw_toggle_render_object_context(self, _):
    self.layout.operator(GU_OT_toggle_object_render.bl_idname, text="Toggle Render")


def draw_print_mesh_count(self, _):
    self.layout.operator(GU_OT_print_highest_mesh_count.bl_idname)


def draw_custom_props_links(self, context):
    self.layout.operator(GU_OT_material_init_custom_props.bl_idname, text="Copy Material Attributes")
    self.layout.operator(GU_OT_copy_custom_props.bl_idname, text="Copy Custom Properties")
    self.layout.operator(GU_OT_property_copy.bl_idname, text="Copy ANY Property")


def draw_boolean_collection_toggle(self, context):
    op = self.layout.operator(GU_OT_collection_toggle_object_visibility.bl_idname, text="Toggle Booleans")
    op.col_name = "BOOL"


def draw_blueprint_collection_toggle(self, context):
    op = self.layout.operator(GU_OT_collection_toggle_object_visibility.bl_idname, text="Toggle Blueprints")
    op.col_name = "BP_"


def draw_exclude_collections_from_object(self, context):
    layout = self.layout
    for col_layer in get_collection_layers_from_collections(context, context.active_object.users_collection):
        split = layout.split(align=True, factor=0.4)
        split.label(text=col_layer.name)
        split.prop(col_layer, "exclude")


def draw_collection_context(self, _):
    layout = self.layout
    layout.separator()
    layout.operator(GU_OT_collection_rename_objects.bl_idname, text="Rename Objects")
    layout.operator(GU_OT_collection_move_to_this.bl_idname, text="Move Selected Objects to this Collection")
    layout.operator(GU_OT_destructively_join_meshes.bl_idname, text="Destructively Join Meshes")


menus_appends = {
    bpy.types.VIEW3D_MT_make_links: draw_custom_props_links,
    bpy.types.VIEW3D_MT_object_context_menu: draw_toggle_render_object_context,
    bpy.types.VIEW3D_MT_mesh_add: draw_new_mesh_objects,
    bpy.types.VIEW3D_MT_object_cleanup: draw_print_mesh_count,
    bpy.types.VIEW3D_MT_view: draw_boolean_collection_toggle,
    bpy.types.VIEW3D_MT_view: draw_blueprint_collection_toggle,
    bpy.types.OUTLINER_MT_collection: draw_collection_context,
    bpy.types.OBJECT_PT_collections: draw_exclude_collections_from_object,
}
menus_prepends = {
    bpy.types.OBJECT_PT_custom_props: draw_custom_properties_ops,
}


def register():
    for menu, draw in menus_appends.items():
        menu.append(draw)
    for menu, draw in menus_prepends.items():
        menu.prepend(draw)


def unregister():
    for menu, draw in menus_appends.items():
        menu.remove(draw)
    for menu, draw in menus_prepends.items():
        menu.remove(draw)
