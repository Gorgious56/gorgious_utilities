def show_message_operator(self, body, mode="INFO"):
    self.report({mode}, body)


def show_message_box(context, body="", title="Message Box", icon="INFO"):
    def draw(self, context):
        if isinstance(body, (list, tuple)):
            for item in body:
                self.layout.label(text=item)
        else:
            self.layout.label(text=body)

    context.window_manager.popup_menu(draw, title=title, icon=icon)
