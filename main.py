# ! ## ------------ ## #
# ? ## BRANCH: newRoll ## #
# ! ## ------------ ## #
# * Post-Optimization I will push to main
# * Webhook Test

import typing
import time

import discord
from discord.ext import commands

from zenlog import log

from misc.config import main_config as mc
import client_config as config


async def initialCogs(CLIENT_INPUT):
    log.info('$ Loading Initial Cogs...')
    initial_cogs = ('cogs.cogManager',
                    'cogs.vampire.vampireRoll',
                    'cogs.exonotes.exoNotes')
    forVar = 0
    for x in initial_cogs:
        targetedCog = initial_cogs[forVar]
        try:
            await CLIENT_INPUT.load_extension(f'{targetedCog}')
            log.debug(f'$ {targetedCog} Loaded')
        except Exception as e:
            log.crit(f"<<<$ Failed to load {targetedCog} {e}>>>")
            exit(000)
        forVar += 1
    log.info('$ Loaded Initial Cogs... Attempting Sync')

    # ! This is a small script purely for use of myself. Remove it when you're using the bot, it has no effect.
    try:
        log.debug(f"$ Loading ddtr")
        await CLIENT_INPUT.load_extension('cogs.ddtr.ddtr')
    except Exception as e:
        log.warn(f"<<<$ {e} | REMOVE TRY STATEMENT IN main.py CONTAINING cogs.ddtr.ddtr >>>")
        exit()
    log.debug(f"$ ddtr Loaded, real sync start.")
    # ! This is a small script purely for use of myself. Remove it when you're using the bot, it has no effect.


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
CLIENT = ExodusClient(command_prefix=config.PREFIX, intents=INTENTS)


# ? Error Handler
@CLIENT.event
async def on_command_error(ctx, error):
    """Error Handling"""
    await ctx.send(f'> `{error}` \n'
                   f'Screenshot this and send it to `{mc.RUNNER}`, the host of this bot. \n'
                   f'To contact the original bot writer: `{mc.DEVELOPER}` and/or visit `{mc.GITREPO}`')


@CLIENT.event
async def on_ready():
    log.warn('$ Project Branch: MAIN')
    log.info(f'$ Servers {len(CLIENT.guilds)}: {", ".join(str(x) for x in CLIENT.guilds)}')
    log.info(f'$ Start-Time: {time.strftime("%H:%M:%S", time.localtime())}')

    await initialCogs(CLIENT)

    # ! Slash Commands Setup
    if config.SLASH_MODE is True:
        try:
            synced = await CLIENT.tree.sync()
            log.crit(f'$ Synced {len(synced)} command(s)')
        except Exception as e:
            log.crit(f'<<<$ Error Syncing Commands: {e}>>>')
            exit()
    elif config.SLASH_MODE is False:
        log.crit('$ SLASH_MODE is False.')
    else:
        log.warn('<<<$ Startup Error: SLASH_MODE IS NOT TRUE OR FALSE >>>')
        exit()

    log.warn('$ Bot Online | All Boot Cogs Loaded.')

    await CLIENT.change_presence(status=discord.Status.idle, activity=discord.Game('with Snakes.'))


@CLIENT.command(name="sync")
async def sync(ctx):  # ! Slash Commands Cog Essential
    if str(ctx.author.id) != f'{mc.RUNNER}':
        return
    synced = await CLIENT.tree.sync()
    print(f"Synced {len(synced)} command(s).")


@commands.command(hidden=True)
async def kill(self, ctx):
    if ctx.author.id != mc.RUNNER_ID:
        return
    await CLIENT.close()


CLIENT.run(token=config.TOKEN, reconnect=True)
