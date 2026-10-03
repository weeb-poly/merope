import asyncio

import discord

from .bot import main as _main

discord.utils.setup_logging()

def main():
    asyncio.run(_main())

if __name__ == "__main__":
    main()
