import bpy
from gorgious_utilities.collection.helper import (
    get_family_down,
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
        return context.collection

    def execute(self, context):
        col_parent = context.collection
        bpy.ops.object.select_all(action="DESELECT")

        all_converted_objects = []
        remove_objs = []
        instances = []

        for obj in col_parent.all_objects:
            if obj.name not in context.view_layer.objects:
                continue
            elif obj.type == "MESH":
                if not self.join_wire_objects and obj.display_type == "WIRE":
                    remove_objs.append(obj)
                    continue
                # obj.select_set(True)
                all_converted_objects.append(obj)
            elif obj.type == "EMPTY":
                if obj.instance_type == "COLLECTION":
                    instances.append(obj)
            elif obj.type == "CURVE":
                curve = obj.data
                if curve.bevel_depth > 0 or obj.modifiers:
                    all_converted_objects.append(obj)
                else:
                    remove_objs.append(obj)
            else:
                remove_objs.append(obj)

        if instances:
            [obj.select_set(True) for obj in instances]
            bpy.ops.object.duplicates_make_real({"selected_objects": instances})
            all_converted_objects.extend(context.selected_objects)

        bpy.ops.object.make_single_user(
            {"selected_objects": all_converted_objects},
            object=True,
            obdata=True,
            material=False,
            animation=False,
        )

        # https://developer.blender.org/T93188
        context.view_layer.objects.active = all_converted_objects[0]
        [o.select_set(True) for o in all_converted_objects]
        bpy.ops.object.convert(target="MESH")

        # Delete all Empty Objects
        bpy.data.batch_remove(remove_objs)
        bpy.data.batch_remove(instances)

        colls_to_remove = []

        for coll in get_family_down(col_parent, include_parent=False):
            if self.col_name.lower() in coll.name.lower():
                obs = [o for o in coll.objects if o.users == 1]
                while obs:
                    bpy.data.objects.remove(obs.pop())
            else:
                obs = [o for o in coll.objects]
                while obs:
                    col_parent.objects.link(obs.pop())
            colls_to_remove.append(coll)

        bpy.data.batch_remove(colls_to_remove)

        join_objects = [obj for obj in col_parent.all_objects if obj.type == "MESH"]

        if join_objects:
            bpy.ops.object.join({"object": join_objects[0], "selected_editable_objects":join_objects})
            join_objects[0].name = col_parent.name

        return {"FINISHED"}


if __name__ == "__main__":
    bpy.utils.register_class(GU_OT_collection_destructively_join_meshes)
