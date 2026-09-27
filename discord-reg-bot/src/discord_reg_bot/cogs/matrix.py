import hashlib
import hmac
import logging
import random
import sqlite3
import string

import aiohttp
from discord.ext import commands
from discord.ext.commands import Bot, Context

# https://github.com/matrix-construct/tuwunel/blob/5ff48622a03f6dcf110a59c8369611375b649037/src/api/client/register/register.rs#L22
RANDOM_USER_ID_LENGTH = 10
# https://github.com/matrix-construct/tuwunel/blob/5ff48622a03f6dcf110a59c8369611375b649037/src/admin/user/mod.rs#L35
AUTO_GEN_PASSWORD_LENGTH = 25

logger = logging.getLogger(__name__)

class MatrixCog(commands.Cog):
    def __init__(self, bot: Bot, key: bytes, server: str):
        self.bot = bot
        self.key = key
        self.server = server

    async def cog_load(self):
        self.session = aiohttp.ClientSession(self.server)
        self.db = sqlite3.connect("users.db")

    async def cog_unload(self):
        await self.session.close()
        self.db.close()

    @commands.hybrid_group()
    async def matrix(self, ctx: Context):
        pass

    @matrix.command(
        description="Register Matrix Account"
    )
    async def register(self, ctx: Context):
        discord_user = ctx.author
        logger.info(f"Checking if Discord User ({discord_user}) has Matrix Account")
        user_id = await self.get_matrix_user(discord_user.id)
        if user_id is not None:
            logger.info(f"Discord User ({discord_user}) already has a Matrix User ({user_id})")
            await ctx.reply(f"Matrix User `{user_id}` exists", ephemeral=True)
            return

        # TODO: use model
        username = self.generate_alphanumeric_string(RANDOM_USER_ID_LENGTH)
        password = self.generate_alphanumeric_string(AUTO_GEN_PASSWORD_LENGTH)
        displayname = discord_user.display_name

        logger.info(f"Creating Matrix User ({username}) for Discord User ({discord_user})")

        matrix_user = await self.create_user(username, password, displayname)
        user_id = matrix_user["user_id"]
        await self.set_matrix_user(discord_user.id, user_id)

        await ctx.reply(
            "\n".join((
                f'Created User `{username}` with password ||`{password}`||.',
                "Usernames are randomly generated and can't be changed.",
                "You can change this password after you login.",
                "Please Login at https://app.cinny.in/login/wpi.moe"
            )),
            ephemeral=True
        )

    async def get_matrix_user(self, discord: int) -> str | None:
        with self.db:
            cur = self.db.execute(
                "SELECT matrix FROM users WHERE discord = ? AND matrix LIKE '%:wpi.moe'",
                (discord,)
            )
            user_id = cur.fetchone()
            cur.close()
        if user_id:
            user_id, = user_id
        return user_id

    async def set_matrix_user(self, discord: int, matrix: str):
        with self.db:
            cur = self.db.execute(
                "INSERT INTO users(discord, matrix) VALUES(?, ?)",
                (discord, matrix,)
            )
            cur.close()

    @staticmethod
    def generate_alphanumeric_string(length: int):
        alphanumeric = string.ascii_letters + string.digits
        return ''.join(random.choices(alphanumeric, k=length))

    async def create_user(self, username: str, password: str, displayname: str) -> dict:
        # https://element-hq.github.io/synapse/latest/admin_api/register_api.html

        # https://github.com/matrix-construct/tuwunel/blob/5ff48622a03f6dcf110a59c8369611375b649037/src/api/client/admin/get_nonce.rs
        async with self.session.get("/_synapse/admin/v1/register") as resp:
            logger.debug(f"Getting Matrix Nonce: {resp}")
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
            logger.debug(f"Registering Matrix User: {resp}")
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
