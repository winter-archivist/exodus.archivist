# PROJECT BRANCH:
# MAIN #

import os
import typing

import discord
from discord.ext import commands

from zenlog import log

TOKEN: str = os.environ["TOKEN"]
CLIENT_PREFIX: str = 'ex.'


# Custom Client & Handler
class ExodusContext(commands.Context):
    def __init__(self, *args: typing.Any, **kwargs: typing.Any):
        super().__init__(*args, **kwargs)

        self.test = 123

    async def context_test(self):
        await self.send(f"{self.test}")


class ExodusClient(commands.Bot):

    async def get_context(self, message: discord.Message, *, cls=ExodusContext):
        return await super().get_context(message, cls=cls)

    async def process_commands(self, message) -> None:
        if message.author.bot:
            return
        ctx = await self.get_context(message)
        await self.invoke(ctx)

    async def on_message(self, message, /) -> None:
        await self.process_commands(message)


# Client Var
INTENTS = discord.Intents.all()
CLIENT = ExodusClient(command_prefix=CLIENT_PREFIX, intents=INTENTS)


@CLIENT.event
async def on_ready():
    log.info('$ Loading Bootstrap Cogs...')
    # Bootstrap Cogs Loading Start
    await CLIENT.load_extension('cogManager')
    await CLIENT.load_extension('cogs.vampire')
    # Bootstrap Cogs Loading Ended
    log.info('$ Bot Online | All Bootstrap Cogs Loaded.')


@CLIENT.command()
async def test(ctx: ExodusContext) -> None:
    await ctx.channel.purge(limit=1)
    await ctx.send('public_test')


@CLIENT.command(hidden=True)
async def _test(ctx: ExodusContext) -> None:
    await ctx.channel.purge(limit=1)
    await ctx.author.send('hidden_test')

CLIENT.run(TOKEN)
