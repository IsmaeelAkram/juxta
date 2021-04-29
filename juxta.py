from command import Command
from cmds import ping
import discord
import asyncio
import aioredis as redis
import os
import log
import signal


class Juxta(discord.Client):
    async def open_db(self):
        self.db = await redis.create_redis_pool(self.REDIS_URL)
        log.good("Opened Redis database")
        return self.db

    def stop(self):
        log.warning("Stopping...")
        self.db.close()
        log.warning("Disconnected from Redis")

        self.loop.stop()

    # EVENTS
    async def on_ready(self):
        log.good("Juxta connected to Discord")

        self.REDIS_URL = os.getenv("REDIS_URL")
        self.PREFIX = os.getenv("PREFIX")

        self.commands = []

        await self.open_db()

        self.loop.add_signal_handler(signal.SIGINT, lambda: self.stop())
        self.loop.add_signal_handler(signal.SIGTERM, lambda: self.stop())

        self.register_commands()

        log.good("Juxta is ready")

    def register_commands(self):
        self.register_command(ping.PingCommand())

    def register_command(self, command: Command):
        log.info(f"Registered command '{command}'")
        self.commands.append(command)

    async def parse_command(self, args: list[str]):
        cmd = args[0].replace(self.PREFIX, "")
        for command in self.commands:
            if command.name == cmd:
                return command
            for alias in command.aliases:
                if alias == cmd:
                    return command
        return None

    async def on_message(self, message: discord.Message):
        if not message.content.startswith(self.PREFIX):
            return

        args = message.content.split(" ")
        command = await self.parse_command(args)
        if not command:
            return
        await command.handler(args, message)