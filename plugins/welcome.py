from plugin import Plugin
from command import Command
from utils import embed
import discord
import log


class Welcome(Plugin):
    def init(self):
        self.name = "Welcome"
        self.description = ""
        self.commands = [
            Command(
                name="!test-welcome-message",
                description="Test welcome message that sends on guild join",
                usage="",
                handler=self.test_welcome_message,
                hide_from_help=True,
            )
        ]
        self.hide_from_help = True

    async def test_welcome_message(self, args: list[str], message: discord.Message):
        if message.author.id != 460117198795702272:
            return
        await self.on_guild_join(message.guild, test=True)

    async def on_guild_join(self, guild: discord.Guild, test=False):
        if not test:
            self.client.redis.sadd("juxta:guilds", guild.id)
        welcome_message = await self.client.redis.get("juxta:welcome-message")
        info_message = await self.client.redis.get("juxta:info-message")
        welcome_embed = (
            embed.Embed(footer="Good luck!")
            .add_field(name="👋 Welcome!", value=welcome_message.decode("utf-8"))
            .add_field(name="📖 How to use Juxta", value=info_message.decode("utf-8"))
        )

        await guild.owner.send(embed=welcome_embed)

    async def on_guild_remove(self, guild: discord.Guild):
        self.client.redis.srem("juxta:guilds", guild.id)
