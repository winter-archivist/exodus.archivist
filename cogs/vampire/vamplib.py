import discord
from discord.ui import View
from zenlog import log

import sqlite3

from cogs.vampire.selections import selections as s
from misc.utils import yaml_utils as yu
from misc.config import main_config as mc


selection_embed_base = discord.Embed(title='', description=f'', color=mc.embed_colors["purple"])
roll_embed_embed_base = discord.Embed(title='Roll', description=f'', color=mc.embed_colors["purple"])
roll_details_embed_base = discord.Embed(title='Extra Details:',description=f'{mc.ISSUE_CONTACT}',color=mc.embed_colors["black"])
not_enough_wp_embed_base = discord.Embed(title='Willpower Reroll', description=f'You don\'t have enough willpower. {mc.ISSUE_CONTACT}', color=mc.embed_colors["red"])
difficulty_options = [
    discord.SelectOption(
        label='Zero', value='0', emoji='<:snek:785811903938953227>'
    ),
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
        label='Six', value='6', emoji='<:snek:785811903938953227>'
    ),
    discord.SelectOption(
        label='Seven', value='7', emoji='<:snek:785811903938953227>'
    ),
    discord.SelectOption(
        label='Eight', value='8', emoji='<:snek:785811903938953227>'
    ),
    discord.SelectOption(
        label='Nine', value='9', emoji='<:snek:785811903938953227>'
    ),
    discord.SelectOption(
        label='Ten', value='10', emoji='<:snek:785811903938953227>'
    ),
    discord.SelectOption(
        label='Eleven', value='11', emoji='<:snek:785811903938953227>'
    ),
    discord.SelectOption(
        label='Twelve', value='12', emoji='<:snek:785811903938953227>'
    ),
    discord.SelectOption(
        label='Thirteen', value='13', emoji='<:snek:785811903938953227>'
    )]


async def rollInitialize(interaction, charactername):
    # ! Runs every time someone uses the /vroll command
    db = sqlite3.connect(f'cogs//vampire//characters//{str(interaction.user.id)}//{charactername}.sqlite')
    charOwnerResultGrab = db.cursor().execute('SELECT userID FROM charOwner')

    if charOwnerResultGrab.fetchone()[0] != f'{interaction.user}':  # ? If interaction user doesn't own the character
        db.close()
        await interaction.response.send_message(f'You don\'t own {charactername}')
        return

    # ? Resets commandvars & reroll_info
    db.cursor().execute(
        'UPDATE commandvars SET difficulty=?, rollPool=?, result=?, pool_composition=?',
        (0, 0, 0, 'N/A'), )
    db.cursor().execute(
        'UPDATE reroll_info SET regularCritDie=?, hungerCritDie=?, regularSuccess=?, '
        'hungerSuccess=?, regularFail=?, hungerFail=?, hungerSkull=?',
        (0, 0, 0, 0, 0, 0, 0), )

    db.commit(); db.close()  # ! DON'T REMOVE

    # ? Writes the name of the current user.id's targetcharacter
    log.crit(f'{charactername=}')
    targetCache = f'cogs/vampire/characters/{str(interaction.user.id)}/{str(interaction.user.id)}.yaml'
    await yu.cacheClear(targetCache)
    await yu.cacheWrite(targetCache, dataInput={'characterName': f'{charactername}'})


async def ownerChecker(interaction: discord.Interaction) -> bool:
    # ! Runs basically any time someone does anything related to the vtm roller
    # ? Standard Usage:
    """
    if not await ownerChecker(interaction):
        return
    pass  # ! Real Code Here
    """

    # ! The following system is designed in such a way a user can have multiple characters, this'd be easier otherwise.
    # ! Also, the reasoning of the if/elif at the bottom is to allow easier use of custom logic around the function
    # ! Everytime this is used there is always some kind of custom logic when you return True
    # ! It's a not particularly great solution, but it works!

    # ? Grabs the current targeted character name of the user interacting with the interaction
    targetCache = f'cogs/vampire/characters/{str(interaction.user.id)}/{str(interaction.user.id)}.yaml'
    data = await yu.cacheRead(f'{targetCache}')
    use_data: dict = {}
    use_data.update(data)
    targetcharacter: str = str(use_data['characterName'])

    # ? Grabs the character owner's ID from targeted character
    db = sqlite3.connect(f'cogs//vampire//characters//{str(interaction.user.id)}//{targetcharacter}.sqlite')
    charOwnerResultGrab = db.cursor().execute('SELECT userID FROM charOwner')
    char_owner: str = str(charOwnerResultGrab.fetchone()[0])

    # ? Checks if the user.id is the same as the character's ownerID
    db.close()
    if char_owner != interaction.user.id:  # ! User doesn't own the Character
        await interaction.followup.send_message(f'> You don\'t own any characters named: `{targetcharacter}`. \n'
                                                f'Please double check the name input and try again, '
                                                f'otherwise please contact `{mc.RUNNER}` or `{mc.DEVELOPER}`')
        return False
    elif char_owner == interaction.user.id:  # ! User does own the Character
        return True
    else:
        log.crit('>** ownerChecker() Err.001')
        return False


async def standardMake(ctx, cursor):
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
    cursor.execute('CREATE TABLE IF NOT EXISTS charOwner(userID INTEGER, userNAME TEXT)')

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

    cursor.execute('INSERT INTO charOwner (userID, userNAME) VALUES(0, "nada")')
    cursor.execute('UPDATE charOwner SET userID=?, userNAME=?', (int(ctx.author.id), f"{ctx.author}"))


class DifficultySelectionView(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Next Step', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=4)
    async def stepper_button_callback(self, interaction, button):
        if not await ownerChecker(interaction):
            return
        working_embed = 1
        working_embed = selection_embed_base.set_field_at(index=0, name='Select Your:', value='Attribute')
        await interaction.response.edit_message(embed=working_embed, view=StandardAttributeSelectionView(self.CLIENT))

    @discord.ui.button(label='Blood Surge', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=4)
    async def blood_surge_button_callback(self, interaction, button):
        if not await ownerChecker(interaction):
            return
        pass

    @discord.ui.select(
        placeholder='Select Difficulty',
        options=difficulty_options)
    async def extra_select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        if not await ownerChecker(interaction):
            return
        pass

        global roll_pool
        forVar = 0

        for x in select.values:
            roll_pool += int(select.values[forVar])
            pool_composition.append(f'{int(select.values[forVar])}')
            forVar += 1

        await interaction.response.edit_message()



