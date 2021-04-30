class Command:
    def __init__(self, *, name: str, description: str, usage: str, handler: bool):
        self.name = name
        self.description = description
        self.usage = usage
        self.handler = handler