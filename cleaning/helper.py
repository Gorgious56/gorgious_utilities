import bpy


def retrieve_data_to_clear(self, context):
    retrieve_data_to_clear.all = "All"
    items = [(retrieve_data_to_clear.all,) * 3]
    for d in dir(bpy.data):
        if "bpy_prop_collection" in str(type(getattr(bpy.data, d))):
            items.append((d, d.capitalize(), d))
    return items
