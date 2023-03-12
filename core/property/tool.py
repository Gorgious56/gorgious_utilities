def get_parent(item):
    return item.id_data.path_resolve(".".join(item.path_from_id().rsplit(".", 1)[:1]))


def display_name(holder, attribute):
    return holder.bl_rna.properties[attribute].name.replace("_", " ").title()
