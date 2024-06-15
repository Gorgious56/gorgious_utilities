import bpy


class GU_OT_print_all_users(bpy.types.Operator):
    bl_idname = "gu.print_all_users"
    bl_label = "Print All Users"
    bl_description = "Print the name of all users of this data block"
    bl_options = {"REGISTER", "UNDO"}
    name: bpy.props.StringProperty()  # type: ignore

    def invoke(self, context, event):
        self.name = context.object.name if context.object else ""
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        user_map = bpy.data.user_map()
        for data_block, users in user_map.items():
            if data_block.name == self.name:
                print(f"Data Block: {data_block}")
                for user in users:
                    print(f"  User: {user}")
        return {"FINISHED"}
