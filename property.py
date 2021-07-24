from bpy.types import(
    Operator,
)

from bpy.props import(
    EnumProperty,
)


def copy_all_custom_props(source, target):
    "Copies ALL custom props from source to target"
    for prop in source['_RNA_UI'].keys():
        copy_custom_prop(source, target, prop)


def copy_custom_prop(source, target, prop):
    "Copies custom prop from source to target"
    # Make sure the custom props dictionary is initialized (Mainly for empty objects) :
    rna_ui_id = '_RNA_UI'
    if rna_ui_id not in target.keys():
        target[rna_ui_id] = {}

    # Copy custom prop :
    target[prop] = source[prop]
    # Copy the subtype, min, max etc :
    try:
        target[rna_ui_id][prop] = source[rna_ui_id][prop].to_dict()
    except KeyError:
        # Custom prop is API defined. Don't mess with it.
        pass
    # "overridable" is a "special" attribute :
    target.property_overridable_library_set(
        f'["{prop}"]', source.is_property_overridable_library(f'["{prop}"]'))


def retrieve_props(self, context):
    """Retrieves all non read-only properties formatted to populate an EnumProperty"""
    retrieve_props.no_copy = "__DO_NOT_COPY_ANY_PROP"
    items = []
    ao = context.active_object

    [items.append((p.identifier, p.name, p.description))
        for p in ao.bl_rna.properties
        if not p.is_readonly]
    if '_RNA_UI' in ao.keys():
        [items.append((p, p, p))
            for p in ao.keys()
            if not p.startswith('_')  # Make sure it's not "private"
            if p in ao['_RNA_UI'].keys()  # Make sure it's not API defined
         ]
    items.sort(key=lambda e: e[1])
    items.insert(0, (retrieve_props.no_copy, "NONE", "Do not copy any property"))
    return items


class GU_OT_property_copy(Operator):
    """Copy Property"""
    bl_idname = "property.copy"
    bl_label = "Copy Any Property from active to selected"
    bl_settings = {'INTERNAL'}
    bl_options = {'UNDO', 'REGISTER'}

    prop_copy: EnumProperty(
        name="Copy Property",
        description="Choose which property to copy from active to selected.\n Silently passes if target object doesn't have property",
        items=retrieve_props,)

    @ classmethod
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
