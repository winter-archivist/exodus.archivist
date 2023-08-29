from discord.ext import commands

from zenlog import log


class GeneralRolls(commands.Cog):
    def __init__(self, CLIENT):
        self.CLIENT = CLIENT

    @commands.command()
    async def genro(self, ctx):
        await ctx.send('genro')


async def setup(CLIENT):
    await CLIENT.add_cog(GeneralRolls(CLIENT))
    log.info('> General Rolls Loaded')


async def teardown(CLIENT):
    log.critical('> General Rolls Unloaded')
