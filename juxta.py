from plugins import utility
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
        log.good("Opened Redis database")
        return self.redis

    def stop(self):
        log.warning("Stopping...")
        self.redis.close()
        log.warning("Disconnected from Redis")

        self.loop.stop()

    # EVENTS
    async def on_ready(self):
        log.good("Juxta connected to Discord")

        self.REDIS_URL = os.getenv("REDIS_URL")
        self.PREFIX = os.getenv("PREFIX")

        self.plugins = []

        await self.open_db()

        self.loop.add_signal_handler(signal.SIGINT, lambda: self.stop())
        self.loop.add_signal_handler(signal.SIGTERM, lambda: self.stop())

        self.register_plugins()

        log.good("Juxta is ready")

    def register_plugins(self):
        self.register_plugin(utility.Utility())

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
        self.redis.incr("juxta:command_count")

        args = message.content.split(" ")
        command = await self.parse_command(args)
        if not command:
            return
        await command.handler(self, args, message)
