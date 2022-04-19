class GU_Menu:
    appends = {}
    prepends = {}

    @classmethod
    def register(cls):
        for menu, draw in cls.appends.items():
            menu.append(draw)
        for menu, draw in cls.prepends.items():
            menu.prepend(draw)

    @classmethod
    def unregister(cls):
        for menu, draw in cls.appends.items():
            menu.remove(draw)
        for menu, draw in cls.prepends.items():
            menu.remove(draw)
