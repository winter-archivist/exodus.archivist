import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import View

import sqlite3
from random import randint
from zenlog import log

from misc.config import main_config as mc
from misc.utils import interaction_utils as iu
from misc.utils import yaml_utils as yu
from cogs.vampire.selections import selections as s
from cogs.vampire import vamplib as vl


class NewVampireRoll(commands.Cog):
    def __init__(self, CLIENT):
        self.CLIENT = CLIENT

    @app_commands.command(name='newroll', description='newRollTest')
    @app_commands.choices(choices=[
        app_commands.Choice(name="Standard", value="standard"),
        app_commands.Choice(name="Frenzy Resist", value="frenzy_resist"),
        app_commands.Choice(name="Predator Type Hunt", value="predator_type_hunt"),
        app_commands.Choice(name="Rouse", value="rouse"),
        app_commands.Choice(name="Remorse", value="remorse")])
    @app_commands.describe(charactername='Character Name')
    async def newRoll(self, interaction: discord.Interaction, choices: app_commands.Choice[str], charactername: str):
        working_embed = f'working_embed RESET - IF USER SEES THIS -> ERROR: {mc.ISSUE_CONTACT}'
        match choices.value:
            case 'standard':
                if await vl.rollInitialize(interaction, charactername):
                    return
                working_embed = vl.selection_embed_base.add_field(name='Select Your:', value='Difficulty')  # ? SUBJECT TO CHANGE
                await interaction.response.send_message(embed=working_embed, view=vl.DifficultySelectionView(self.CLIENT))

                # ! JUST WORK ABOVE
            case 'frenzy_resist':
                # frenzy resist calculations
                frenzy_resist_embed = (discord.Embed(title='', description=f'', color=mc.embed_colors["purple"]))
                await interaction.response.send_message(embed=frenzy_resist_embed)
            case 'predator_type_hunt':
                # predator-type hunt calculations
                predator_embed = (discord.Embed(title='', description=f'', color=mc.embed_colors["purple"]))
                await interaction.response.send_message(embed=predator_embed)
            case 'rouse':
                # remorse calculations
                rouse_embed = (discord.Embed(title='', description=f'', color=mc.embed_colors["purple"]))
                await interaction.response.send_message(embed=rouse_embed)
            case 'remorse':
                # remorse calculations
                remorse_embed = (discord.Embed(title='', description=f'', color=mc.embed_colors["purple"]))
                await interaction.response.send_message(embed=remorse_embed)
            case _:
                await interaction.response.send_message(content=f'`ISSUE: /newRoll case _ {choices.value=}` | {mc.ISSUE_CONTACT}')

    @commands.command(hidden=True)
    async def new(self, ctx, targetcharacter: str):
        if ctx.author.id == mc.RUNNER_ID:
            try:
                db = sqlite3.connect(f'cogs//vampire//characters//{str(ctx.author.id)}//{targetcharacter}.sqlite')
                cursor = db.cursor()

                await vl.standardMake(ctx, cursor)

                # CommandVars
                cursor.execute('CREATE TABLE IF NOT EXISTS commandvars(difficulty INTEGER, rollPool INTEGER, result INTEGER, pool_composition TEXT)')

                cursor.execute('CREATE TABLE IF NOT EXISTS reroll_info('
                               'regularCritDie INTEGER, hungerCritDie INTEGER, '
                               'regularSuccess INTEGER, hungerSuccess INTEGER, '
                               'regularFail INTEGER, hungerFail INTEGER, '
                               'hungerSkull INTEGER)')

                cursor.execute('CREATE TABLE IF NOT EXISTS char_info(blood_potency INTEGER, clan TEXT, generation INTEGER, bane_severity INTEGER)')
                db.commit(); db.close()
                await ctx.send('Make Complete')
            except Exception as e:
                log.crit(f'>* Error With Making New Character {targetcharacter}: {e}')


async def setup(CLIENT):
    await CLIENT.add_cog(NewVampireRoll(CLIENT))
