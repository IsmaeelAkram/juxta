from plugins import utility, moderation, music, help, welcome, logger
import embed
from discord_sentry_reporting import use_sentry
import plugin
import discord
import asyncio
import aioredis
import os
import log
import signal
import exceptions
import storage


class Juxta(discord.Client):
    async def open_db(self):
        self.redis = await aioredis.create_redis_pool(
            self.REDIS_URL, password=self.REDIS_PASS
        )
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
        self.REDIS_PASS = os.getenv("REDIS_PASS")
        self.REDIS_URL = os.getenv("REDIS_URL")
        self.SENTRY_URL = os.getenv("SENTRY_URL")

        self.plugins = []

        use_sentry(self, dsn=self.SENTRY_URL)
        await self.open_db()
        self.register_plugins()
        discord.opus.load_opus(os.getenv("OPUS_PATH"))
        if discord.opus.is_loaded():
            log.good("Opus loaded")
        else:
            raise discord.opus.OpusNotLoaded

        self.loop.add_signal_handler(signal.SIGINT, lambda: self.stop())
        self.loop.add_signal_handler(signal.SIGTERM, lambda: self.stop())

        # await self.change_presence(
        #     activity=discord.Activity(
        #         name="bug reports", type=discord.ActivityType.listening
        #     )
        # )
        # log.good("Presence set")

        log.good("Juxta is ready")

    def register_plugins(self):
        self.register_plugin(utility.Utility(self))
        self.register_plugin(moderation.Moderation(self))
        self.register_plugin(music.Music(self))
        self.register_plugin(help.Help(self))
        self.register_plugin(welcome.Welcome(self))
        self.register_plugin(logger.Logger(self))

    def register_plugin(self, plugin: plugin.Plugin):
        log.info(f"Registered plugin '{plugin.name}'")
        self.plugins.append(plugin)

    async def parse_command(self, args: list):
        for plugin in self.plugins:
            for command in plugin.commands:
                if args[0] == command.name:
                    return (plugin, command)
        return None

    async def on_message(self, message: discord.Message):
        if not message.content.startswith("!"):
            return

        args = message.content.split(" ")
        (plugin, command) = await self.parse_command(args)
        if not command:
            return

        guild_storage = storage.GuildStorage(self, message.guild.id)
        if await guild_storage.has_plugin(plugin):
            self.redis.incr("juxta:command_count")
            try:
                await command.handler(args, message)
            except PermissionError as e:
                log.warning(e)
                await message.channel.send(
                    message.author.mention,
                    embed=embed.SoftErrorEmbed(
                        f"You don't have permission to run `{command.name}`!"
                    ),
                )
            except exceptions.ArgsError as e:
                log.warning(e)
                if command.usage == "":
                    command_usage = command.usage
                else:
                    command_usage = " " + command.usage
                await message.channel.send(
                    message.author.mention,
                    embed=embed.SoftErrorEmbed(
                        f"You're missing arguments!\nUsage: `{command.name}{command_usage}`"
                    ),
                )
            except exceptions.NoVoiceChannelError as e:
                await message.channel.send(
                    message.author.mention,
                    embed=embed.SoftErrorEmbed(f"You're not in a voice channel!"),
                )
            except exceptions.AlreadyInVoiceChannelError as e:
                await message.channel.send(
                    message.author.mention,
                    embed=embed.SoftErrorEmbed(f"I'm already in your voice channel!"),
                )
            except exceptions.BotNotInVoiceChannelError as e:
                await message.channel.send(
                    message.author.mention,
                    embed=embed.SoftErrorEmbed(f"I'm not in a voice channel!"),
                )
        for plugin in self.plugins:
            if await guild_storage.has_plugin(plugin):
                await plugin.on_message(message)

    async def on_guild_join(self, guild: discord.Guild):
        self.redis.sadd("juxta:guilds", guild.id)
        guild_storage = storage.GuildStorage(self, guild.id)
        await guild_storage.add_plugin("welcome")
        await guild_storage.add_plugin("help")

        for plugin in self.plugins:
            if await guild_storage.has_plugin(plugin):
                await plugin.on_guild_join(guild)

    async def on_guild_remove(self, guild: discord.Guild):
        self.redis.srem("juxta:guilds", guild.id)
        guild_storage = storage.GuildStorage(self, guild.id)
        for plugin in self.plugins:
            if await guild_storage.has_plugin(plugin):
                await plugin.on_guild_remove(guild)