from plugin import Plugin
from command import Command
import discord
import random


class Utility(Plugin):
    def __init__(self):
        self.name = "Utility"
        self.description = "Utilitarian commands"
        self.commands = [
            Command(
                name="ping", description="Check bot status", usage="", handler=self.ping
            ),
            Command(
                name="debuginfo",
                description="Get debugging info (only for bot admins)",
                usage="",
                handler=self.debuginfo,
            ),
        ]

    async def ping(self, bot, args: list[str], message: discord.Message):
        pong_message = random.choice(["Pong!", "Hey!", "Hello!"])
        await message.channel.send(f"{message.author.mention} {pong_message}")
        return True

    async def debuginfo(self, bot, args: list[str], message: discord.Message):
        return True