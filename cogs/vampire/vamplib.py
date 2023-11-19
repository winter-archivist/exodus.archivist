import discord
import sqlite3
from misc.utils import yaml_utils as yu
from misc.config import main_config as mc


selection_embed_base = discord.Embed(title='', description=f'', color=mc.embed_colors["purple"])
roll_embed_embed_base = discord.Embed(title='Roll', description=f'', color=mc.embed_colors["purple"])
roll_details_embed_base = discord.Embed(title='Extra Details:',description=f'{mc.ISSUE_CONTACT}',color=mc.embed_colors["black"])
not_enough_wp_embed_base = discord.Embed(title='Willpower Reroll', description=f'You don\'t have enough willpower. {mc.ISSUE_CONTACT}', color=mc.embed_colors["red"])


async def rollInitialize(interaction, charactername):
    db = sqlite3.connect(f'cogs//vampire//characters//{str(interaction.user.id)}//{charactername}.sqlite')
    cursor = db.cursor()
    charOwnerResultGrab = cursor.execute('SELECT userID FROM charOwner')

    if charOwnerResultGrab.fetchone()[0] != f'{interaction.user}':
        db.close()
        await interaction.response.send_message(f'You don\'t own {charactername}')
        return

    cursor.execute(  # ! Resets commandvars
        'UPDATE commandvars SET difficulty=?, rollPool=?, result=?, pool_composition=?',
        (0, 0, 0, 'N/A'), )
    cursor.execute(  # ! Resets reroll_info
        'UPDATE reroll_info SET regularCritDie=?, hungerCritDie=?, regularSuccess=?, '
        'hungerSuccess=?, regularFail=?, hungerFail=?, hungerSkull=?',
        (0, 0, 0, 0, 0, 0, 0), )
    db.commit(); db.close()

    targetCache = f'cogs/vampire/characters/{str(interaction.user.id)}/{str(interaction.user.id)}.yaml'
    await yu.cacheClear(targetCache)
    await yu.cacheWrite(targetCache, dataInput={'characterName': f'{charactername}'})