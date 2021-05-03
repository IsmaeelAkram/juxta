import discord


class Plugin:
    def __init__(self, client: discord.Client):
        self.client = client
        self.name = ""
        self.slug = ""
        self.description = ""
        self.commands = []
        self.hide_from_help = False
        self.init()

    def init(self):
        pass

    async def on_message(self, message: discord.Message):
        pass

    async def on_guild_join(self, guild: discord.Guild):
        pass

    async def on_guild_remove(self, guild: discord.Guild):
        pass