from bpy.types import (
    Operator,
)

from bpy.props import (
    EnumProperty,
)


def get_all_ui_props(obj):
    items = obj.items()
    rna_properties = {prop.identifier for prop in obj.bl_rna.properties if prop.is_runtime}
    for k, _ in items:
        if k in rna_properties:
            continue
        yield k


def copy_all_custom_props(source, target):
    "Copies ALL custom props from source to target"
    target.id_properties_ensure()
    source.id_properties_ensure()
    for prop_name in get_all_ui_props(source):
        copy_custom_prop(source, target, prop_name, ensure=False)


def copy_custom_prop(source, target, prop_name, ensure=True):
    "Copies custom prop from source to target"
    if ensure:
        target.id_properties_ensure()
        source.id_properties_ensure()
    prop_data_source = source.id_properties_ui(prop_name)
    target[prop_name] = source[prop_name]
    prop_data_target = target.id_properties_ui(prop_name)
    prop_data_target.update_from(prop_data_source)
    target.property_overridable_library_set(
        f'["{prop_name}"]', source.is_property_overridable_library(f'["{prop_name}"]')
    )


def retrieve_props(self, context):
    """Retrieves all non read-only properties formatted to populate an EnumProperty"""
    retrieve_props.no_copy = "__DO_NOT_COPY_ANY_PROP"
    items = []
    ao = context.active_object

    for p in ao.bl_rna.properties:
        if p.is_readonly:
            continue
        items.append((p.identifier, p.name, p.description))
    if "_RNA_UI" in ao.keys():
        [
            items.append((p, p, p))
            for p in ao.keys()
            if not p.startswith("_")  # Make sure it's not "private"
            if p in ao["_RNA_UI"].keys()  # Make sure it's not API defined
        ]
    items.sort(key=lambda e: e[1])
    items.insert(0, (retrieve_props.no_copy, "NONE", "Do not copy any property"))
    return items


class GU_OT_property_copy(Operator):
    """Copy Property"""

    bl_idname = "property.copy"
    bl_label = "Copy Any Property from active to selected"
    bl_settings = {"INTERNAL"}
    bl_options = {"UNDO", "REGISTER"}

    prop_copy: EnumProperty(
        name="Copy Property",
        description="Choose which property to copy from active to selected.\n Silently passes if target object doesn't have property",
        items=retrieve_props,
    )

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and len(context.selected_objects) > 0

    def invoke(self, context, event):
        # Reset prop to prevent random mishaps :
        self.prop_copy = retrieve_props.no_copy
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        if self.prop_copy == retrieve_props.no_copy:
            return {"FINISHED"}
        ao = context.active_object
        if self.prop_copy in ao.keys():
            for obj in context.selected_objects:
                if ao == obj:
                    continue
                copy_custom_prop(ao, obj, self.prop_copy)
        else:
            value = getattr(ao, self.prop_copy, None)
            for obj in context.selected_objects:
                if ao == obj:
                    continue
                try:
                    setattr(obj, self.prop_copy, value)
                except TypeError as e:
                    # Edge case : Only empties can have an instance_type of 'COLLECTION'
                    print(f"Could not copy property from {ao.name} to {obj.name}\n{e}")
                except AttributeError as e:
                    # For some reason some properties are readonly despite is_readonly being False
                    print(f"Could not copy property from {ao.name} to {obj.name}\n{e}")

        return {"FINISHED"}
