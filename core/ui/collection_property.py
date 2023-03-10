def draw(layout, collection_property):
    collection_property_holder = collection_property.id_data.path_resolve(
        ".".join(collection_property.path_from_id().rsplit(".", 1)[:1])
    )
    collection_property_name = repr(collection_property).split(".")[-1]
    column = layout.column(align=True)
    column.context_pointer_set("collection_property_holder", collection_property_holder)
    op_add = column.operator("gu.collection_property_operations", icon="ADD", text="")
    op_add.collection_property_name = collection_property_name
    op_add.operation = "ADD"
    for i, element in enumerate(getattr(collection_property_holder, collection_property_name)):
        row = column.row(align=True)
        if hasattr(element, "draw"):
            element.draw(row)
        else:
            for ann in element.__annotations__:
                if element.bl_rna.properties[ann].is_hidden:
                    continue
                row.prop(element, ann, text=f"{element.bl_rna.properties[ann].name}")
        op_remove = row.operator("gu.collection_property_operations", icon="REMOVE", text="")
        op_remove.collection_property_name = collection_property_name
        op_remove.operation = "REMOVE"
        op_remove.index = i
