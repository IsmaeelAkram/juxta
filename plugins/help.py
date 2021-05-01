from plugin import Plugin
from command import Command
from utils import embed
import discord


class Help(Plugin):
    def __init__(self, client: discord.Client):
        self.client = client
        self.name = "Help"
        self.description = "List of commands"
        self.commands = [
            Command(
                name="help",
                description="Shows all commands, descriptions, and usages",
                usage="",
                handler=self.help,
            ),
            Command(
                name="commands",
                description="Alias for !help",
                usage="",
                handler=self.help,
            ),
        ]

    async def help(self, args: list[str], message: discord.Message):
        help_embed = embed.Embed(
            title="Juxta Help",
            description="Juxta is a high-performance, easy-to-use Discord bot with an abundance of features. This help prompt is meant to be a guide on the commands Juxta has to offer, and how to use them.",
        ).set_thumbnail(
            url="https://raw.githubusercontent.com/IsmaeelAkram/juxta/master/art/Processor.png"
        )
        await message.author.send(embed=help_embed)

        for plugin in self.client.plugins:
            plugin_commands = ""
            for command in plugin.commands:
                if command.hide_from_help == False:
                    if command.usage == "":
                        usage = ""
                    else:
                        usage = " " + command.usage
                    plugin_commands += f"`{self.client.PREFIX}{command.name}{usage}`\n{command.description}\n\n"
            if len(plugin.commands) != 0:
                await message.author.send(
                    embed=embed.Embed(
                        title=plugin.name, description=plugin_commands
                    ).set_thumbnail(
                        url="https://raw.githubusercontent.com/IsmaeelAkram/juxta/master/art/Processor.png"
                    )
                )
                await message.add_reaction("✅")
