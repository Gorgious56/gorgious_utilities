from gorgious_utilities.core.prop import GUPropsCollection, GUPropsScene
import bpy
from bpy.props import (
    PointerProperty,
    EnumProperty,
    BoolProperty,
    FloatVectorProperty,
    IntProperty,
)
from bpy.types import PropertyGroup
from bpy.app.handlers import persistent


def set_dirty(self, context):
    self.is_dirty = True
    self.should_enforce_any = any(getattr(self, attr) for attr in self.__annotations__ if attr.endswith("enforce"))


class GU_PG_EnforceProps(PropertyGroup):
    NOT_ENFORCED_ATTRIBUTE_NAMES = ("is_dirty", "last_item_count", "should_enforce_any", "priority")  # type: ignore
    is_dirty: BoolProperty(default=False)  # type: ignore
    last_item_count: IntProperty(default=-1, update=set_dirty)  # type: ignore
    should_enforce_any: BoolProperty(default=False)  # type: ignore
    priority: IntProperty(
        soft_min=0,
        soft_max=255,
        description="Enforcement Priority. Highest priority rules will be applied last",
        update=set_dirty,
    )  # type: ignore

    show_name_enforce: BoolProperty(default=False, update=set_dirty)  # type: ignore
    show_name: BoolProperty(default=False, update=set_dirty)  # type: ignore

    show_axis_enforce: BoolProperty(default=False, update=set_dirty)  # type: ignore
    show_axis: BoolProperty(default=False, update=set_dirty)  # type: ignore

    show_wire_enforce: BoolProperty(default=False, update=set_dirty)  # type: ignore
    show_wire: BoolProperty(default=False, update=set_dirty)  # type: ignore

    show_all_edges_enforce: BoolProperty(default=False, update=set_dirty)  # type: ignore
    show_all_edges: BoolProperty(default=False, update=set_dirty)  # type: ignore

    show_texture_space_enforce: BoolProperty(default=False, update=set_dirty)  # type: ignore
    show_texture_space: BoolProperty(default=False, update=set_dirty)  # type: ignore

    show_in_front_enforce: BoolProperty(default=False, update=set_dirty)  # type: ignore
    show_in_front: BoolProperty(default=False, update=set_dirty)  # type: ignore

    display_type_enforce: BoolProperty(default=False, update=set_dirty)  # type: ignore
    display_type: EnumProperty(
        items=(
            ("BOUNDS", "Bounds", ""),
            ("WIRE", "Wire", ""),
            ("SOLID", "Solid", ""),
            ("TEXTURED", "Textured", ""),
        ),
        default="TEXTURED",
        name="Display",
        update=set_dirty,
    )  # type: ignore

    color_enforce: BoolProperty(default=False, update=set_dirty)  # type: ignore
    color: FloatVectorProperty(
        subtype="COLOR",
        size=4,
        min=0,
        max=1,
        default=(1, 1, 1, 1),
        name="Color",
        update=set_dirty,
    )  # type: ignore

    @property
    def enforceable_props(self):
        return [
            p
            for p in self.__annotations__
            if p not in GU_PG_EnforceProps.NOT_ENFORCED_ATTRIBUTE_NAMES and not p.endswith("enforce")
        ]

    def draw(self, layout):
        layout = layout.column(align=True)
        layout.prop(self, "is_dirty", toggle=True, text="Force Update", icon="FILE_REFRESH")
        layout.prop(self, "priority", text="Priority")
        for attr in self.__annotations__:
            if attr in GU_PG_EnforceProps.NOT_ENFORCED_ATTRIBUTE_NAMES:
                continue
            if attr.endswith("enforce"):
                continue
            row = layout.row(align=True, heading=attr.replace("_", " ").title())
            row.prop(self, f"{attr}_enforce", text="")
            col = row.row(align=True)
            col.prop(self, attr, text="")
            col.active = getattr(self, f"{attr}_enforce")

    def should_update_enforcement(self):
        if (objects_count := len(self.id_data.all_objects)) != self.last_item_count:
            self.last_item_count = objects_count
            return self.should_enforce_any or self.is_dirty
        return self.is_dirty


@persistent
def enforce(scene):
    if scene.GUProps.collection_enforce.active:
        collections = [c for c in scene.collection.children_recursive if c.GUProps.enforce.should_enforce_any]
        collections = set(sorted(collections, key=lambda c: c.GUProps.enforce.priority))
        for col in collections:
            props = col.GUProps.enforce
            children_recursive = col.children_recursive
            for col_children in children_recursive:
                if col_children.GUProps.enforce.is_dirty:
                    props.is_dirty = True
                    break
            if not props.should_update_enforcement():
                continue
            for attr in props.enforceable_props:
                if getattr(props, f"{attr}_enforce"):
                    for obj in col.all_objects:
                        setattr(obj, attr, getattr(props, attr))
            for col_children in children_recursive:
                col_children.GUProps.enforce.is_dirty = True

            props.is_dirty = False


def draw_OBJECT_PT_DISPLAY(self, context):
    enforced_props = {}
    for col in context.scene.collection.children_recursive:
        if context.object.name in col.all_objects:
            for enforceable_prop in col.GUProps.enforce.enforceable_props:
                if getattr(col.GUProps.enforce, f"{enforceable_prop}_enforce"):
                    enforced_props[enforceable_prop] = True

    layout = self.layout
    layout.use_property_split = True
    if any(enforced_props.values()):
        layout.label(text="Some properties are enforced by Collections.", icon="INFO")

    obj = context.object
    obj_type = obj.type
    is_geometry = obj_type in {"MESH", "CURVE", "SURFACE", "META", "FONT", "VOLUME", "CURVES", "POINTCLOUD"}
    has_bounds = is_geometry or obj_type in {"LATTICE", "ARMATURE"}
    is_wire = obj_type in {"CAMERA", "EMPTY"}
    is_empty_image = obj_type == "EMPTY" and obj.empty_display_type == "IMAGE"
    is_dupli = obj.instance_type != "NONE"
    is_gpencil = obj_type == "GPENCIL"

    col = layout.column(heading="Show")
    col_name = col.column()
    col_name.prop(obj, "show_name", text="Name")
    col_name.enabled = not enforced_props.get("show_name", False)
    col_axis = col.column()
    col_axis.prop(obj, "show_axis", text="Axes")
    col_axis.enabled = not enforced_props.get("show_axis", False)

    # Makes no sense for cameras, armatures, etc.!
    # but these settings do apply to dupli instances
    if is_geometry or is_dupli:
        col_wireframe = col.column()
        col_wireframe.prop(obj, "show_wire", text="Wireframe")
        col_wireframe.enabled = not enforced_props.get("show_wire", False)
    if obj_type == "MESH" or is_dupli:
        col_edges = col.column()
        col_edges.prop(obj, "show_all_edges", text="All Edges")
        col_edges.enabled = not enforced_props.get("show_all_edges", False)
    if is_geometry:
        col_texture_space = col.column()
        col_texture_space.prop(obj, "show_texture_space", text="Texture Space")
        col_texture_space.enabled = not enforced_props.get("show_texture_space", False)
        col.prop(obj.display, "show_shadows", text="Shadow")
    col_in_front = col.column()
    col_in_front.prop(obj, "show_in_front", text="In Front")
    col_in_front.enabled = not enforced_props.get("show_in_front", False)
    # if obj_type == 'MESH' or is_empty_image:
    #    col.prop(obj, "show_transparent", text="Transparency")
    sub = layout.column()
    if is_wire:
        # wire objects only use the max. display type for duplis
        sub.active = is_dupli
    sub.prop(obj, "display_type", text="Display As")
    sub.enabled = not enforced_props.get("display_type", False)

    if is_geometry or is_dupli or is_empty_image or is_gpencil:
        # Only useful with object having faces/materials...
        col_color = col.column()
        col_color.prop(obj, "color")
        col_color.enabled = not enforced_props.get("color", False)

    if has_bounds:
        col = layout.column(align=False, heading="Bounds")
        col.use_property_decorate = False
        row = col.row(align=True)
        sub = row.row(align=True)
        sub.prop(obj, "show_bounds", text="")
        sub = sub.row(align=True)
        sub.active = obj.show_bounds or (obj.display_type == "BOUNDS")
        sub.prop(obj, "display_bounds_type", text="")
        row.prop_decorator(obj, "display_bounds_type")


draw_OBJECT_PT_DISPLAY.previous_draw = None


class GU_PG_collection_enforce_scene(PropertyGroup):
    active: BoolProperty(default=False)  # type: ignore


GUPropsCollection.__annotations__["enforce"] = PointerProperty(type=GU_PG_EnforceProps)
GUPropsScene.__annotations__["collection_enforce"] = PointerProperty(type=GU_PG_collection_enforce_scene)


def register():
    draw_OBJECT_PT_DISPLAY.previous_draw = bpy.types.OBJECT_PT_display.draw
    bpy.types.OBJECT_PT_display.draw = draw_OBJECT_PT_DISPLAY
    bpy.app.handlers.depsgraph_update_post.append(enforce)


def unregister():
    bpy.app.handlers.depsgraph_update_post.remove(enforce)
    bpy.types.OBJECT_PT_display.draw = draw_OBJECT_PT_DISPLAY.previous_draw
