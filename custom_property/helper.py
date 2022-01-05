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
    try:
        prop_data_source = source.id_properties_ui(prop_name)
    except TypeError:
        return
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
