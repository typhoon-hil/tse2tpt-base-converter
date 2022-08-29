class Parentable:
    """ Models entities which have parent. """
    def __init__(self, parent, *args, **kwargs) -> None:
        """ Initialize an object. """
        super().__init__(*args, **kwargs)

        self.parent = parent


class Nameable:
    """ Models entities which have name. """
    def __init__(self, name, *args, **kwargs) -> None:
        """ Initialize an object. """
        super().__init__(*args, **kwargs)

        self.name = name
