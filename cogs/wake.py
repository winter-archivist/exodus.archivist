from discord.ext import commands

from zenlog import log


class Wake(commands.Cog):
    def __init__(self, CLIENT):
        self.CLIENT = CLIENT

    @commands.command()
    async def wake(self, ctx):
        await ctx.send('wake')

    @commands.command()
    async def wakeAt(self, ctx):
        target = ExodusClient.get_user(int(567819777209532418))
        await target.send(content='wakeAt', )


async def setup(CLIENT):
    await CLIENT.add_cog(Wake(CLIENT))
    log.info('> Wake Loaded')


async def teardown():
    log.critical('> Wake Unloaded')
