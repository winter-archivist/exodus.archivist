# ! ## -------------------- ## #
# ? ## Project Branch: Main ## #
# ! ## -------------------- ## #

import typing
import time
import discord
from discord.ext import commands
from zenlog import log

from misc.config import mainConfig as mC, clientConfig as cC


async def initializeStartupCogs(CLIENT_INPUT):
    log.info('$ Initializing Startup Cogs...')

    # To add cogs, just add their directory, but instead of / use .
    # however do not include their file extension
    initial_cogs: tuple = ('cogs.cogManager',
                           'cogs.vampire.vampireCog',
                           'cogs.exonotes.exoNotes')

    # Tries to load any cog listed in the above tuple
    # Exits Startup if the cog isn't found
    for_var = 0
    for x in initial_cogs:
        targeted_cog = initial_cogs[for_var]

        try:
            await CLIENT_INPUT.load_extension(f'{targeted_cog}')
            log.debug(f'$ {targeted_cog} Loaded')

        except Exception as e:
            log.crit(f"<<<$ Failed to load {targeted_cog} {e}>>>")
            exit(000)

        for_var += 1

    log.info('$ Loaded Startup Cogs... Slash Mode Check Starting...')

    # ! ---READ THE COMMENTS BELOW--- !
    # ! This script will kill the bot on Startup !
    # It's a simple automation script for a "calculator" (it can only add)
    # that remembers the prior number then adds the command input
    import cogs.ddtr.ddtr as ddtr
    await ddtr.ddtr_check(CLIENT_INPUT)
    # ! ---READ THE COMMENTS ABOVE--- !


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
        await self.invoke(ctx)  # Do not remove

    async def on_message(self, message, /) -> None:
        await self.process_commands(message)


INTENTS = discord.Intents.all()
CLIENT = ExodusClient(command_prefix=cC.PREFIX, intents=INTENTS)


@CLIENT.event
async def on_ready():
    log.warn('$ Project Branch: MAIN')
    log.info(f'$ Servers {len(CLIENT.guilds)}: {", ".join(str(x) for x in CLIENT.guilds)}')
    log.info(f'$ Start-Time: {time.strftime("%H:%M:%S", time.localtime())}')

    # Loads any cogs listed in the tuple "initial_cogs" in initializeStartupCogs()
    await initializeStartupCogs(CLIENT)

    # Slash Commands Setup
    # Can be easily disabled/enabled via the variable
    # "SLASH_MODE" in misc/config/clientConfig.py
    match cC.SLASH_MODE:

        case True:
            try:
                synced = await CLIENT.tree.sync()
                log.info(f"Synced [ {len(synced)} ] command(s).")

            except Exception as e:
                log.crit(f'<<<$ Error Syncing Commands | {e}>>>')
                exit()

        case False:
            log.warn('$ SLASH_MODE is False, Sync Skipped')

        case _:
            log.crit('<<<$ SLASH_MODE is Not a Bool, Client Killed >>>')
            exit()

    log.info('$ Bot Online | All Startup Cogs Initialized.')
    await CLIENT.change_presence(status=discord.Status.idle, activity=discord.Game('with Snakes.'))


# Required for Slash Commands to work
# Do Not Remove.
@CLIENT.command(name="sync")
async def sync(ctx):  # ! Slash Commands Cog Essential
    if str(ctx.author.id) != f'{mC.RUNNER}':
        return
    synced = await CLIENT.tree.sync()
    log.info(f"Synced [ {len(synced)} ] command(s).")


CLIENT.run(token=cC.TOKEN, reconnect=True)
