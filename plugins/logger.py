from plugin import Plugin
from command import Command
import discord
import embed
import storage


class Logger(Plugin):
    def init(self):
        self.name = "Logger"
        self.slug = "logger"
        self.description = "Log bot events"
        self.commands = [
            Command(
                name="!set-log-channel",
                description="Set channel to send logs too",
                usage="[channel]",
                handler=self.set_log_channel,
            )
        ]

    async def set_log_channel(self, args: list, message: discord.Message):
        guild_storage = storage.GuildStorage(self.client, message.guild.id)
        channel_id = args[1].replace("<", "").replace("#", "").replace(">", "")
        await guild_storage.set_log_channel(message.guild.id, channel_id)
        await message.channel.send(
            embed=embed.Embed(
                title="👌", description=f"Log channel has been set to {args[1]}"
            )
        )

    async def on_command(self, command: Command, args: list):
        pass
