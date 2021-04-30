from plugin import Plugin
from command import Command
from utils import embed
import discord
import log


class Moderation(Plugin):
    def __init__(self):
        self.name = "Moderation"
        self.description = "Moderation commands"
        self.commands = [
            Command(
                name="kick",
                description="Kick user",
                usage="[user]",
                handler=self.kick,
            ),
            Command(
                name="ban",
                description="Ban user",
                usage="[user]",
                handler=self.ban,
            ),
            Command(
                name="warn",
                description="Warn user",
                usage="[user] (optional reason)",
                handler=self.warn,
            ),
        ]

    async def kick(self, bot, args: list[str], message: discord.Message):
        self.redis.incr("juxta:kick_count")

    async def ban(self, bot, args: list[str], message: discord.Message):
        self.redis.incr("juxta:ban_count")

    async def warn(self, bot, args: list[str], message: discord.Message):
        self.redis.incr("juxta:warn_count")