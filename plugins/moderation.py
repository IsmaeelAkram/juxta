from plugin import Plugin
from command import Command
import embed
import discord
import log


class Moderation(Plugin):
    def init(self):
        self.name = "Moderation"
        self.slug = "moderation"
        self.description = "Moderation commands"
        self.commands = [
            Command(
                name="!kick",
                description="Kick user",
                usage="[user]",
                handler=self.kick,
            ),
            Command(
                name="!ban",
                description="Ban user",
                usage="[user]",
                handler=self.ban,
            ),
            Command(
                name="!warn",
                description="Warn user",
                usage="[user] (optional reason)",
                handler=self.warn,
            ),
        ]

    async def kick(self, args: list[str], message: discord.Message):
        self.redis.incr("juxta:kick_count")

    async def ban(self, args: list[str], message: discord.Message):
        self.redis.incr("juxta:ban_count")

    async def warn(self, args: list[str], message: discord.Message):
        self.redis.incr("juxta:warn_count")