import discord


class Plugin:
    def __init__(self):
        self.name = ""
        self.description = ""
        self.commands = []

    async def on_message(self, message: discord.Message):
        pass