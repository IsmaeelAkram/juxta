from plugin import Plugin
from command import Command
from utils import embed
import discord
import random
import requests
import os
import sys
import log


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
                description="Get debugging info (only for devs)",
                usage="",
                handler=self.debuginfo,
            ),
            Command(
                name="help",
                description="Shows all commands, descriptions, and usages",
                usage="",
                handler=self.help,
            ),
            Command(
                name="commands",
                description="Alias for !help",
                usage="",
                handler=self.commands,
            ),
        ]

    async def ping(self, bot, args: list[str], message: discord.Message):
        pong_message = random.choice(["Pong!", "Hey!", "Hello!"])
        await message.channel.send(f"{message.author.mention} {pong_message}")

    async def debuginfo(self, bot, args: list[str], message: discord.Message):
        if message.author.id != 460117198795702272:
            raise PermissionError
        debug_info = embed.Embed(title="🖥 Debug Info")
        debug_info.add_field(
            name="Public IP", value=requests.get("https://api.ipify.org").text
        )
        debug_info.add_field(name="Working Dir", value=os.getcwd())
        debug_info.add_field(name="Python Version", value=sys.version.split(" ")[0])
        await message.author.send(embed=debug_info)
        await message.add_reaction("✅")

    async def help(self, bot, args: list[str], message: discord.Message):
        help_embed = embed.Embed(
            title="Juxta Help",
            description="Juxta is a high-performance, easy-to-use Discord bot with an abundance of features. This help prompt is meant to be a guide on the commands Juxta has to offer, and how to use them.",
        )
        await message.channel.send(embed=help_embed)

        for plugin in bot.plugins:
            plugin_commands = ""
            for command in plugin.commands:
                if command.usage == "":
                    usage = ""
                else:
                    usage = " " + command.usage
                plugin_commands += (
                    f"`{bot.PREFIX}{command.name}{usage}` — **{command.description}**\n"
                )
            await message.channel.send(
                embed=embed.Embed(title=plugin.name, description=plugin_commands)
            )

    async def commands(self, bot, args: list[str], message: discord.Message):
        await self.help(bot, args, message)