import sqlite3
from discord import Embed
from discord.ui import View
from zenlog import log

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
                    return_page, return_view = await attributePageBuilder(initial_page)
                case 'roller.physical':
                    return_page, return_view = await physicalPageBuilder(initial_page)
                case 'roller.social':
                    return_page, return_view = await socialPageBuilder(initial_page)
                case 'roller.mental':
                    return_page, return_view = await mentalPageBuilder(initial_page)
                case 'roller.discipline':
                    return_page, return_view = await disciplinePageBuilder(initial_page)
                case 'roller.extras':
                    return_page, return_view = await extrasPageBuilder(initial_page)
                case 'roller.rolled':
                    return_page, return_view = await rolledPageBuilder(initial_page)
                case 'roller.rerolled':
                    return_page, return_view = await rerolledPageBuilder(initial_page)
                case _:
                    log.error('**> Provided target_page_name does not exist.')
                    raise Exception('Provided target_page_name does not exist.')
        return return_page, return_view
    except sqlite3.Error as e:
        log.error(f'**> rollerPageDecider | SQLITE3 ERROR | {e}')


async def rollerBasicPageInformation(interaction, return_page):
    character_name = await vU.getCharacterName(interaction)

    with sqlite3.connect(f'cogs//vampire//characters//{str(interaction.user.id)}//{character_name}//{character_name}.sqlite') as db:
        cursor = db.cursor()
        roll_pool = int(cursor.execute('SELECT rollPool FROM commandVars').fetchone()[0])
        difficulty = int(cursor.execute('SELECT difficulty from commandVars').fetchone()[0])
        roll_comp = cursor.execute('SELECT poolComp from commandVars').fetchone()[0]

    return_page.add_field(name='Roll Pool:', value=f'{roll_pool}')
    return_page.add_field(name='Difficulty:', value=f'{difficulty}')
    return_page.add_field(name='Roll Composition:', value=f'{roll_comp}')

    return return_page


async def difficultyPageBuilder(return_page) -> Embed and View:
    return_view = rV.KRV_DIFFICULTY
    return return_page, return_view


async def attributePageBuilder(return_page):
    return_view = rV.KRV_ATTRIBUTE
    return return_page, return_view


async def physicalPageBuilder(return_page) -> Embed and View:
    return_view = rV.KRV_PHYSICAL
    return return_page, return_view


async def socialPageBuilder(return_page) -> Embed and View:
    return_view = rV.KRV_SOCIAL
    return return_page, return_view


async def mentalPageBuilder(return_page) -> Embed and View:
    return_view = rV.KRV_MENTAL
    return return_page, return_view


async def disciplinePageBuilder(return_page) -> Embed and View:
    return_view = rV.KRV_DISCIPLINE
    return return_page, return_view


async def extrasPageBuilder(return_page) -> Embed and View:
    return_view = rV.KRV_EXTRAS
    return return_page, return_view


async def rolledPageBuilder(return_page) -> Embed and View:
    return_view = rV.KRV_ROLLED
    return return_page, return_view


async def rerolledPageBuilder(return_page) -> Embed and View:
    return_view = rV.KRV_REROLLED
    return return_page, return_view
