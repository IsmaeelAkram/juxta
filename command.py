import discord


class Command:
    def __init__(str, name: str, description: str, aliases: list[str]):
        self.name = name
        self.description = description
        self.aliases = aliases

    async def handler(self, args: list[str], message: discord.Message):
        pass