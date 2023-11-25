import discord
from discord.ui import View
from zenlog import log

import sqlite3

from cogs.vampire.selections import selections as s
from misc.utils import yaml_utils as yu
from misc.config import main_config as mc

selection_embed_base = discord.Embed(title='', description=f'', color=mc.embed_colors["purple"])
roll_embed_embed_base = discord.Embed(title='Roll', description=f'', color=mc.embed_colors["purple"])
roll_details_embed_base = discord.Embed(title='Extra Details:', description=f'{mc.ISSUE_CONTACT}', color=mc.embed_colors["black"])
not_enough_wp_embed_base = discord.Embed(title='Willpower Reroll',
                                         description=f'You don\'t have enough willpower. {mc.ISSUE_CONTACT}',
                                         color=mc.embed_colors["red"])
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
    char_owner_id = charOwnerResultGrab.fetchone()[0]
    if char_owner_id != interaction.user.id:  # ? If interaction user doesn't own the character
        db.close()
        await interaction.response.send_message(msg=f'You don\'t own {charactername}', ephemeral=True)
        return False

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
    targetCache = f'cogs/vampire/characters/{str(interaction.user.id)}/{str(interaction.user.id)}.yaml'
    await yu.cacheClear(targetCache)
    await yu.cacheWrite(targetCache, dataInput={'characterName': f'{charactername}'})


async def ownerChecker(interaction: discord.Interaction):
    # ! Runs basically any time someone does anything related to the vtm roller
    # ? Standard Usage:
    """
    targetcharacter = await ownerChecker(interaction)
    if targetcharacter is str: pass
    elif targetcharacter is False: return
    pass  # ! Real Code Here
    """

    # ! The following system is designed in such a way a user can have multiple characters, this'd be easier otherwise.
    # ! Also, the reasoning of the if/elif at the bottom is to allow easier use of custom logic around the function
    # ! Everytime this is used there is always some kind of custom logic when you return True
    # ! It's a not particularly great solution, but it works!

    # ? READS targetcharacter from proper .yaml
    targetCache = f'cogs/vampire/characters/{str(interaction.user.id)}/{str(interaction.user.id)}.yaml'
    data = await yu.cacheRead(f'{targetCache}')
    use_data: dict = {}
    use_data.update(data)
    targetcharacter: str = str(use_data['characterName'])

    # ? READS the character owner's id in the proper character (Just insurance)
    db = sqlite3.connect(f'cogs//vampire//characters//{str(interaction.user.id)}//{targetcharacter}.sqlite')
    charOwnerResultGrab = db.cursor().execute('SELECT userID FROM userInfo')
    char_owner_id = charOwnerResultGrab.fetchone()[0]
    char_owner_id: int = int(char_owner_id)

    # ? Checks if the user.id is the same as the character's ownerID
    # ? If they DON'T, it just tells the person using the command that, and return False
    # ? If they DO, then it returns the targetcharacter
    db.close()
    if char_owner_id != interaction.user.id:  # ! User does __NOT__ own the Character
        await interaction.response.send_message(f'> You don\'t own any characters named: `{targetcharacter}`.\n\n'
                                                f'Please double check the name input and try again, otherwise please contact\n'
                                                f'* Bot\'s Current Runner:`{mc.RUNNER}`\n'
                                                f'* Bot\'s Current Developer: `{mc.DEVELOPER}`')
        return False
    elif char_owner_id == interaction.user.id:  # ! User __DOES__ own the Character
        return targetcharacter


class StandardStartSelectionView(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Next Step', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=4)
    async def stepper_button_callback(self, interaction, button):
        targetcharacter = await ownerChecker(interaction)
        if targetcharacter is str:
            pass
        elif targetcharacter is False:
            return

        db = sqlite3.connect(f'cogs//vampire//characters//{str(interaction.user.id)}//{targetcharacter}.sqlite'); cursor = db.cursor()
        rollPoolGrab = cursor.execute('SELECT rollPool FROM commandvars')
        roll_pool = int(rollPoolGrab.fetchone()[0])
        rollPoolCompGrab = cursor.execute('SELECT poolComp from commandvars')  # ! ROLL COMP
        roll_pool_composition = rollPoolCompGrab.fetchall()  # ! ROLL COMP FETCH
        log.crit(f'{roll_pool_composition=}')
        db.close()

        working_embed = selection_embed_base.add_field(name='Initial Roll Information', value='')
        working_embed.add_field(name='Roll Pool:', value=f'{roll_pool}')
        working_embed.add_field(name='Roll Composition:', value=f'{roll_pool_composition}')  # ! THIS NEEDS TO ACTUALLY WORK
        await interaction.response.edit_message(embed=working_embed, view=StandardAttributeSelectionView(self.CLIENT))

    @discord.ui.button(label='Blood Surge', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.red, row=4)
    async def blood_surge_button_callback(self, interaction, button):
        # ! THIS NEEDS TO ALSO CHECK HUNGER AND MAKE A ROUSE!!!!
        targetcharacter = await ownerChecker(interaction)
        if targetcharacter is str:
            pass
        elif targetcharacter is False:
            return

        db = sqlite3.connect(f'cogs//vampire//characters//{str(interaction.user.id)}//{targetcharacter}.sqlite'); cursor = db.cursor()
        hungerGrab = cursor.execute('SELECT hungerCount from hunger')

        rollPoolGrab = cursor.execute('SELECT rollPool FROM commandvars')
        new_roll_pool = int(rollPoolGrab.fetchone()[0] + 2)
        cursor.execute('UPDATE commandvars SET rollPool=?', (new_roll_pool,))
        db.commit(); db.close()

        button.disabled = True
        button.label = 'Blood Surged'
        button.style = discord.ButtonStyle.gray
        await interaction.response.edit_message(view=self)

    @discord.ui.select(placeholder='Select Difficulty', options=difficulty_options)
    async def extra_select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        if not await ownerChecker(interaction):
            return
        pass
        """

        forVar = 0

        for x in select.values:
            roll_pool += int(select.values[forVar])
            pool_composition.append(f'{int(select.values[forVar])}')
            forVar += 1
        """
        await interaction.response.edit_message()


class StandardAttributeSelectionView(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT
