from plugin import Plugin
from command import Command
import embed
import discord
import asyncio
import log
import exceptions


class Music(Plugin):
    def init(self):
        self.name = "Music"
        self.slug = "music"
        self.description = "Music commands"
        self.commands = [
            Command(
                name="!summon",
                description="Bring Juxta into your voice channel",
                usage="",
                handler=self.summon,
            ),
            Command(
                name="!join",
                description="Alias of !summon",
                usage="",
                handler=self.summon,
            ),
            Command(
                name="!connect",
                description="Alias of !summon",
                usage="",
                handler=self.summon,
            ),
            Command(
                name="!leave",
                description="Remove Juxta from your voice channel",
                usage="",
                handler=self.leave,
            ),
            Command(
                name="!disconnect",
                description="Alias of !leave",
                usage="",
                handler=self.leave,
            ),
            Command(
                name="!airhorn",
                description="Plays an airhorn in your voice channel",
                usage="",
                handler=self.airhorn,
            ),
        ]

    async def summon(self, args: list[str], message: discord.Message, is_cmd=True):
        user_voice = message.author.voice
        if user_voice == None:
            raise exceptions.NoVoiceChannelError
            return
        if message.guild.voice_client != None:
            if user_voice.channel.id != message.guild.voice_client.channel.id:
                await self.leave(args, message, is_cmd=False)
                await user_voice.channel.connect()
                await message.guild.change_voice_state(
                    channel=user_voice.channel, self_deaf=True
                )
            else:
                raise exceptions.AlreadyInVoiceChannelError
        else:
            await user_voice.channel.connect()
            await message.guild.change_voice_state(
                channel=user_voice.channel, self_deaf=True
            )
        if is_cmd:
            await message.add_reaction("👌")

    async def leave(self, args: list[str], message: discord.Message, is_cmd=True):
        if message.guild.voice_client == None:
            raise exceptions.BotNotInVoiceChannelError
            return
        await message.guild.voice_client.disconnect()
        if is_cmd:
            await message.add_reaction("👌")

    async def airhorn(self, args: list[str], message: discord.Message):
        isQuick = False

        user_voice = message.author.voice
        if user_voice == None:
            raise exceptions.NoVoiceChannelError
            return
        if message.guild.voice_client != None:
            if user_voice.channel.id != message.guild.voice_client.channel.id:
                isQuick = True
                await self.leave(args, message, is_cmd=False)
                await user_voice.channel.connect()
                await message.guild.change_voice_state(
                    channel=user_voice.channel, self_deaf=True
                )
        else:
            isQuick = True
            await user_voice.channel.connect()
            await message.guild.change_voice_state(
                channel=user_voice.channel, self_deaf=True
            )

        source = discord.PCMVolumeTransformer(
            discord.FFmpegPCMAudio("data/airhorn_default.ogg")
        )
        message.guild.voice_client.play(
            source, after=lambda e: print(f"Player error: {e}") if e else None
        )

        await message.delete()
        if isQuick:
            await asyncio.sleep(3)
            await message.guild.voice_client.disconnect()
