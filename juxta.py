from plugins import utility, moderation, music
from utils import embed
import plugin
import discord
import asyncio
import aioredis
import os
import log
import signal


class Juxta(discord.Client):
    async def open_db(self):
        self.redis = await aioredis.create_redis_pool(self.REDIS_URL)
        log.good("Connected to Redis")
        return self.redis

    def stop(self):
        log.warning("Stopping...")
        self.redis.close()
        log.warning("Disconnected from Redis")

        self.loop.stop()

    # EVENTS
    async def on_connect(self):
        log.good("Connected to Discord")

    async def on_ready(self):
        self.REDIS_URL = os.getenv("REDIS_URL")
        self.PREFIX = os.getenv("PREFIX")

        self.plugins = []

        await self.open_db()
        self.register_plugins()
        discord.opus.load_opus(os.getenv("OPUS_PATH"))
        if discord.opus.is_loaded():
            log.good("Opus loaded")

        self.loop.add_signal_handler(signal.SIGINT, lambda: self.stop())
        self.loop.add_signal_handler(signal.SIGTERM, lambda: self.stop())

        log.good("Juxta is ready")

    def register_plugins(self):
        self.register_plugin(utility.Utility(self))
        self.register_plugin(moderation.Moderation(self))
        self.register_plugin(music.Music(self))

    def register_plugin(self, plugin: plugin.Plugin):
        log.info(f"Registered plugin '{plugin.name}'")
        self.plugins.append(plugin)

    async def parse_command(self, args: list[str]):
        cmd = args[0].replace(self.PREFIX, "")

        for plugin in self.plugins:
            for command in plugin.commands:
                if cmd == command.name:
                    return command

    async def on_message(self, message: discord.Message):
        if not message.content.startswith(self.PREFIX):
            return

        args = message.content.split(" ")
        command = await self.parse_command(args)
        if not command:
            return
        self.redis.incr("juxta:command_count")

        try:
            await command.handler(self, args, message)
        except PermissionError as e:
            log.warning(e)
            await message.channel.send(
                embed=embed.SoftErrorEmbed(
                    f"You don't have permission to run `{self.PREFIX}{command.name}`!"
                )
            )
        except TypeError as e:
            log.warning(e)
            if command.usage == "":
                command_usage = command.usage
            else:
                command_usage = " " + command.usage
            await message.channel.send(
                embed=embed.SoftErrorEmbed(
                    f"You're missing arguments!\nUsage: `{self.PREFIX}{command.name}{command_usage}`"
                )
            )
        for plugin in self.plugins:
            await plugin.on_message(message)

    async def on_guild_join(self, guild: discord.Guild):
        for plugin in self.plugins:
            await plugin.on_guild_join(guild)

    async def on_guild_leave(self, guild: discord.Guild):
        for plugin in self.plugins:
            await plugin.on_guild_leave(guild)