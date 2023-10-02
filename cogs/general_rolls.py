from discord.ext import commands

from zenlog import log

import random


class GeneralRolls(commands.Cog):
    def __init__(self, CLIENT):
        self.CLIENT = CLIENT

    @commands.command(aliases=['r'])
    async def roll(self, ctx, dieAmount: int, dieFaces: int, dieModifierOperation: str = '0', dieModifierNumber: int = 0, limiter: int = 0):

        if str(ctx.author) == '.ashywinter' and limiter != 0:
            await ctx.send('### ~~__|~~ `LIMIT REMOVED : DANGER ZONE` ~~|__~~ ')
            log.warning('> Limiter for roll ignored')

        elif dieModifierNumber > 1000 or dieAmount > 1000 or dieFaces > 1000:
            await ctx.send(f'Please use a number below 1000.')
            return

        dieTotal = 0; counter = 0
        operations = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            'x': lambda x, y: x * y, '*': lambda x, y: x * y,
            '/': lambda x, y: x / y, '_': lambda x, y: x / y,
            '^': lambda x, y: x ** y, '**': lambda x, y: x ** y
        }
        while counter < dieAmount:
            dieTotal = dieTotal + random.randint(1, dieFaces)
            counter += 1

        if dieModifierOperation in operations and dieModifierOperation != '0':
            operation = operations[dieModifierOperation]
            dieTotal = operation(dieTotal, dieModifierNumber)
            await ctx.send(f'Rolled: {str(dieAmount)}d{dieFaces}{str(dieModifierOperation)}{str(dieModifierNumber)} = {str(dieTotal)}')

        elif dieModifierOperation == '0':
            await ctx.send(f'Rolled: {str(dieAmount)}d{dieFaces} = {str(dieTotal)}')

        else:
            log.warning('> Incorrect `dieModifierOperation` passed to `roll` command')


async def setup(CLIENT):
    await CLIENT.add_cog(GeneralRolls(CLIENT))
    log.info('> General Rolls Loaded')


async def teardown():
    log.critical('> General Rolls Unloaded')
