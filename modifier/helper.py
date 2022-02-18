import bpy
from gorgious_utilities.custom_property.helper import get_all_ui_props
from gorgious_utilities.driver.helper import (
    add_driver_to,
)
from gorgious_utilities.event.watcher import (
    parent_watchers,
)


def get_geometry_nodes_groups(self, context):
    get_geometry_nodes_groups.groups = []
    for ng in [ng for ng in bpy.data.node_groups if ng.bl_idname == "GeometryNodeTree"]:
        get_geometry_nodes_groups.groups.append((ng.name,) * 3)
    return get_geometry_nodes_groups.groups


def get_geometry_node_modifier_names(self, context):
    mods = [m for m in context.active_object.modifiers if m.type == "NODES"]
    return ((mod.name,) * 3 for mod in mods)


def get_output_attributes(self, context):
    o = context.active_object
    mod = o.modifiers[self.mod_name]
    node_tree = mod.node_group
    # output_node = next(n for n in node_tree.nodes if isinstance(n, bpy.types.NodeGroupOutput))
    # inputs = output_node.inputs
    # for output in inputs:
    #     print(output)

    # for k, v in mod.items():
    #     prop_rna = (mod.id_properties_ui(k))
    #     print(prop_rna.as_dict())

    for ui_prop in get_all_ui_props(mod):
        if ui_prop.startswith("Output"):
            yield (ui_prop,) * 3


def mod_equality(mod1, mod2, ignore=["name"]):
    return all(getattr(mod1, prop, True) == getattr(mod2, prop, False) for prop in mod1.bl_rna.properties.keys())


def same_modifier_stack_ordered(obj1, obj2):
    return all(mod_equality(m, obj2.modifiers[i]) for i, m in enumerate(obj1.modifiers))


def are_modifiers_same(mods_before, mods_after):
    """
    Return True if the modifiers are the same
    """
    if len(mods_before) != len(mods_after):
        return False
    for m1, m2 in zip(mods_before, mods_after):
        if m1.name != m2.name or m1.type != m2.type:
            return False
    return True


def copy_modifiers(from_object, to_objects, replace, drive):
    from_mods = from_object.modifiers
    for obj in to_objects:
        if not obj or obj == from_object:
            continue
        if replace:
            obj.modifiers.clear()
            for from_mod in from_mods:
                obj.modifiers.new(name=from_mod.name, type=from_mod.type)
        for mod in obj.modifiers:
            for from_mod in from_mods:
                if not (from_mod.name == mod.name and from_mod.type == mod.type):
                    continue
                for attr, value in mod.bl_rna.properties.items():
                    if value.is_readonly:
                        continue
                    if replace:
                        setattr(mod, attr, getattr(from_mod, attr))
                    if attr == "show_expanded" or not value.is_animatable:
                        continue
                    if drive:
                        if getattr(value, "is_array", False):
                            for dim in range(value.array_length):
                                attr_dim = attr + "[" + str(dim) + "]"
                                add_driver_to(
                                    mod,
                                    {"attr": attr, "dim": dim},
                                    ((attr, "OBJECT", from_object, 'modifiers["' + mod.name + '"].' + attr_dim),),
                                    None,
                                )
                        else:
                            add_driver_to(
                                mod,
                                attr,
                                ((attr, "OBJECT", from_object, 'modifiers["' + mod.name + '"].' + attr),),
                                None,
                            )


def are_any_objs_synched(objs):
    return any(parent_watchers(obj) for obj in objs)


def remove_drivers(obj):
    for mod in obj.modifiers:
        for attr, value in mod.bl_rna.properties.items():
            if value.is_readonly or attr == "show_expanded" or not value.is_animatable:
                continue
            if getattr(value, "is_array", False):
                for dim in range(value.array_length):
                    attr_dim = attr + "[" + str(dim) + "]"
                    mod.driver_remove(attr, dim)
            else:
                mod.driver_remove(attr)


def remove_drivers_objs(objs):
    for obj in objs:
        remove_drivers(obj)
    bpy.ops.clean.faulty_drivers()
