import discord
from command import Command
import random


class PingCommand(Command):
    def __init__(self):
        self.name = "ping"
        self.description = "Checks bot status"
        self.aliases = ["pong"]

    async def handler(self, args: list[str], message: discord.Message):
        pong_message = random.choice(["Pong!", "Hey!", "Hello!"])
        await message.channel.send(f"{message.author.mention} {pong_message}")