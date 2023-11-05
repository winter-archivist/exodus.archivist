# ! ## ------------ ## #
# ? ## BRANCH: MAIN ## #
# ! ## ------------ ## #

import os
import typing
import time

import discord
from discord.ext import commands

from zenlog import log

# ? Used to start the bot, TOKEN you can find on the discord developer page, prefix is just the bot prefix ex: ! ? # . <
TOKEN: str = f'{os.environ["TOKEN"]}'
PREFIX: str = f'{os.environ["PREFIX"]}'

# ? Used Across Bot, this should be YOUR userNAME (Not userID)
DEVELOPER = '.ashywinter'  # ! if you need to contact who wrote this awful code
GITREPO = 'https://github.com/AshenEntropy/.ae_rewrite'
RUNNER: str = f'{os.environ["RUNNER"]}'  # ! your discord userNAME
ISSUE_CONTACT: str = (f'If you believe there is an issue, screenshot this and send it to `{RUNNER}`, the host of this bot. \n'
                      f'To contact the original bot writer: {DEVELOPER}` and/or visit `{GITREPO}`')


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
    await ctx.send(f'`{error}`')


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

CLIENT.run(TOKEN)
