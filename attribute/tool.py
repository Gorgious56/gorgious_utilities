def get_bmesh_domain(domain):
    if domain == "POINT":
        return "verts"
    elif domain == "EDGE":
        return "edges"
    elif domain == "FACE":
        return "faces"


def get_layer_type(data_type):
    if data_type == "FLOAT":
        return "float"
    elif data_type == "INT":
        return "int"
    elif data_type == "STRING":
        return "string"
    elif data_type == "FLOAT_VECTOR":
        return "float_vector"
    elif data_type == "FLOAT_COLOR":
        return "float_color"
    elif data_type == "BOOLEAN":
        return "int"
    else:
        raise Exception(f"Data type '{data_type}' not supported")


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
