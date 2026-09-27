import asyncio
import os

import discord
from discord.ext import commands

from .cogs import DbCog, MatrixCog

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN", "")
MATRIX_REG_SHARED_SECRET = os.environ.get("MATRIX_REG_SHARED_SECRET", "")
MATRIX_SERVER = os.environ.get("MATRIX_SERVER", "")

async def _load_cogs(bot: commands.Bot):
    await bot.add_cog(DbCog(bot))
    await bot.add_cog(MatrixCog(bot, MATRIX_REG_SHARED_SECRET.encode(), MATRIX_SERVER))

async def _run_bot(bot: commands.Bot, token: str):
    async with bot:
        await _load_cogs(bot)
        await bot.start(token)

def main():
    discord.utils.setup_logging()

    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(
        commands.when_mentioned,
        intents=intents
    )

    asyncio.run(_run_bot(bot, DISCORD_TOKEN))

if __name__ == "__main__":
    main()
