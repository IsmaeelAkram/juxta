import aioredis
import discord
from command import Command
from plugin import Plugin
import embed
import log


class GuildStorage:
    def __init__(self, bot, guild_id: int):
        self.bot = bot
        self.guild_id = guild_id
        self.plugins_set = f"juxta:guilds:{self.guild_id}:plugins"

    async def add_plugin(self, plugin_slug: str):
        return await self.bot.redis.sadd(self.plugins_set, plugin_slug)

    async def remove_plugin(self, plugin_slug: str):
        return await self.bot.redis.srem(self.plugins_set, plugin_slug)

    async def get_plugins(self):
        plugins = []
        plugin_slugs = await self.bot.redis.smembers(self.plugins_set)
        for plugin_slug in plugin_slugs:
            for plugin in self.bot.plugins:
                if plugin_slug == plugin.slug.encode("utf-8"):
                    plugins.append(plugin)
        return plugins

    async def has_plugin(self, plugin: Plugin):
        if not await self.bot.redis.sismember(self.plugins_set, plugin.slug):
            return False
        else:
            return True

    async def has_command(self, command: Command):
        guild_plugins = await self.get_plugins()
        for plugin in self.bot.plugins:
            if plugin.slug.encode("utf-8") in guild_plugins:
                if command in plugin.commands:
                    return True
        return False

    async def generate_main_help(self, guild_plugins: [Plugin]):
        help_embed = embed.Embed(
            author="Juxta Plugins Help",
            icon="https://raw.githubusercontent.com/IsmaeelAkram/juxta/master/art/Processor.png",
        ).set_thumbnail(
            url="https://raw.githubusercontent.com/IsmaeelAkram/juxta/master/art/Processor.png"
        )
        for plugin in guild_plugins:
            if not plugin.hide_from_help:
                help_embed.add_field(
                    name=plugin.name, value=f"`!help {plugin.name.lower()}`"
                )
        return help_embed

    async def generate_plugin_help(self, args: list[str], guild_plugins: [Plugin]):
        for plugin in guild_plugins:
            if plugin.slug == args[1].lower():
                if not plugin.hide_from_help:
                    plugin_commands = ""
                    for command in plugin.commands:
                        if command.hide_from_help == False:
                            if command.usage == "":
                                usage = ""
                            else:
                                usage = " " + command.usage
                            plugin_commands += (
                                f"`{command.name}{usage}`\n{command.description}\n\n"
                            )
                    return embed.Embed(
                        title=plugin.name + " Plugin",
                        description=plugin_commands,
                    ).set_thumbnail(
                        url="https://raw.githubusercontent.com/IsmaeelAkram/juxta/master/art/Processor.png"
                    )
