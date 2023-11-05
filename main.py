# ! ## ------------ ## #
# ? ## BRANCH: MAIN ## #
# ! ## ------------ ## #

import os
import typing
import time

import discord
from discord.ext import commands

from misc import ashen_utils as au
from zenlog import log

# ? Used to start the bot, TOKEN you can find on the discord developer page, prefix is just the bot prefix ex: ! ? # . <
TOKEN: str = f'{os.environ["TOKEN"]}'
PREFIX: str = f'{os.environ["PREFIX"]}'


# ? Custom Client & Handler
class ExodusContext(commands.Context):
    def __init__(self, *args: typing.Any, **kwargs: typing.Any):
        super().__init__(*args, **kwargs)

        self.test = 123

    async def context_test(self):
        await self.send(f"{self.test}")


# ? The Client itself
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
CLIENT = ExodusClient(command_prefix=PREFIX, intents=INTENTS)


@CLIENT.event
async def on_command_error(ctx, error):
    """Error Handling"""
    await ctx.send(f'> `{error}` \n'
                   f'Screenshot this and send it to `{au.RUNNER}`, the host of this bot. \n'
                   f'To contact the original bot writer: `{au.DEVELOPER}` and/or visit `{au.GITREPO}`')


@CLIENT.event
async def on_ready():
    log.warn('$ Project Branch: MAIN')
    log.info(f'$ Servers: {", ".join(str(x) for x in CLIENT.guilds)}\n$ Server Count: {len(CLIENT.guilds)}')
    log.info(f'$ Start-Time: {time.strftime("%H:%M:%S", time.localtime())}')

    log.warn('$ Loading Bootstrap Cogs...')
    await CLIENT.load_extension('cogManager')
    await CLIENT.load_extension('cogs.exonotes.exoNotes')
    await CLIENT.load_extension('cogs.vampire.vampireRoll')
    log.warn('$ Bot Online | All Bootstrap Cogs Loaded.')
    await CLIENT.change_presence(status=discord.Status.idle, activity=discord.Game('with Snakes.'))


@CLIENT.command()
async def test(ctx):
    if not isinstance(ctx.channel, discord.channel.DMChannel): await ctx.channel.purge(limit=1)
    await ctx.author.send(f'Bot Functional {time.strftime("%H:%M:%S", time.localtime())}')


@CLIENT.command()
@commands.dm_only()
async def errormake(ctx):
    if not isinstance(ctx.channel, discord.channel.DMChannel): await ctx.channel.purge(limit=1)
    await ctx.author.send(f'Bot Functional {time.strftime("%H:%M:%S", time.localtime())}')


CLIENT.run(TOKEN)
