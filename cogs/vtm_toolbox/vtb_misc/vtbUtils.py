import sqlite3
from os import path
from zenlog import log
from discord import Embed
from random import randint

import misc.utils.yamlUtils as yU
import misc.config.mainConfig as mC


async def writeCharacterName(interaction, character_name) -> bool:
    targetDB = f'cogs//vampire//vtb_characters//{str(interaction.user.id)}//{character_name}//{character_name}.sqlite'

    log.debug(f'> Checking if [ `{targetDB}` ] exists')
    if not path.exists(targetDB):
        log.warn(f'*> Database [ `{targetDB}` ] does not exist')
        await interaction.response.send_message(embed=Embed(title='Database Error', color=mC.EMBED_COLORS["red"],
                                                            description=f'[ `{character_name}` ] Does Not Exist..'), ephemeral=True)
        return False
    else:
        log.debug(f'> Successful Connection to [ `{targetDB}` ]')

    with sqlite3.connect(targetDB) as db:
        char_owner_id = db.cursor().execute('SELECT userID FROM ownerInfo').fetchone()[0]
        if char_owner_id != interaction.user.id:  # ? If interaction user doesn't own the character
            await interaction.response.send_message(f'You don\'t own {character_name}', ephemeral=True)
            return False

        targetCache = f'cogs/vampire/vtb_characters/{str(interaction.user.id)}/{str(interaction.user.id)}.yaml'
        await yU.cacheClear(targetCache)
        await yU.cacheWrite(targetCache, dataInput={'characterName': f'{character_name}'})

    return True


async def ownerCheck(interaction):
    character_name = await getCharacterName(interaction)
    targetDB = f'cogs//vampire//vtb_characters//{str(interaction.user.id)}//{character_name}//{character_name}.sqlite'
    with sqlite3.connect(targetDB) as db:
        char_owner_id = db.cursor().execute('SELECT userID FROM ownerInfo').fetchone()[0]
        if char_owner_id != interaction.user.id:  # ? If interaction user doesn't own the character
            return False
        else:
            return True
    pass


async def getCharacterName(interaction) -> str:
    target_cache = f'cogs/vampire/vtb_characters/{str(interaction.user.id)}/{str(interaction.user.id)}.yaml'
    use_data: dict = {}
    use_data.update(await yU.cacheRead(f'{target_cache}'))
    character_name: str = str(use_data['characterName'])
    return character_name


async def rouseCheck(interaction) -> str:
    character_name: str = await getCharacterName(interaction)
    try:
        with sqlite3.connect(f'cogs//vampire//vtb_characters//{str(interaction.user.id)}//{character_name}//{character_name}.sqlite') as db:
            cursor = db.cursor()
            hunger = int(cursor.execute('SELECT hunger from charInfo').fetchone()[0])
            rouse_num_result: int = randint(1, 10)

            if hunger >= 5:
                # TODO: HANDLE FRENZY STUFF
                return 'Frenzy'  # * Hunger Frenzy, No Hunger Gain Too High Already

            elif rouse_num_result >= 6:
                return 'Pass'  # * No Hunger Gain

            elif rouse_num_result <= 5:
                cursor.execute('UPDATE charInfo SET hunger=?', (str(int(hunger + 1))))
                db.commit()
                return 'Fail'  # * Hunger Gain
    except sqlite3.Error as e:
        log.error(f'rouseCheck | SQLITE3 ERROR | {e}')


async def rollPrep(interaction, character_name: str = 'None'):

    if character_name == 'None':
        character_name = await getCharacterName(interaction)

    # This will be fixed in the future, I just want to get this small thing pushed out soon.
    # For more info, just look up "atrocious" in rollerViews.py
    await yU.cacheClear(f'cogs//vampire//vtb_characters//{str(interaction.user.id)}//{character_name}//roll_mark.yaml')

    with sqlite3.connect(f'cogs//vampire//vtb_characters//{str(interaction.user.id)}//{character_name}//{character_name}.sqlite') as db:
        cursor = db.cursor()  # ? Resets commandvars & reroll_info
        cursor.execute('UPDATE commandvars SET difficulty=?, rollPool=?, result=?, poolComp=?', (0, 0, 0, 'Base[0]'), )
        cursor.execute('UPDATE rerollInfo SET regularCritDie=?, hungerCritDie=?, regularSuccess=?, hungerSuccess=?, regularFail=?, hungerFail=?, hungerSkull=?', (0, 0, 0, 0, 0, 0, 0), )
        db.commit()
