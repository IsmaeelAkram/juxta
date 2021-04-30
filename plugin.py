import discord


class Plugin:
    def __init__(self):
        self.name = ""
        self.description = ""
        self.commands = []

    async def on_message(self, message: discord.Message):
        pass

    async def on_guild_join(self, guild: discord.Guild):
        pass

    async def on_guild_remove(self, guild: discord.Guild):
        pass