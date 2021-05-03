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
import exceptions


class Utility(Plugin):
    def init(self):
        self.name = "Utility"
        self.slug = "utility"
        self.description = "Utilitarian commands"
        self.commands = [
            Command(
                name="!ping",
                description="Check bot status",
                usage="",
                handler=self.ping,
            ),
            Command(
                name="!debuginfo",
                description="Get debugging info (only for devs)",
                usage="",
                handler=self.debuginfo,
                hide_from_help=True,
            ),
            Command(
                name="!stats",
                description="Get debugging info (only for devs)",
                usage="",
                handler=self.stats,
                hide_from_help=True,
            ),
            Command(
                name="!pin",
                description="Pin message",
                usage="[message ID]",
                handler=self.pin,
            ),
            Command(
                name="!serverinfo",
                description="Get server info",
                usage="",
                handler=self.serverinfo,
            ),
        ]

    async def ping(self, args: list[str], message: discord.Message):
        await message.channel.send(
            embed=embed.Embed(
                title="🏓 Pong!",
                description=f"Server latency is **{round(self.client.latency)}ms**",
            )
        )

    async def debuginfo(self, args: list[str], message: discord.Message):
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

    async def stats(self, args: list[str], message: discord.Message):
        stats_embed = embed.Embed(title="📈 Stats")

        command_count = await self.client.redis.get("juxta:command_count")
        stats_embed.add_field(
            name="Commands Handled", value=command_count.decode("utf-8")
        )
        kick_count = await self.client.redis.get("juxta:kick_count")
        stats_embed.add_field(name="Users Kicked", value=kick_count.decode("utf-8"))
        ban_count = await self.client.redis.get("juxta:ban_count")
        stats_embed.add_field(name="Users Banned", value=ban_count.decode("utf-8"))
        warn_count = await self.client.redis.get("juxta:warn_count")
        stats_embed.add_field(name="Users Warned", value=kick_count.decode("utf-8"))
        stats_embed.add_field(name="Servers Managing", value=len(self.client.guilds))
        await message.channel.send(embed=stats_embed)
        await message.add_reaction("👌")

    async def pin(self, args: list[str], message: discord.Message):
        if len(args) < 2:
            raise exceptions.ArgsError
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

    async def serverinfo(self, args: list[str], message: discord.Message):
        server_info_embed = (
            embed.Embed(title=message.guild.name)
            .set_thumbnail(url=message.guild.icon_url)
            .add_field(name="Server ID", value=message.guild.id)
            .add_field(name="Owner", value=message.guild.owner.mention)
            .add_field(name="Member Count", value=message.guild.member_count)
            .add_field(name="Channel Count", value=len(message.guild.channels))
            .add_field(name="Role Count", value=len(message.guild.roles))
            .add_field(name="Created At", value=message.guild.created_at)
            .add_field(name="Region", value=message.guild.region)
            .add_field(
                name="System Channel", value=message.guild.system_channel.mention
            )
            .add_field(name="Rules Channel", value=message.guild.rules_channel.mention)
        )

        await message.channel.send(message.author.mention, embed=server_info_embed)
