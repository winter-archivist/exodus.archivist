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
        match choices.value:
            case 'standard':
                if await vl.rollInitialize(interaction, charactername):
                    return
                working_embed = vl.selection_embed_base.add_field(name='Initial Roll Information', value='')
                working_embed.add_field(name='Roll Pool:', value='0')
                working_embed.add_field(name='Roll Composition:', value='None')
                await interaction.response.send_message(embed=working_embed, view=vl.StandardStartSelectionView(self.CLIENT))
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

                cursor.execute('CREATE TABLE IF NOT EXISTS charAttributes('
                               'strength INTEGER, dexterity INTEGER, stamina INTEGER, '
                               'charisma INTEGER, manipulation INTEGER, composure INTEGER, '
                               'intelligence INTEGER, wits INTEGER, resolve INTEGER)')

                cursor.execute(
                    'CREATE TABLE IF NOT EXISTS physicalSkills(athletics INTEGER, brawl INTEGER, craft INTEGER, drive INTEGER, '
                    'firearms INTEGER, larceny INTEGER, melee INTEGER, stealth INTEGER, survival INTEGER)')
                cursor.execute(
                    'CREATE TABLE IF NOT EXISTS socialSkills(animal_ken INTEGER, etiquette INTEGER, insight INTEGER, intimidation INTEGER, '
                    'leadership INTEGER, performance INTEGER, persuasion INTEGER, streetwise INTEGER, subterfuge INTEGER)')
                cursor.execute(
                    'CREATE TABLE IF NOT EXISTS mentalSkills(academics INTEGER, awareness INTEGER, finance INTEGER, investigation INTEGER, '
                    'medicine INTEGER, occult INTEGER, politics INTEGER, science INTEGER, technology INTEGER)')

                cursor.execute('CREATE TABLE IF NOT EXISTS disciplines('
                               'obfuscate INTEGER, animalism INTEGER, potence INTEGER, dominate INTEGER, '
                               'auspex INTEGER, protean INTEGER, fortitude INTEGER, thin_blood_alchemy, '
                               'chemeristry INTEGER, seven INTEGER, myr INTEGER, selena INTEGER)')

                cursor.execute(
                    'CREATE TABLE IF NOT EXISTS willpower(willpowerBase INTEGER, willpowerSUP INTEGER, willpowerAGG INTEGER)')
                cursor.execute('CREATE TABLE IF NOT EXISTS health(healthBase INTEGER, healthSUP INTEGER, healthAGG INTEGER)')
                cursor.execute('CREATE TABLE IF NOT EXISTS ownerInfo(userID INTEGER, userNAME TEXT)')

                # ! Sep

                cursor.execute('INSERT INTO charAttributes('
                               'strength, dexterity, stamina, '
                               'charisma, manipulation, composure, '
                               'intelligence, wits, resolve) '
                               'VALUES(1,2,3, 1,2,3, 1,2,3)')

                cursor.execute('INSERT INTO physicalSkills ('
                               'athletics, brawl, craft, drive, firearms, larceny, '
                               'melee, stealth, survival) VALUES(1,2,3,4,5,6,7,8,9)')
                cursor.execute('INSERT INTO socialSkills (animal_ken, etiquette, insight, intimidation, leadership, performance, '
                               'persuasion, streetwise, subterfuge) VALUES(1,2,3,4,5,6,7,8,9)')
                cursor.execute('INSERT INTO mentalSkills (academics, awareness, finance, investigation, medicine, occult, '
                               'politics, science, technology) VALUES(1,2,3,4,5,6,7,8,9)')

                cursor.execute('INSERT INTO disciplines('
                               'obfuscate, animalism, potence, dominate, '
                               'auspex, protean, fortitude, thin_blood_alchemy, '
                               'chemeristry, seven, myr, selena)'
                               'VALUES(1,1,1,1, 1,1,1,1, 1,1,1,1)')

                cursor.execute('INSERT INTO willpower (willpowerBase, willpowerSUP, willpowerAGG) VALUES(5,0,0)')
                cursor.execute('INSERT INTO health (healthBase, healthSUP, healthAGG) VALUES(5,0,0)')
                cursor.execute('INSERT INTO userInfo (userID, userNAME) VALUES(0, "nada")')
                cursor.execute('UPDATE userInfo SET userID=?, userNAME=?', (int(ctx.author.id), f"{ctx.author}"))

                # !

                # CommandVars
                cursor.execute('CREATE TABLE IF NOT EXISTS commandVars(difficulty INTEGER, rollPool INTEGER, result INTEGER, poolComp TEXT)')

                cursor.execute('CREATE TABLE IF NOT EXISTS rerollInfo('
                               'regularCritDie INTEGER, hungerCritDie INTEGER, '
                               'regularSuccess INTEGER, hungerSuccess INTEGER, '
                               'regularFail INTEGER, hungerFail INTEGER, '
                               'hungerSkull INTEGER)')

                cursor.execute('CREATE TABLE IF NOT EXISTS charInfo(blood_potency INTEGER, clan TEXT, generation INTEGER, '
                               'bane_severity INTEGER, hunger INTEGER)')
                db.commit(); db.close()
                await ctx.send('Make Complete')
            except Exception as e:
                log.crit(f'>* Error With Making New Character {targetcharacter}: {e}')


async def setup(CLIENT):
    await CLIENT.add_cog(NewVampireRoll(CLIENT))
