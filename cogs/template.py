from discord.ext import commands

from zenlog import log


class TEMPLATE(commands.Cog):
    def __init__(self, CLIENT):
        self.CLIENT = CLIENT

    @commands.command()
    async def TEMPLATE(self, ctx):
        await ctx.send('TEMPLATE')


async def setup(CLIENT):
    await CLIENT.add_cog(TEMPLATE(CLIENT))
    log.info('> Template Loaded')
