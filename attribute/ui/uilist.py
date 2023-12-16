import bpy


class ATTRIBUTE_UL_gu_display(bpy.types.UIList):
    def draw_item(
        self, context, layout, data, item, icon, active_data, active_propname
    ):
        if item.name.startswith(".") or not item.name:
            return
        layout.label(text=item.name)

    def filter_items(self, context, data, propname):
        attributes = getattr(data, propname)
        filter_flags = []
        mesh_select_mode = context.scene.tool_settings.mesh_select_mode
        for attribute in attributes:
            filter_flags.append(1 << 0)
            if attribute.name == "position" or not attribute.name:
                continue
            if attribute.domain == "POINT" and mesh_select_mode[0]:
                filter_flags[-1] = self.bitflag_filter_item
            elif attribute.domain == "EDGE" and mesh_select_mode[1]:
                filter_flags[-1] = self.bitflag_filter_item
            elif attribute.domain == "FACE" and mesh_select_mode[2]:
                filter_flags[-1] = self.bitflag_filter_item

        filter_neworder = range(len(attributes))
        return filter_flags, filter_neworder
