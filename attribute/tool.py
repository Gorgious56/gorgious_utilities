def get_bmesh_domain(bm, domain):
    if domain == "POINT":
        return bm.verts
    elif domain == "EDGE":
        return bm.edges
    elif domain == "FACE":
        return bm.faces


def get_attribute_size_from_value(value):
    if isinstance(value, str):
        return 1
    try:
        return len(value)
    except TypeError:
        return 1


def get_attribute_size_and_name_from_attribute(attribute):
    first_attribute = attribute.data[0]
    attr_name = get_attribute_data_name(first_attribute)
    if attr_name is None:
        return
    return get_attribute_size_from_value(getattr(first_attribute, attr_name)), attr_name


def get_attribute_data_name(attribute_member):
    for attr_name in ("value", "vector", "color"):
        if hasattr(attribute_member, attr_name):
            return attr_name
    return None
