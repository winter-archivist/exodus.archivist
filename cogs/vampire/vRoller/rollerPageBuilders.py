import sqlite3
from discord import Embed
from discord.ui import View
from zenlog import log

import misc.config.mainConfig as mC
import cogs.vampire.vMisc.vampireUtils as vU
import cogs.vampire.vRoller.rollerViews as rV


async def rollerPageDecider(interaction, target_page_name, initial_page) -> Embed and View:
    try:
        character_name = await vU.getCharacterName(interaction)
        with sqlite3.connect(f'cogs//vampire//characters//{str(interaction.user.id)}//{character_name}//{character_name}.sqlite') as db:
            cursor = db.cursor()
            match target_page_name:
                case 'roller.difficulty':
                    return_page, return_view = await difficultyPageBuilder(initial_page)
                case 'roller.attribute':
                    return_page, return_view = await attributePageBuilder(initial_page, cursor)
                case _:
                    log.error('**> Provided target_page_name does not exist.')
                    raise Exception('Provided target_page_name does not exist.')
        return return_page, return_view
    except sqlite3.Error as e:
        log.error(f'**> rollerPageDecider | SQLITE3 ERROR | {e}')


async def rollerBasicPageInformation(interaction, return_embed):
    character_name = await vU.getCharacterName(interaction)

    with sqlite3.connect(f'cogs//vampire//characters//{str(interaction.user.id)}//{character_name}//{character_name}.sqlite') as db:
        cursor = db.cursor()
        roll_pool = int(cursor.execute('SELECT rollPool FROM commandVars').fetchone()[0])
        difficulty = int(cursor.execute('SELECT difficulty from commandVars').fetchone()[0])
        roll_comp = cursor.execute('SELECT poolComp from commandVars').fetchone()[0]

    return_embed.add_field(name='Roll Information', value='', inline=False)
    return_embed.add_field(name='Roll Pool:', value=f'{roll_pool}')
    return_embed.add_field(name='Difficulty:', value=f'{difficulty}')
    return_embed.add_field(name='Roll Composition:', value=f'{roll_comp}')

    return return_embed


async def difficultyPageBuilder(return_page) -> Embed and View:
    return_page.add_field(name='Select Difficulty.', value='', inline=False)
    return_view = rV.KRV_DIFFICULTY
    return return_page, return_view


async def attributePageBuilder(return_embed, cursor):
    return 1, 1

