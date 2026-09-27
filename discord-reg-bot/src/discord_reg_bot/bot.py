from collections.abc import Iterable

from discord.ext import commands


class MeropeDiscordBot(commands.Bot):
    def __init__(
        self,
        *args,
        initial_extensions: Iterable[str],
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self._initial_extensions = initial_extensions

    async def setup_hook(self) -> None:
        # here, we are loading extensions prior to sync to ensure we are syncing interactions defined in those extensions.

        for extension in self._initial_extensions:
            await self.load_extension(extension)

        # This would also be a good place to connect to our database and
        # load anything that should be in memory prior to handling events.
