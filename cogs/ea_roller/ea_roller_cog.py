import discord
from zenlog import log
import discord.ext

from random import randint

import misc.config.main_config as mc


class EA_ROLLER(discord.ext.commands.Cog):
    def __init__(self, CLIENT):
        self.CLIENT = CLIENT

    @discord.app_commands.command(name='earoll', description='EA Dice Roller!')
    @discord.app_commands.describe(variety='1 = 1 sided die',
                                   count='2 = 2 dice rolled',
                                   add='optional, 3 = +3',
                                   subtract='optional, 4 = -4')
    async def earoll(self, interaction: discord.Interaction, variety: str, count: str, add: str = '0', subtract: str = '0'):

        variety: int = int(variety)
        count: int = int(count)
        add: int = int(add)
        subtract: int = int(subtract)

        highest_num_allowed: int = 100
        if variety > highest_num_allowed or count > highest_num_allowed or add > highest_num_allowed or subtract > highest_num_allowed:
            page: discord.Embed = discord.Embed(title='EA Roller', description='-# Non-TTRPG System Bound Dice Roller',
                                                colour=mc.EMBED_COLORS['purple'])
            page.set_footer(text=f'{interaction.user.id}', icon_url=f'{interaction.user.avatar}')
            page.set_author(name=f'{interaction.user.name}', icon_url=f'{interaction.user.avatar}')
            page.add_field(name='Roll Error:', value=f'A Provided Number is Higher Than {highest_num_allowed}', inline=False)
            await interaction.response.send_message(embed=page, ephemeral=True)
            return

        roll_log: str = ''
        roll_result: int = 0
        while_var: int = 0

        while while_var < count:
            die_result: int = randint(1, variety)
            roll_log += f'{die_result}[d{variety}] + '
            roll_result += die_result
            while_var += 1

        roll_log = roll_log[:-3]

        if add != 0:
            roll_log += f' + {add}'
            roll_result += add

        if subtract != 0:
            roll_log += f' - {subtract}'
            roll_result -= subtract

        page: discord.Embed = discord.Embed(title='EA Roller', description='-# Non-TTRPG System Bound Dice Roller', colour=mc.EMBED_COLORS['purple'])
        page.set_footer(text=f'{interaction.user.id}', icon_url=f'{interaction.user.avatar}')
        page.set_author(name=f'{interaction.user.name}', icon_url=f'{interaction.user.avatar}')
        page.add_field(name='Roll Log:', value=f'{roll_log}', inline=False)
        page.add_field(name='Result:', value=f'{roll_result}', inline=False)

        await interaction.response.send_message(embed=page)
        return


async def setup(CLIENT):
    await CLIENT.add_cog(EA_ROLLER(CLIENT))
