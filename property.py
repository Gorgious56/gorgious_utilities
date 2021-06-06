from bpy.types import(
    Operator,
)

from bpy.props import(
    EnumProperty,
)


def retrieve_props(self, context):
    items = []
    ao = context.active_object

    [items.append((p.identifier, p.name, p.description))
     for p in ao.bl_rna.properties if not ao.is_property_readonly(p.identifier)]
    [items.append((p, p, p)) for p in ao.keys() if not p.startswith('_')]
    items.sort(key=lambda e: e[1])
    items.insert(0, ("___None", "NONE", "Do not copy any property"))
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
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        ao = context.active_object
        custom_prop = False
        if self.prop_copy in ao.keys():
            value = ao[self.prop_copy]
            custom_prop = True
        else:
            value = getattr(context.active_object, self.prop_copy, None)
        if value is not None:
            for obj in context.selected_objects:
                if custom_prop:
                    obj[self.prop_copy] = value
                else:
                    try:
                        setattr(obj, self.prop_copy, value)
                    except TypeError:
                        pass
        return {"FINISHED"}
