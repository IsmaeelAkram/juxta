class Command:
    def __init__(
        self, *, name: str, description: str, usage: str, handler, hide_from_help=False
    ):
        self.name = name
        self.description = description
        self.usage = usage
        self.handler = handler
        self.hide_from_help = hide_from_help