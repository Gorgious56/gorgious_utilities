import bpy


class GU_OT_modifier_select_used_booleans(bpy.types.Operator):
    """Selects all the boolean objects and collections used by this object's modifiers"""

    bl_label = "Select Used Booleans"
    bl_idname = "select.used_booleans"
    bl_options = {"REGISTER", "UNDO"}

    extend: bpy.props.BoolProperty(
        name="Extend",
        default=False,
    )

    select_hidden: bpy.props.BoolProperty(
        name="Select Hidden",
        default=True,
    )

    select_disabled: bpy.props.BoolProperty(
        name="Select Disabled",
        default=True,
    )

    select_unselectable: bpy.props.BoolProperty(
        name="Select Unselectable",
        default=True,
    )

    select_operand: bpy.props.EnumProperty(
        name="Select Operand",
        items=(
            ("Both",) * 3,
            ("Object",) * 3,
            ("Collection",) * 3,
        ),
        default="Both",
    )

    @classmethod
    def poll(cls, context):
        return context.selected_objects

    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type != "MESH":
                continue
            mods = obj.modifiers
            used_bools = set()
            for mod in mods:
                if mod.type != "BOOLEAN":
                    continue

                if mod.operand_type == "COLLECTION" and mod.collection is not None:
                    if self.select_operand in ("Both", "Collection"):
                        used_bools.update(mod.collection.all_objects)
                elif mod.object is not None:
                    if self.select_operand in ("Both", "Object"):
                        used_bools.add(mod.object)

            for used_bool in used_bools:
                # Logic from https://blenderartists.org/t/blender-2-8-python-hide-unhide-objects/1141228/2

                if (not used_bool.hide_viewport and not used_bool.visible_get()) and self.select_hidden:
                    # Hidden with the eye icon
                    used_bool.hide_set(False)

                if used_bool.hide_viewport:
                    used_bool.hide_viewport = False  #  Toggle to test visibility

                    if used_bool.visible_get() and self.select_disabled:
                        # Hidden with the monitor icon
                        used_bool.hide_viewport = False
                    elif self.select_disabled and self.select_hidden:
                        # Hidden both ways
                        used_bool.hide_viewport = False
                        used_bool.hide_set(False)
                    else:
                        used_bool.hide_viewport = True  #  Toggle back

                if used_bool.hide_select and self.select_unselectable:
                    used_bool.hide_select = False

                used_bool.select_set(True)

            obj.select_set(self.extend)
            if not self.extend and context.selected_objects:
                context.view_layer.objects.active = context.selected_objects[0]

        return {"FINISHED"}
