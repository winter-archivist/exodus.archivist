# ## ----------------------
# ## Check README.md
# ## For extra info
# ## ----------------------


import typing
import time
import discord
from discord.ext import commands
from zenlog import log

import misc.config.main_config as mc
import misc.config.client_config as cc


async def initialize_startup_cogs(CLIENT_INPUT):
    log.info('$ Initializing Startup Cogs...')

    # Tries to load any cog listed in the above tuple; stops execution if the cog isn't found.
    for x in cc.INITIALIZATION_COGS:
        try:
            await CLIENT_INPUT.load_extension(x)
            log.debug(f'$ Loaded Initialization Cog: {x}')

        except Exception as e:
            log.crit(f"<<<$ Failed to Load Initialization Cog: {x} {e}>>>")
            exit()

    log.info('$ Loaded Startup Cogs... Slash Mode Check Started, Safe to Begin Use.')


# Custom Client & Handler, not much extra here yet.
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
        await self.invoke(ctx)  # Do not remove.

    async def on_message(self, message, /) -> None:
        await self.process_commands(message)


INTENTS = discord.Intents.all()
CLIENT = ExodusClient(command_prefix=cc.PREFIX, intents=INTENTS)


@CLIENT.event
async def on_ready():
    log.warn('$ Project Branch: main')
    log.info(f'$ Server Count: {len(CLIENT.guilds)}')
    log.info(f'$ Server Names: {", ".join(str(x) for x in CLIENT.guilds)}')
    log.info(f'$ Start-Time: {time.strftime("%H:%M:%S", time.localtime())}')

    await initialize_startup_cogs(CLIENT)

    # Slash Commands Setup; can be easily disabled/enabled via the variable "SYNC_SLASH_COMMANDS_ON_START" in misc/config/client_config.py
    match cc.SYNC_SLASH_COMMANDS_ON_START:

        case True:

            try:
                synced = await CLIENT.tree.sync()
                log.info(f"Synced [ {len(synced)} ] command(s).")

            except Exception as e:
                log.crit(f'<<<$ Error Syncing Commands | {e}>>>')
                exit()

        case False:
            log.warn('$ SYNC_SLASH_COMMANDS_ON_START is False, Sync Skipped')

        case _:
            log.crit('<<<$ SYNC_SLASH_COMMANDS_ON_START is Not a Bool, Client Killed >>>')
            exit()

    log.info('$ Bot Online | All Startup Cogs Initialized.')
    await CLIENT.change_presence(status=discord.Status.idle, activity=discord.Game('with Snakes.'))


# Required for Slash Commands to work
# Do Not Remove.
@CLIENT.command(name="sync")
@commands.is_owner()
async def sync(ctx):
    # ! Essential to ALL Slash Commands
    try:
        synced = await CLIENT.tree.sync()
        log.info(f"Synced [ {len(synced)} ] command(s).")
        await ctx.channel.send('Synced.')

    except Exception as e:
        log.crit(f'<<< Error Syncing Commands | {e}>>>')
        exit()


CLIENT.run(token=cc.TOKEN, reconnect=True)
