import discord
import sqlite3
from misc import ashen_utils as au


async def basicSelection(character, selectValues, roll_pool, pool_composition, targetTable, interaction):
    db = sqlite3.connect(f'{au.vePCDBLocation}{character}.sqlite')
    cursor = db.cursor()
    forVar = 0

    for x in selectValues:
        resultGrab = cursor.execute(f'SELECT {selectValues[forVar]} FROM {targetTable}')
        resultPull = resultGrab.fetchone()[0]
        roll_pool += resultPull
        pool_composition.append(f'{selectValues[forVar]}')
        forVar += 1
    db.close()
    await interaction.response.edit_message()
    return roll_pool

# Attribute Options
physicalAttributeOptions = [
            discord.SelectOption(
                label='Strength', value='strength',
                emoji='<:color_01_blood_red:1136744533812596906>',
            ),
            discord.SelectOption(
                label='Dexterity', value='dexterity',
                emoji='<:color_04_orange:1136744764201512981> ',
            ),
            discord.SelectOption(
                label='Stamina', value='stamina',
                emoji='<:color_08_dark_green:1136753193691381760>',
            )]

socialAttributeOptions = [
            discord.SelectOption(
                label='Charisma', value='charisma',
                emoji='<:color_01_blood_red:1136744533812596906>',
            ),
            discord.SelectOption(
                label='Manipulation', value='manipulation',
                emoji='<:color_04_orange:1136744764201512981> ',
            ),
            discord.SelectOption(
                label='Composure', value='composure',
                emoji='<:color_08_dark_green:1136753193691381760>',
            )]

mentalAttributeOptions = [
            discord.SelectOption(
                label='Intelligence', value='intelligence',
                emoji='<:color_01_blood_red:1136744533812596906>',
            ),
            discord.SelectOption(
                label='Wits', value='wits',
                emoji='<:color_04_orange:1136744764201512981> ',
            ),
            discord.SelectOption(
                label='Resolve', value='resolve',
                emoji='<:color_08_dark_green:1136753193691381760>',
            )]


# Skill Options
physicalSkillOptions = [
    discord.SelectOption(
        label='Athletics', value='athletics', emoji='<:snek:785811903938953227>'
    ),
    discord.SelectOption(
        label='Brawl', value='brawl', emoji='<:snek:785811903938953227>'
    ),
    discord.SelectOption(
        label='Craft', value='craft', emoji='<:snek:785811903938953227>'
    ),
    discord.SelectOption(
        label='Drive', value='drive', emoji='<:snek:785811903938953227>'
    ),
    discord.SelectOption(
        label='Firearms', value='firearms', emoji='<:snek:785811903938953227>'
    ),
    discord.SelectOption(
        label='Larceny', value='larceny', emoji='<:snek:785811903938953227>'
    ),
    discord.SelectOption(
        label='Melee', value='melee', emoji='<:snek:785811903938953227>'
    ),
    discord.SelectOption(
        label='Stealth', value='stealth', emoji='<:snek:785811903938953227>'
    ),
    discord.SelectOption(
        label='Survival', value='survival', emoji='<:snek:785811903938953227>'
    ), ]

socialSkillOptions = [
    discord.SelectOption(
        label='Animal Ken', value='animal_ken', emoji='<:snek:785811903938953227>'
    ),
    discord.SelectOption(
        label='Etiquette', value='etiquette', emoji='<:snek:785811903938953227>'
    ),
    discord.SelectOption(
        label='Insight', value='insight', emoji='<:snek:785811903938953227>'
    ),
    discord.SelectOption(
        label='Intimidation', value='intimidation', emoji='<:snek:785811903938953227>'
    ),
    discord.SelectOption(
        label='Leadership', value='leadership', emoji='<:snek:785811903938953227>'
    ),
    discord.SelectOption(
        label='Performance', value='performance', emoji='<:snek:785811903938953227>'
    ),
    discord.SelectOption(
        label='Persuasion', value='persuasion', emoji='<:snek:785811903938953227>'
    ),
    discord.SelectOption(
        label='Streetwise', value='streetwise', emoji='<:snek:785811903938953227>'
    ),
    discord.SelectOption(
        label='Subterfuge', value='subterfuge', emoji='<:snek:785811903938953227>'
    ), ]

mentalSkillOptions = [
    discord.SelectOption(
        label='Academics', value='academics', emoji='<:snek:785811903938953227>'
    ),
    discord.SelectOption(
        label='Awareness', value='awareness', emoji='<:snek:785811903938953227>'
    ),
    discord.SelectOption(
        label='Finance', value='finance', emoji='<:snek:785811903938953227>'
    ),
    discord.SelectOption(
        label='Investigation', value='investigation', emoji='<:snek:785811903938953227>'
    ),
    discord.SelectOption(
        label='Medicine', value='medicine', emoji='<:snek:785811903938953227>'
    ),
    discord.SelectOption(
        label='Occult', value='occult', emoji='<:snek:785811903938953227>'
    ),
    discord.SelectOption(
        label='Politics', value='politics', emoji='<:snek:785811903938953227>'
    ),
    discord.SelectOption(
        label='Science', value='science', emoji='<:snek:785811903938953227>'
    ),
    discord.SelectOption(
        label='Technology', value='technology', emoji='<:snek:785811903938953227>'
    ), ]


# Discipline Options
disciplineOptions = [
    discord.SelectOption(
        label='Obfuscate', value='obfuscate', emoji='<:snek:785811903938953227>'
    ),
    discord.SelectOption(
        label='Animalism', value='animalism', emoji='<:snek:785811903938953227>'
    ),
    discord.SelectOption(
        label='Potence', value='potence', emoji='<:snek:785811903938953227>'
    ),
    discord.SelectOption(
        label='Dominate', value='dominate', emoji='<:snek:785811903938953227>'
    ),
    discord.SelectOption(
        label='Auspex', value='auspex', emoji='<:snek:785811903938953227>'
    ),
    discord.SelectOption(
        label='Protean', value='protean', emoji='<:snek:785811903938953227>'
    ),
    discord.SelectOption(
        label='Fortitude', value='fortitude', emoji='<:snek:785811903938953227>'
    ),
    discord.SelectOption(
        label='Thinblood Alchemy', value='thin_blood_alchemy', emoji='<:snek:785811903938953227>'
    ),
    discord.SelectOption(
        label='Chemeristry', value='chemeristry', emoji='<:snek:785811903938953227>'
    ),
    discord.SelectOption(
        label='Seven', value='seven', emoji='<:snek:785811903938953227>'
    ),
    discord.SelectOption(
        label='Myr', value='myr', emoji='<:snek:785811903938953227>'
    ),
    discord.SelectOption(
        label='Selena', value='selena', emoji='<:snek:785811903938953227>'
    ),]


# Simple + & - Options
extraOptions = [
    discord.SelectOption(
        label='One', value='1', emoji='<:snek:785811903938953227>'
    ),
    discord.SelectOption(
        label='Two', value='2', emoji='<:snek:785811903938953227>'
    ),
    discord.SelectOption(
        label='Three', value='3', emoji='<:snek:785811903938953227>'
    ),
    discord.SelectOption(
        label='Four', value='4', emoji='<:snek:785811903938953227>'
    ),
    discord.SelectOption(
        label='Five', value='5', emoji='<:snek:785811903938953227>'
    ),
    discord.SelectOption(
        label='Minus One', value='-1', emoji='<:snek:785811903938953227>'
    ),
    discord.SelectOption(
        label='Minus Two', value='-2', emoji='<:snek:785811903938953227>'
    ),
    discord.SelectOption(
        label='Minus Three', value='-3', emoji='<:snek:785811903938953227>'
    ),
    discord.SelectOption(
        label='Minus Four', value='-4', emoji='<:snek:785811903938953227>'
    ),
    discord.SelectOption(
        label='Minus Five', value='-5', emoji='<:snek:785811903938953227>')]
