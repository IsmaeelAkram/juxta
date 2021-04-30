from plugin import Plugin
from command import Command
from utils import embed
import discord
import log


class Welcome(Plugin):
    def __init__(self, client: discord.Client):
        self.client = client
        self.name = "Welcome"
        self.description = ""
        self.commands = []

    async def on_guild_join(self, guild: discord.Guild):
        pass