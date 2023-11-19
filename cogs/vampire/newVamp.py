import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import View

import sqlite3
from random import randint

from misc.config import main_config as mc
from misc.utils import interaction_utils as iu
from misc.utils import yaml_utils as yu
from cogs.vampire.selections import selections as s
from cogs.vampire import vamplib as vl


async def standardMake(cursor):
    # Physical
    cursor.execute('CREATE TABLE IF NOT EXISTS physicalAttributes(strength INTEGER, dexterity INTEGER, stamina INTEGER)')
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS physicalSkills(athletics INTEGER, brawl INTEGER, craft INTEGER, drive INTEGER, '
        'firearms INTEGER, larceny INTEGER, melee INTEGER, stealth INTEGER, survival INTEGER)')

    # Social
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS socialAttributes(charisma INTEGER, manipulation INTEGER, composure INTEGER)')
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS socialSkills(animal_ken INTEGER, etiquette INTEGER, insight INTEGER, intimidation INTEGER, '
        'leadership INTEGER, performance INTEGER, persuasion INTEGER, streetwise INTEGER, subterfuge INTEGER)')

    # Mental
    cursor.execute('CREATE TABLE IF NOT EXISTS mentalAttributes(intelligence INTEGER, wits INTEGER, resolve INTEGER)')
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS mentalSkills(academics INTEGER, awareness INTEGER, finance INTEGER, investigation INTEGER, '
        'medicine INTEGER, occult INTEGER, politics INTEGER, science INTEGER, technology INTEGER)')

    # Disciplines
    cursor.execute('CREATE TABLE IF NOT EXISTS disciplines('
                   'obfuscate INTEGER, animalism INTEGER, potence INTEGER, dominate INTEGER, '
                   'auspex INTEGER, protean INTEGER, fortitude INTEGER, thin_blood_alchemy, '
                   'chemeristry INTEGER, seven INTEGER, myr INTEGER, selena INTEGER)')

    # Other
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS willpower(willpowerBase INTEGER, willpowerSUP INTEGER, willpowerAGG INTEGER)')
    cursor.execute('CREATE TABLE IF NOT EXISTS health(healthBase INTEGER, healthSUP INTEGER, healthAGG INTEGER)')
    cursor.execute('CREATE TABLE IF NOT EXISTS hunger(hungerCount INTEGER)')
    cursor.execute('CREATE TABLE IF NOT EXISTS charOwner(userID TEXT)')

    # Basic Value Input into Blank Vampire DB

    # Physical
    cursor.execute('INSERT INTO physicalAttributes (strength, dexterity, stamina) VALUES(1,2,3)')
    cursor.execute(
        'INSERT INTO physicalSkills (athletics, brawl, craft, drive, firearms, larceny, melee, stealth, survival) '
        'VALUES(1,2,3,4,5,6,7,8,9)')

    # Social
    cursor.execute('INSERT INTO socialAttributes (charisma, manipulation, composure) VALUES(1,2,3)')
    cursor.execute('INSERT INTO socialSkills (animal_ken, etiquette, insight, intimidation, leadership, performance, '
                   'persuasion, streetwise, subterfuge)'
                   'VALUES(1,2,3,4,5,6,7,8,9)')

    # Mental
    cursor.execute('INSERT INTO mentalAttributes (intelligence, wits, resolve) VALUES(1,2,3)')
    cursor.execute('INSERT INTO mentalSkills (academics, awareness, finance, investigation, medicine, occult, '
                   'politics, science, technology)'
                   'VALUES(1,2,3,4,5,6,7,8,9)')

    # Disciplines
    # seven is Temporis
    # myr is Dementation
    # selena is Nihilistics
    cursor.execute('INSERT INTO disciplines('
                   'obfuscate, animalism, potence, dominate, '
                   'auspex, protean, fortitude, thin_blood_alchemy, '
                   'chemeristry, seven, myr, selena)'
                   'VALUES(1,1,1,1, 1,1,1,1, 1,1,1,1)')

    # Other
    cursor.execute('INSERT INTO willpower (willpowerBase, willpowerSUP, willpowerAGG) VALUES(5,0,0)')
    cursor.execute('INSERT INTO health (healthBase, healthSUP, healthAGG) VALUES(5,0,0)')
    cursor.execute('INSERT INTO hunger (hungerCount) VALUES(1)')
    cursor.execute('INSERT INTO charOwner (userID) VALUES("")')


class StandardView(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT


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

        # ! JUST TO MAKE SURE I TEST THE RIGHT ONE
        if charactername != 'debug':
            return
        else:
            pass
        # ! JUST TO MAKE SURE I TEST THE RIGHT ONE

        match choices.value:
            case 'standard':
                await vl.rollInitialize(interaction, charactername)
                working_embed = 'ERROR WITH working_embed'
                # ? WORKING EMBED MAY BE CHANGED
                working_embed = vl.selection_embed_base.add_field(name='Select Your:', value='Attribute')
                await interaction.response.send_message(embed=working_embed, view=StandardView(self.CLIENT))
                # ! JUST WORK ABOVE
                # ? JUST WORK ABOVE
                # * JUST WORK ABOVE
                # ! JUST WORK ABOVE
                # * JUST WORK ABOVE
                # ? JUST WORK ABOVE
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
            db = sqlite3.connect(f'cogs//vampire//characters//{str(ctx.author.id)}//{targetcharacter}.sqlite')
            cursor = db.cursor()
            await standardMake(db)

            # CommandVars
            cursor.execute('CREATE TABLE IF NOT EXISTS commandvars(difficulty INTEGER, rollPool INTEGER, result INTEGER, pool_composition TEXT)')

            cursor.execute('CREATE TABLE IF NOT EXISTS reroll_info('
                           'regularCritDie INTEGER, hungerCritDie INTEGER, '
                           'regularSuccess INTEGER, hungerSuccess INTEGER, '
                           'regularFail INTEGER, hungerFail INTEGER, '
                           'hungerSkull INTEGER)')
            db.commit()
            db.close()


async def setup(CLIENT):
    await CLIENT.add_cog(NewVampireRoll(CLIENT))
