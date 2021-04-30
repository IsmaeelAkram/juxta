from plugin import Plugin
from command import Command
from utils import embed
import discord
import random
import requests
import aioredis
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
                hide_from_help=True,
            ),
            Command(
                name="stats",
                description="Get debugging info (only for devs)",
                usage="",
                handler=self.stats,
                hide_from_help=True,
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
                handler=self.help,
            ),
            Command(
                name="pin",
                description="Pin message",
                usage="[message ID]",
                handler=self.pin,
            ),
        ]

    async def ping(self, client, args: list[str], message: discord.Message):
        await message.channel.send(
            embed=embed.Embed(
                title="🏓 Pong!",
                description=f"Server latency is **{round(client.latency)}ms**",
            )
        )

    async def debuginfo(self, client, args: list[str], message: discord.Message):
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

    async def stats(self, client, args: list[str], message: discord.Message):
        stats_embed = embed.Embed(title="📈 Stats")

        command_count = await client.redis.get("juxta:command_count")
        stats_embed.add_field(
            name="Commands Handled", value=command_count.decode("utf-8")
        )
        kick_count = await client.redis.get("juxta:kick_count")
        stats_embed.add_field(name="Users Kicked", value=kick_count.decode("utf-8"))
        ban_count = await client.redis.get("juxta:ban_count")
        stats_embed.add_field(name="Users Banned", value=ban_count.decode("utf-8"))
        warn_count = await client.redis.get("juxta:warn_count")
        stats_embed.add_field(name="Users Warned", value=kick_count.decode("utf-8"))
        stats_embed.add_field(name="Servers Managing", value=len(client.guilds))
        await message.channel.send(embed=stats_embed)
        await message.add_reaction("👌")

    async def help(self, client, args: list[str], message: discord.Message):
        help_embed = embed.Embed(
            title="Juxta Help",
            description="Juxta is a high-performance, easy-to-use Discord bot with an abundance of features. This help prompt is meant to be a guide on the commands Juxta has to offer, and how to use them.",
        ).set_thumbnail(
            url="https://raw.githubusercontent.com/IsmaeelAkram/juxta/master/art/Processor.png"
        )
        await message.channel.send(embed=help_embed)

        for plugin in client.plugins:
            plugin_commands = ""
            for command in plugin.commands:
                if command.hide_from_help == False:
                    if command.usage == "":
                        usage = ""
                    else:
                        usage = " " + command.usage
                    plugin_commands += f"`{client.PREFIX}{command.name}{usage}`\n{command.description}\n\n"
            await message.channel.send(
                embed=embed.Embed(
                    title=plugin.name, description=plugin_commands
                ).set_thumbnail(
                    url="https://raw.githubusercontent.com/IsmaeelAkram/juxta/master/art/Processor.png"
                )
            )

    async def pin(self, client, args: list[str], message: discord.Message):
        if len(args) < 2:
            raise TypeError
            return

        message_id = args[1]
        try:
            message = await message.channel.fetch_message(message_id)
            await message.pin()
        except discord.errors.NotFound:
            await message.channel.send(
                embed=embed.SoftErrorEmbed(
                    "That message was not found! Right-click the message and press `Copy ID`."
                )
            )
