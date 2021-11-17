import bpy
from gorgious_utilities.collection.helper import (
    get_all_children,
)


class GU_OT_collection_destructively_join_meshes(bpy.types.Operator):
    """Destructively applies modifiers, converts curves and instances, removes boolean collections, and join meshes"""

    bl_idname = "collection.destructively_join_meshes"
    bl_label = "Destructively join meshes"
    bl_options = {"UNDO"}

    col_name: bpy.props.StringProperty(name="Col Name", default="BOOL")
    join_wire_objects: bpy.props.BoolProperty(name="Join Wire Objects", default=False)

    @classmethod
    def poll(cls, context):
        return context.selected_objects

    def execute(self, context):
        col_parent = context.collection
        bpy.ops.object.select_all(action="DESELECT")

        all_converted_objects = []
        remove_objs = []
        instances = []

        for obj in col_parent.all_objects:
            if obj.name not in context.view_layer.objects:
                continue
            if obj.type == "MESH":
                if not self.join_wire_objects and obj.display_type == "WIRE":
                    remove_objs.append(obj)
                    continue
                obj.select_set(True)
                all_converted_objects.append(obj)
                continue
            elif obj.type == "EMPTY" and obj.instance_type == "COLLECTION":
                instances.append(obj)
                continue
            elif obj.type == "CURVE":
                curve = obj.data
                if curve.bevel_depth > 0 or obj.modifiers:
                    obj.select_set(True)
                    all_converted_objects.append(obj)
                else:
                    remove_objs.append(obj)
            else:
                remove_objs.append(obj)

        context.view_layer.objects.active = context.selected_objects[0]
        bpy.ops.object.make_single_user(object=True, obdata=True, material=False, animation=False)
        bpy.ops.object.convert(target="MESH")
        bpy.ops.object.select_all(action="DESELECT")

        if instances:
            ctx = context.copy()
            ctx["object"] = instances[0]
            ctx["active_object"] = instances[0]
            ctx["selected_objects"] = instances
            ctx["selected_editable_objects"] = instances
            bpy.ops.object.duplicates_make_real(ctx)

        # Delete all Empty Objects
        while remove_objs:
            bpy.data.objects.remove(remove_objs.pop())
        while instances:
            bpy.data.objects.remove(instances.pop())

        all_child_collections = get_all_children(col_parent)

        for coll in all_child_collections:
            if coll == col_parent:
                continue
            if coll:
                if self.col_name.lower() in coll.name.lower():
                    obs = [o for o in coll.objects if o.users == 1]
                    while obs:
                        bpy.data.objects.remove(obs.pop())
                else:
                    obs = [o for o in coll.objects]
                    while obs:
                        col_parent.objects.link(obs.pop())

                bpy.data.collections.remove(coll)

        join_objects = [obj for obj in col_parent.all_objects if obj.type == "MESH"]

        if join_objects:
            ctx = context.copy()
            o = join_objects[0]
            ctx["object"] = o
            ctx["active_object"] = o
            ctx["selected_objects"] = join_objects
            ctx["selected_editable_objects"] = join_objects
            bpy.ops.object.join(ctx)

            o.name = col_parent.name

        return {"FINISHED"}


if __name__ == "__main__":
    bpy.utils.register_class(GU_OT_collection_destructively_join_meshes)