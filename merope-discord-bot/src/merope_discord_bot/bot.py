import os

import discord
from discord.ext import commands

from .cogs import MatrixCog

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN", "")

intents = discord.Intents.none()

bot = commands.Bot(
    commands.when_mentioned,
    intents=intents,
    max_messages=None,
)

@bot.event
async def on_ready():
    await bot.tree.sync()

async def main():
    async with bot:
        await bot.add_cog(MatrixCog(bot))
        await bot.start(DISCORD_TOKEN)
