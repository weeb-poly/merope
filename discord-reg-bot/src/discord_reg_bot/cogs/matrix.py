import hashlib
import hmac
import os
import random
import string

import aiohttp
import discord
from discord.ext import commands
from discord.ext.commands import Bot, Context

# https://github.com/matrix-construct/tuwunel/blob/5ff48622a03f6dcf110a59c8369611375b649037/src/api/client/register/register.rs#L22
RANDOM_USER_ID_LENGTH = 10
# https://github.com/matrix-construct/tuwunel/blob/5ff48622a03f6dcf110a59c8369611375b649037/src/admin/user/mod.rs#L35
AUTO_GEN_PASSWORD_LENGTH = 25

class Matrix(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.key = os.environ.get("MATRIX_REG_SHARED_SECRET", "").encode()
        self.matrix_server = "https://matrix.wpi.moe/" # TODO

    async def cog_load(self):
        self.session = aiohttp.ClientSession(self.matrix_server)

    async def cog_unload(self):
        await self.session.close()

    @commands.hybrid_group()
    async def matrix(self, ctx: Context):
        pass

    @matrix.command()
    async def register(self, ctx: Context):
        member = ctx.author
        username = await self.get_matrix_user(member)
        if username is not None:
            await ctx.send("Matrix User already exists")
            return

        # TODO: use model
        username = self.generate_alphanumeric_string(RANDOM_USER_ID_LENGTH)
        password = self.generate_alphanumeric_string(AUTO_GEN_PASSWORD_LENGTH)
        displayname = member.display_name

        await self.create_user(username, password, displayname)
        await self.set_matrix_user(member, username)

        await ctx.send(f'Created User `{username}` with password ||`{password}`||')

    async def get_matrix_user(self, member: discord.User | discord.Member) -> str | None:
        # TODO: get matrix user if exists. This may require a database
        return None

    async def set_matrix_user(self, member: discord.User | discord.Member, username: str):
        # TODO: set matrix user in database
        return None

    @staticmethod
    def generate_alphanumeric_string(length: int):
        alphanumeric = string.ascii_letters + string.digits
        return ''.join(random.choices(alphanumeric, k=length))

    async def create_user(self, username: str, password: str, displayname: str) -> dict:
        # https://element-hq.github.io/synapse/latest/admin_api/register_api.html

        # https://github.com/matrix-construct/tuwunel/blob/5ff48622a03f6dcf110a59c8369611375b649037/src/api/client/admin/get_nonce.rs
        async with self.session.get("/_synapse/admin/v1/register") as resp:
            nonce = (await resp.json())["nonce"]

        data = {
            "nonce": nonce,
            "username": username,
            "displayname": displayname,
            "password": password,
            "admin": False,
            "mac": ""
        }

        data["mac"] = self.generate_mac(
            self.key,
            data["nonce"],
            data["username"],
            data["password"],
            data["admin"]
        )

        # https://github.com/matrix-construct/tuwunel/blob/5ff48622a03f6dcf110a59c8369611375b649037/src/api/client/admin/register.rs
        async with self.session.post("/_synapse/admin/v1/register", json=data) as resp:
            # TODO: validate response
            return await resp.json()

    @staticmethod
    def generate_mac(
        key: bytes | bytearray,
        nonce: str,
        user: str,
        password: str,
        admin: bool = False,
        user_type: str | None = None
    ) -> str:
        mac = hmac.new(
            key=key,
            digestmod=hashlib.sha1,
        )

        mac.update(nonce.encode('utf8'))
        mac.update(b"\x00")
        mac.update(user.encode('utf8'))
        mac.update(b"\x00")
        mac.update(password.encode('utf8'))
        mac.update(b"\x00")
        mac.update(b"admin" if admin else b"notadmin")
        if user_type:
            mac.update(b"\x00")
            mac.update(user_type.encode('utf8'))

        return mac.hexdigest()


async def setup(bot: Bot):
    cog = Matrix(bot)
    await bot.add_cog(cog)
