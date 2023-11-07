# ! ## ------------ ## #
# ? ## BRANCH: MAIN ## #
# ! ## ------------ ## #

import os
import typing
import time

import discord
from discord.ext import commands

from misc import ashen_utils as au, cog_initial as ci
from zenlog import log

# ! You can find my personal discord [au.DEVELOPER] & the gitrepo [au.GITREPO] in misc/utils/ashen_utils.py
# ? Essential for Client to run.
TOKEN: str = f'{os.environ["TOKEN"]}'  # ? Find this on your discord developer portal
PREFIX: str = f'{os.environ["PREFIX"]}'  # ? Prefix for all Non-Slash Commands. Default: "ex."


# ? Custom Client & Handler, not much extra here yet.
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


INTENTS = discord.Intents.all()
CLIENT = ExodusClient(command_prefix=PREFIX, intents=INTENTS)


# ? Error Handler
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

    await ci.initialCogs(CLIENT)

    # ! Slash Commands Setup
    try:
        synced = await CLIENT.tree.sync()
        log.crit(f'$ Synced {len(synced)} command(s)')
    except Exception as e:
        log.crit(f'<<<$ Error Syncing Commands: {e}>>>')
        exit()

    log.warn('$ Bot Online | All Boot Cogs Loaded.')

    await CLIENT.change_presence(status=discord.Status.idle, activity=discord.Game('with Snakes.'))


@CLIENT.command(name="sync")
async def sync(ctx):  # ! Slash Commands Cog Essential
    if str(ctx.author.id) != f'{au.RUNNER}':
        return
    synced = await CLIENT.tree.sync()
    print(f"Synced {len(synced)} command(s).")


CLIENT.run(TOKEN)
