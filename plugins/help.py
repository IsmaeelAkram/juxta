from plugin import Plugin
from command import Command
from utils import embed
import discord


class Help(Plugin):
    def init(self):
        self.name = "Help"
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

    async def help(self, args: list[str], message: discord.Message):
        if len(args) <= 1:
            help_embed = embed.Embed(
                author="Juxta Plugins Help",
                icon="https://raw.githubusercontent.com/IsmaeelAkram/juxta/master/art/Processor.png",
            ).set_thumbnail(
                url="https://raw.githubusercontent.com/IsmaeelAkram/juxta/master/art/Processor.png"
            )
            for plugin in self.client.plugins:
                help_embed.add_field(
                    name=plugin.name, value=f"`!help {plugin.name.lower()}`"
                )
            await message.author.send(embed=help_embed)
        else:
            for plugin in self.client.plugins:
                if plugin.name.lower() == args[1].lower():
                    if not plugin.hide_from_help:
                        plugin_commands = ""
                        for command in plugin.commands:
                            if command.hide_from_help == False:
                                if command.usage == "":
                                    usage = ""
                                else:
                                    usage = " " + command.usage
                                plugin_commands += f"`{command.name}{usage}`\n{command.description}\n\n"
                        await message.author.send(
                            embed=embed.Embed(
                                title=plugin.name + " Plugin",
                                description=plugin_commands,
                            ).set_thumbnail(
                                url="https://raw.githubusercontent.com/IsmaeelAkram/juxta/master/art/Processor.png"
                            )
                        )
                        return

        await message.delete()
