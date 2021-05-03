from plugin import Plugin
from command import Command
from utils import embed
import discord
import storage
import log


class Help(Plugin):
    def init(self):
        self.name = "Help"
        self.slug = "help"
        self.description = "List of commands"
        self.commands = [
            Command(
                name="!help",
                description="Shows all commands, descriptions, and usages",
                usage="",
                handler=self.help,
            ),
            Command(
                name="!commands",
                description="Alias for !help",
                usage="",
                handler=self.help,
            ),
        ]
        self.hide_from_help = True

    async def help(self, args: list[str], message: discord.Message):
        guild_storage = storage.GuildStorage(self.client, message.guild.id)
        guild_plugins = await guild_storage.get_plugins()
        if len(args) <= 1:
            help_embed = await guild_storage.generate_main_help(guild_plugins)
            await message.author.send(embed=help_embed)
        else:
            plugin_help_embed = await guild_storage.generate_plugin_help(
                args, guild_plugins
            )
            if plugin_help_embed:
                await message.author.send(embed=plugin_help_embed)

        await message.delete()
