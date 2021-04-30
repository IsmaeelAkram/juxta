from plugin import Plugin
from command import Command
from utils import embed
import discord
import asyncio
import log


class Music(Plugin):
    def __init__(self, client: discord.Client):
        self.client = client
        self.name = "Music"
        self.description = "Music commands"
        self.commands = [
            Command(
                name="summon",
                description="Bring Juxta into your voice channel",
                usage="",
                handler=self.summon,
            ),
            Command(
                name="join",
                description="Alias of !summon",
                usage="",
                handler=self.summon,
            ),
            Command(
                name="connect",
                description="Alias of !summon",
                usage="",
                handler=self.summon,
            ),
            Command(
                name="leave",
                description="Remove Juxta from your voice channel",
                usage="",
                handler=self.leave,
            ),
            Command(
                name="disconnect",
                description="Alias of !leave",
                usage="",
                handler=self.leave,
            ),
            Command(
                name="airhorn",
                description="Plays an airhorn in your voice channel",
                usage="",
                handler=self.airhorn,
            ),
        ]

    async def summon(self, args: list[str], message: discord.Message):
        voice_channel = message.author.voice.channel
        await voice_channel.connect()
        await message.guild.change_voice_state(channel=voice_channel, self_deaf=True)
        await message.add_reaction("👌")

    async def leave(self, args: list[str], message: discord.Message):
        await message.guild.voice_client.disconnect()
        await message.add_reaction("👌")

    async def airhorn(self, args: list[str], message: discord.Message):
        isQuick = False
        try:
            voice_channel = message.author.voice.channel
            await voice_channel.connect()
            isQuick = True
        except:
            pass
        source = discord.PCMVolumeTransformer(
            discord.FFmpegPCMAudio("data/airhorn_default.ogg")
        )
        message.guild.voice_client.play(
            source, after=lambda e: print(f"Player error: {e}") if e else None
        )

        await message.add_reaction("📣")
        if isQuick:
            await asyncio.sleep(3)
            await message.guild.voice_client.disconnect()
