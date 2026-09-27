import sqlite3

from discord.ext import commands
from discord.ext.commands import Bot


class DbCog(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    async def cog_load(self):
        self.con = sqlite3.connect("matrix.db")

    async def cog_unload(self):
        self.con.close()
