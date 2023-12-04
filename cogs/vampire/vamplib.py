import discord
from discord.ui import View
from zenlog import log

import sqlite3
from random import randint
import os

from cogs.vampire.selections import selections as s
from misc.utils import yaml_utils as yu
from misc.config import main_config as mc

selection_embed = discord.Embed(title='', description=f'', color=mc.embed_colors["purple"])
selection_embed.add_field(name='Roll Information', value='', inline=False)
selection_embed.add_field(name='Roll Pool:', value=f'N/A')
selection_embed.add_field(name='Difficulty:', value=f'N/A')
selection_embed.add_field(name='Roll Composition:', value=f'N/A')

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


async def rouseCheck(interaction, targetcharacter) -> str:
    with sqlite3.connect(f'cogs//vampire//characters//{str(interaction.user.id)}//{targetcharacter}.sqlite') as db:
        cursor = db.cursor()
        hunger_grab = cursor.execute('SELECT hunger from charInfo')
        hunger: int = int(hunger_grab.fetchone()[0])
        rouse_num_result: int = randint(1, 10)
        if hunger >= 5:
            db.close()
            if rouse_num_result <= 5:
                return 'Frenzy'  # * Hunger Frenzy, No Hunger Gain Too High Already
            return 'Hungry'

        elif rouse_num_result >= 6:
            db.close()
            return 'Pass'  # * No Hunger Gain

        elif rouse_num_result <= 5:
            cursor.execute('UPDATE charInfo SET hunger=?', (str(int(hunger + 1))))
            db.commit();
            db.close()
            return 'Fail'  # * Hunger Gain


async def selectionEmbedSetter(interaction, targetcharacter) -> None:
    db = sqlite3.connect(f'cogs//vampire//characters//{str(interaction.user.id)}//{targetcharacter}.sqlite'); cursor = db.cursor()
    roll_pool_grab = cursor.execute('SELECT rollPool FROM commandVars')
    roll_pool = int(roll_pool_grab.fetchone()[0])

    difficulty_grab = cursor.execute('SELECT difficulty from commandVars')
    difficulty: int = int(difficulty_grab.fetchone()[0])

    roll_pool_comp_grab = cursor.execute('SELECT poolComp from commandVars')
    roll_comp = roll_pool_comp_grab.fetchone()[0]

    url_grab = cursor.execute('SELECT imgURL from charInfo')
    url = url_grab.fetchone()[0]
    db.close()

    selection_embed.set_field_at(index=1, name='Roll Pool:', value=f'{roll_pool}')
    selection_embed.set_field_at(index=2, name='Difficulty:', value=f'{difficulty}')
    selection_embed.set_field_at(index=3, name='Roll Composition:', value=f'{roll_comp}')
    selection_embed.set_thumbnail(url=f'{url}')


async def rollInitialize(interaction, charactername) -> bool:
    # ! Runs every time someone uses the /vroll command
    targetDB = f'cogs//vampire//characters//{str(interaction.user.id)}//{charactername}.sqlite'

    log.debug(f'> Checking if [ `{targetDB}` ] exists')
    if not os.path.exists(targetDB):
        log.warn(f'*> Database [ `{targetDB}` ] does not exist')
        await interaction.response.send_message(embed=discord.Embed(
            title='Database Error', color=mc.embed_colors["red"], description=f'[ `{charactername}` ] Does not Exist. \n\n {mc.ISSUE_CONTACT}'), ephemeral=True)
        return False
    else:
        log.debug(f'> Successful Connection to [ `{targetDB}` ]')

    db = sqlite3.connect(targetDB); cursor = db.cursor()
    charOwnerResultGrab = cursor.execute('SELECT userID FROM ownerInfo')
    char_owner_id = charOwnerResultGrab.fetchone()[0]
    if char_owner_id != interaction.user.id:  # ? If interaction user doesn't own the character
        db.close()
        await interaction.response.send_message(f'You don\'t own {charactername}', ephemeral=True)
        return False

    # ? Resets commandvars & reroll_info
    cursor.execute(
        'UPDATE commandvars SET difficulty=?, rollPool=?, result=?, poolComp=?',
        (0, 0, 0, 'N/A'), )
    cursor.execute(
        'UPDATE rerollInfo SET regularCritDie=?, hungerCritDie=?, regularSuccess=?, '
        'hungerSuccess=?, regularFail=?, hungerFail=?, hungerSkull=?',
        (0, 0, 0, 0, 0, 0, 0), )

    url_grab = cursor.execute('SELECT imgURL from charInfo')
    url = url_grab.fetchone()[0]
    selection_embed.set_thumbnail(url=f'{url}')

    db.commit(); db.close()

    targetCache = f'cogs/vampire/characters/{str(interaction.user.id)}/{str(interaction.user.id)}.yaml'
    await yu.cacheClear(targetCache)
    await yu.cacheWrite(targetCache, dataInput={'characterName': f'{charactername}'})
    return True


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
    charOwnerResultGrab = db.cursor().execute('SELECT userID FROM ownerInfo')
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

        await selectionEmbedSetter(interaction, targetcharacter)

        await interaction.response.edit_message(embed=selection_embed, view=StandardAttributeSelectionView(self.CLIENT))

    @discord.ui.button(label='Blood Surge', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.red, row=4)
    async def blood_surge_button_callback(self, interaction, button):
        targetcharacter = await ownerChecker(interaction)
        if targetcharacter is str:
            pass
        elif targetcharacter is False:
            return

        rouse_result = await rouseCheck(interaction, targetcharacter)
        if rouse_result in ('Frenzy', 'Hungry'):
            button.disabled = True
            button.style = discord.ButtonStyle.gray

            if rouse_result == 'Frenzy':
                button.label = 'Broken Chains.'
                # ! DO FRENZY STUFF HERE

            elif rouse_result == 'Hungry':
                button.label = 'Too Hungry, Feast.'

            await interaction.response.edit_message(view=self)
            return
        elif rouse_result == 'Pass':
            button.label = 'The Beast\'s Lock Rattles, Hunger Avoided.'
        elif rouse_result == 'Fail':
            button.label = 'Blood Boils Within, Hunger Gained.'

        db = sqlite3.connect(f'cogs//vampire//characters//{str(interaction.user.id)}//{targetcharacter}.sqlite'); cursor = db.cursor()

        bp_grab = cursor.execute('SELECT blood_potency FROM charInfo')
        bp: int = int(bp_grab.fetchone()[0])
        bp_mapping = {1: 2,  2: 2,  3: 3,  4: 3,  5: 4,  6: 5}
        bp_add = bp_mapping[bp]

        roll_pool_grab = cursor.execute('SELECT rollPool FROM commandvars')
        new_roll_pool: int = int(roll_pool_grab.fetchone()[0] + bp_add)
        cursor.execute('UPDATE commandvars SET rollPool=?', (new_roll_pool,))
        cursor.execute('UPDATE commandvars SET poolComp=?', (f"Blood Surge[{bp_add}], ", ))
        db.commit(); db.close()

        await selectionEmbedSetter(interaction, targetcharacter)

        button.disabled = True
        button.style = discord.ButtonStyle.gray
        await interaction.response.edit_message(embed=selection_embed, view=self)

    @discord.ui.select(placeholder='Select Difficulty', options=difficulty_options, max_values=1, min_values=1)
    async def difficulty_select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        targetcharacter = await ownerChecker(interaction)
        if targetcharacter is str:
            pass
        elif targetcharacter is False:
            return

        db = sqlite3.connect(f'cogs//vampire//characters//{str(interaction.user.id)}//{targetcharacter}.sqlite'); cursor = db.cursor()
        cursor.execute('UPDATE commandvars SET difficulty=?', select.values)
        db.commit(); db.close()

        await selectionEmbedSetter(interaction, targetcharacter)

        await interaction.response.edit_message(embed=selection_embed, view=self)


class StandardAttributeSelectionView(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT
