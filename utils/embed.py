import discord
import colors
import datetime


def Embed(
    description="",
    image=None,
    title="",
    color=0xFCFCFC,
    footer="",
):
    return discord.Embed(
        description=description,
        image=image,
        title=title,
        color=color,
        timestamp=datetime.datetime.utcnow(),
    ).set_footer(text=footer)


def SoftErrorEmbed(error):
    return discord.Embed(title="Oops!", description=error, color=0xD13F3F)