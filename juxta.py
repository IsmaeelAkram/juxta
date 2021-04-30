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
    async def on_ready(self):
        log.good("Connected to Discord")

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
        self.register_plugin(utility.Utility())
        self.register_plugin(moderation.Moderation())
        self.register_plugin(music.Music())

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
        for plugin in self.plugins:
            await plugin.on_message(message)
        if not message.content.startswith(self.PREFIX):
            return

        args = message.content.split(" ")
        command = await self.parse_command(args)
        if not command:
            return
        self.redis.incr("juxta:command_count")

        try:
            await command.handler(self, args, message)
        except PermissionError:
            await message.channel.send(
                embed=embed.SoftErrorEmbed(
                    f"You don't have permission to run `{self.PREFIX}{command.name}`!"
                )
            )
