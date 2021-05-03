import aioredis
import discord
from command import Command
from plugin import Plugin
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
        return await self.bot.redis.smembers(self.plugins_set)

    async def has_plugin(self, plugin: Plugin):
        if plugin.slug == "help":
            return True
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