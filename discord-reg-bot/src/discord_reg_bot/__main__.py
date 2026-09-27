import asyncio
import os

import discord
from discord.ext import commands

from .bot import MeropeDiscordBot


async def _run_bot(bot: commands.Bot, token: str):
    async with bot:
        await bot.start(token)

def main():
    discord.utils.setup_logging()

    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    assert DISCORD_TOKEN is not None

    exts = ["cogs.matrix"]

    intents = discord.Intents.default()
    intents.message_content = True
    bot = MeropeDiscordBot(
        commands.when_mentioned,
        initial_extensions=exts,
        intents=intents,
    )

    asyncio.run(_run_bot(bot, DISCORD_TOKEN))

if __name__ == "__main__":
    main()
