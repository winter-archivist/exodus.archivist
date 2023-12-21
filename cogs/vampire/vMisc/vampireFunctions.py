import discord
import sqlite3
from zenlog import log
from os import path
from random import randint

import cogs.vampire.vMisc.vampireEmbeds as vE
import cogs.vampire.vMisc.vampireViews as vV

from misc.utils import yamlUtils as yu
from misc.config import mainConfig as mc

# TODO: ! FIX THIS !


async def normalRoller(interaction, self, targetcharacter):
    try:
        with sqlite3.connect(f'cogs//vampire//characters//{str(interaction.user.id)}//{targetcharacter}//{targetcharacter}.sqlite') as db:
            cursor = db.cursor()
            roll_pool = int(cursor.execute('SELECT rollPool FROM commandVars').fetchone()[0])
            difficulty = int(cursor.execute('SELECT difficulty from commandVars').fetchone()[0])
            hunger = int(cursor.execute('SELECT hunger from charInfo').fetchone()[0])
    except sqlite3.Error as e:
        log.error(f'*> normalRoller_1 | SQLITE3 ERROR | {e}')

    result: dict = {'regular_crit': 0, 'hunger_crit': 0, 'regular_success': 0, 'hunger_success': 0, 'regular_fail': 0,
                    'hunger_fail' : 0, 'hunger_skull': 0}
    while_pool = roll_pool
    while 0 < while_pool:
        die_result = randint(1, 10)

        if hunger <= 0:

            if die_result == 10:
                result['regular_crit'] += 1
            elif die_result >= 6:
                result['regular_success'] += 1
            elif die_result <= 5:
                result['regular_fail'] += 1

        else:
            hunger -= 1

            if die_result == 10:
                result['hunger_crit'] += 1
            elif die_result == 1:
                result['hunger_skull'] += 1
            elif die_result >= 6:
                result['hunger_success'] += 1
            elif die_result <= 5:
                result['hunger_fail'] += 1

        while_pool -= 1
    try:
        with sqlite3.connect(f'cogs//vampire//characters//{str(interaction.user.id)}//{targetcharacter}//{targetcharacter}.sqlite') as db:
            cursor = db.cursor()
            cursor.execute(
                'UPDATE rerollInfo SET regularCritDie=?, hungerCritDie=?, regularSuccess=?, hungerSuccess=?, regularFail=?, hungerFail=?, hungerSkull=?',
                (result['regular_crit'], result['hunger_crit'], result['regular_success'], result['hunger_success'],
                 result['regular_fail'], result['hunger_fail'], result['hunger_skull']))
            db.commit()
    except sqlite3.Error as e:
        log.error(f'normalRoller_2 | SQLITE3 ERROR | {e}')

    crits = 0
    flag = ''
    while_total = result['regular_crit'] + result['hunger_crit']
    while while_total > 0:
        if result['regular_crit'] + result['hunger_crit'] > 2:
            if result['regular_crit'] >= 2:
                crits += 4
                result['regular_crit'] -= 2

            elif result['hunger_crit'] >= 2:
                crits += 4
                flag = 'Messy Crit'
                result['hunger_crit'] -= 2

            elif result['regular_crit'] + result['hunger_crit'] >= 2:
                crits += 4
                flag = 'Messy Crit'
                break
        else:
            break
        while_total -= 1

    crits += result['hunger_crit'] + result['regular_crit']
    total_successes = int(result['regular_success'] + result['hunger_success'] + crits)

    roll_embed = discord.Embed(title='ERROR', description=f'ERROR', color=mc.embed_colors["red"])
    if total_successes < int(difficulty):
        if int(result['hunger_skull']) > 0:
            flag = 'Bestial Failure'
            roll_embed = discord.Embed(title='Roll Results', description=f'`{targetcharacter}` - `{interaction.user}`',
                                       color=mc.embed_colors["black"])
        else:
            flag = 'Fail'
            roll_embed = discord.Embed(title='Roll Results', description=f'`{targetcharacter}` - `{interaction.user}`',
                                       color=mc.embed_colors["red"])
    elif total_successes >= int(difficulty) and flag != 'Messy Crit':
        flag = 'Success'
        roll_embed = discord.Embed(title='Roll Results', description=f'`{targetcharacter}` - `{interaction.user}`',
                                   color=mc.embed_colors["green"])

    try:
        with sqlite3.connect(f'cogs//vampire//characters//{str(interaction.user.id)}//{targetcharacter}//{targetcharacter}.sqlite') as db:
            cursor = db.cursor()
            roll_comp = cursor.execute('SELECT poolComp from commandVars').fetchone()[0]
            url = cursor.execute('SELECT imgURL from charInfo').fetchone()[0]

            roll_embed.add_field(name='Roll Pool:', value=f'{roll_pool}')
            roll_embed.add_field(name='Difficulty:', value=f'{difficulty}')
            roll_embed.add_field(name='Roll Composition:', value=f'{roll_comp}')
            roll_embed.add_field(name='Roll Result:', value=f'{total_successes} | {flag}')
            roll_embed.set_thumbnail(url=f'{url}')
    except sqlite3.Error as e:
        log.error(f'normalRoller_3 | SQLITE3 ERROR | {e}')

    await interaction.response.edit_message(embed=roll_embed, view=vV.StandardRerollView(self.CLIENT))


async def reRoller(interaction, self, targetcharacter, button):
    try:
        with sqlite3.connect(f'cogs//vampire//characters//{str(interaction.user.id)}//{targetcharacter}//{targetcharacter}.sqlite') as db:
            cursor = db.cursor()
            roll_pool = int(cursor.execute('SELECT rollPool FROM commandVars').fetchone()[0])
            difficulty = int(cursor.execute('SELECT difficulty from commandVars').fetchone()[0])
            wp_base = cursor.execute('SELECT willpowerBase FROM willpower').fetchone()[0]
            wp_SUP = cursor.execute('SELECT willpowerSUP FROM willpower').fetchone()[0]
            wp_AGG = cursor.execute('SELECT willpowerAGG FROM willpower').fetchone()[0]
            hunger_crit = cursor.execute('SELECT hungerCritDie FROM rerollInfo').fetchone()[0]
            regular_crit = cursor.execute('SELECT regularCritDie FROM rerollInfo').fetchone()[0]
            regular_success = cursor.execute('SELECT regularSuccess FROM rerollInfo').fetchone()[0]
            hunger_success = cursor.execute('SELECT hungerCritDie FROM rerollInfo').fetchone()[0]
            regular_fail = cursor.execute('SELECT regularFail FROM rerollInfo').fetchone()[0]
            hunger_skulls = cursor.execute('SELECT hungerSkull FROM rerollInfo').fetchone()[0]
    except sqlite3.Error as e:
        log.error(f'reRoller_1 | SQLITE3 ERROR | {e}')

    roll_results: dict = {'regular_crit'  : regular_crit, 'hunger_crit': hunger_crit, 'regular_success': regular_success,
                          'hunger_success': hunger_success, 'regular_fail': regular_fail, 'hunger_skull': hunger_skulls}

    if roll_results['regular_fail'] >= 3:
        rerolls = 3
        roll_results['regular_fail'] -= 3
    else:
        rerolls = roll_results['regular_fail']
        roll_results['regular_fail'] -= roll_results['regular_fail']

    while 0 < rerolls:
        die_result = randint(1, 10)

        if die_result == 10:
            roll_results['regular_crit'] += 1
        elif die_result >= 6:
            roll_results['regular_success'] += 1
        elif die_result <= 5:
            roll_results['regular_fail'] += 1

        rerolls -= 1

    try:
        with sqlite3.connect(f'cogs//vampire//characters//{str(interaction.user.id)}//{targetcharacter}//{targetcharacter}.sqlite') as db:
            cursor = db.cursor()
            cursor.execute('UPDATE rerollInfo SET regularCritDie=?, regularSuccess=?, regularFail=?',
                           (roll_results['regular_crit'], roll_results['regular_success'], roll_results['regular_fail']))
            db.commit()
    except sqlite3.Error as e:
        log.error(f'reRoller_2 | SQLITE3 ERROR | {e}')

    crits = 0
    flag = ''
    while_total = roll_results['regular_crit'] + roll_results['hunger_crit']
    while while_total > 0:
        if roll_results['regular_crit'] + roll_results['hunger_crit'] > 2:
            if roll_results['regular_crit'] >= 2:
                crits += 4
                roll_results['regular_crit'] -= 2

            elif roll_results['hunger_crit'] >= 2:
                crits += 4
                flag = 'Messy Crit'
                roll_results['hunger_crit'] -= 2

            elif roll_results['regular_crit'] + roll_results['hunger_crit'] >= 2:
                crits += 4
                flag = 'Messy Crit'
                break
        else:
            break
        while_total -= 1

    crits += roll_results['hunger_crit'] + roll_results['regular_crit']
    total_successes = int(roll_results['regular_success'] + roll_results['hunger_success'] + crits)

    reroll_embed = discord.Embed(title='ERROR', description=f'ERROR', color=mc.embed_colors["red"])
    if total_successes < int(difficulty):
        if int(roll_results['hunger_skull']) > 0:
            flag = 'Bestial Failure'
            reroll_embed = discord.Embed(title='Roll Results', description=f'`{targetcharacter}` - `{interaction.user}`',
                                         color=mc.embed_colors["black"])
        else:
            flag = 'Fail'
            reroll_embed = discord.Embed(title='Roll Results', description=f'`{targetcharacter}` - `{interaction.user}`',
                                         color=mc.embed_colors["red"])
    elif total_successes >= int(difficulty) and flag != 'Messy Crit':
        flag = 'Success'
        reroll_embed = discord.Embed(title='Roll Results', description=f'`{targetcharacter}` - `{interaction.user}`',
                                     color=mc.embed_colors["green"])

    if wp_base <= wp_AGG:
        button.disabled = True
        button.label = 'Fate Sealed'
        await interaction.response.edit_message(view=self)
        await interaction.followup.send(embed=vE.not_enough_wp_embed, ephemeral=True)
        return
    elif wp_base <= wp_SUP:
        db.cursor().execute('UPDATE willpower SET willpowerAGG=?', (str(wp_AGG + 1),))
    else:
        db.cursor().execute('UPDATE willpower SET willpowerSUP=?', (str(wp_SUP + 1),))
    db.commit()

    try:
        with sqlite3.connect(f'cogs//vampire//characters//{str(interaction.user.id)}//{targetcharacter}//{targetcharacter}.sqlite') as db:
            cursor = db.cursor()
            roll_comp = cursor.execute('SELECT poolComp from commandVars').fetchone()[0]
            url = cursor.execute('SELECT imgURL from charInfo').fetchone()[0]

            reroll_embed.add_field(name='Roll Pool:', value=f'{roll_pool}')
            reroll_embed.add_field(name='Difficulty:', value=f'{difficulty}')
            reroll_embed.add_field(name='Roll Composition:', value=f'{roll_comp}')
            reroll_embed.add_field(name='Roll Result:', value=f'{total_successes} | {flag}')
            wp_SUP_new = cursor.execute('SELECT willpowerSUP FROM willpower').fetchone()[0]
            wp_AGG_new = cursor.execute('SELECT willpowerAGG FROM willpower').fetchone()[0]
            wp_subtract = wp_SUP_new + wp_AGG_new
            wp_untouched = wp_base - wp_subtract
            if wp_untouched < 0:
                wp_untouched = 0
            reroll_embed.add_field(name='Untouched, Superficial, and Aggravated Willpower:',
                                   value=f'{wp_untouched}, {wp_SUP_new}, {wp_AGG_new}')
            reroll_embed.set_thumbnail(url=f'{url}')
    except sqlite3.Error as e:
        log.error(f'reRoller_3 | SQLITE3 ERROR | {e}')

    button.disabled = True
    button.label = 'Fate Tempted'
    await interaction.response.edit_message(embed=reroll_embed, view=self)


async def simpleSelection(interaction, select, self, targetDB, func_callback):
    targetcharacter = await ownerChecker(interaction)
    if targetcharacter is str:
        pass
    elif targetcharacter is False:
        return

    try:
        with sqlite3.connect(f'cogs//vampire//characters//{str(interaction.user.id)}//{targetcharacter}//{targetcharacter}.sqlite') as db:
            cursor = db.cursor()
            for_var = 0

            roll_pool = int(cursor.execute('SELECT rollPool FROM commandvars').fetchone()[0])
            roll_comp = cursor.execute('SELECT poolComp from commandVars').fetchone()[0]

            for x in select.values:
                skill_value_grab = cursor.execute(f'SELECT {select.values[for_var]} FROM {targetDB}')
                skill_value = skill_value_grab.fetchone()[0]
                roll_pool += skill_value
                roll_comp = f'{roll_comp} + {select.values[for_var]}[{skill_value}]'
                db.commit()
                for_var += 1

            cursor.execute('UPDATE commandvars SET poolComp=?', (roll_comp,))
            cursor.execute('UPDATE commandvars SET rollPool=?', (roll_pool,))
            db.commit()

            await selectionEmbedSetter(interaction, targetcharacter)

            select.disabled = True
            await interaction.response.edit_message(embed=vE.selection_embed, view=self)
    except sqlite3.Error as e:
        log.error(f'{func_callback} | SQLITE3 ERROR | {e}')


async def rouseCheck(interaction, targetcharacter) -> str:
    try:
        with sqlite3.connect(f'cogs//vampire//characters//{str(interaction.user.id)}//{targetcharacter}//{targetcharacter}.sqlite') as db:
            cursor = db.cursor()
            hunger = int(cursor.execute('SELECT hunger from charInfo').fetchone()[0])
            rouse_num_result: int = randint(1, 10)

            if hunger >= 5:
                if rouse_num_result <= 5:
                    return 'Frenzy'  # * Hunger Frenzy, No Hunger Gain Too High Already
                return 'Hungry'

            elif rouse_num_result >= 6:
                return 'Pass'  # * No Hunger Gain

            elif rouse_num_result <= 5:
                cursor.execute('UPDATE charInfo SET hunger=?', (str(int(hunger + 1))))
                db.commit()
                return 'Fail'  # * Hunger Gain
    except sqlite3.Error as e:
        log.error(f'rouseCheck | SQLITE3 ERROR | {e}')


async def selectionEmbedSetter(interaction, targetcharacter) -> None:
    try:
        with sqlite3.connect(f'cogs//vampire//characters//{str(interaction.user.id)}//{targetcharacter}//{targetcharacter}.sqlite') as db:
            cursor = db.cursor()
            roll_pool = int(cursor.execute('SELECT rollPool FROM commandVars').fetchone()[0])
            difficulty = int(cursor.execute('SELECT difficulty from commandVars').fetchone()[0])
            roll_comp = cursor.execute('SELECT poolComp from commandVars').fetchone()[0]
            character_avatar = cursor.execute('SELECT imgURL from charInfo').fetchone()[0]

            vE.selection_embed.set_field_at(index=0, name='Character Name',value=f'{targetcharacter}', inline=False)
            vE.selection_embed.set_field_at(index=1, name='Roll Information', value='', inline=False)
            vE.selection_embed.set_field_at(index=2, name='Roll Pool:', value=f'{roll_pool}')
            vE.selection_embed.set_field_at(index=3, name='Difficulty:', value=f'{difficulty}')
            vE.selection_embed.set_field_at(index=4, name='Roll Composition:', value=f'{roll_comp}')

            user_info = {'user_name'  : interaction.user,
                         'user_id'    : interaction.user.id,
                         'user_avatar': interaction.user.display_avatar}

            vE.selection_embed.set_thumbnail(url=character_avatar)
            vE.selection_embed.set_footer(text=f'{user_info["user_id"]}', icon_url=f'{user_info["user_avatar"]}')
            vE.selection_embed.set_author(name=f'{user_info["user_name"]}', icon_url=f'{user_info["user_avatar"]}')
    except sqlite3.Error as e:
        log.error(f'selectionEmbedSetter | SQLITE3 ERROR | {e}')


async def rollInitialize(interaction, charactername) -> bool:
    # ! Runs every time someone uses the /vroll command
    targetDB = f'cogs//vampire//characters//{str(interaction.user.id)}//{charactername}//{charactername}.sqlite'

    log.debug(f'> Checking if [ `{targetDB}` ] exists')
    if not path.exists(targetDB):
        log.warn(f'*> Database [ `{targetDB}` ] does not exist')
        await interaction.response.send_message(embed=discord.Embed(
            title='Database Error', color=mc.embed_colors["red"],
            description=f'[ `{charactername}` ] Does Not Exist, Preventing Roll. \n\n {mc.ISSUE_CONTACT}'), ephemeral=True)
        return False
    else:
        log.debug(f'> Successful Connection to [ `{targetDB}` ]')

    try:
        with sqlite3.connect(targetDB) as db:
            cursor = db.cursor()
            char_owner_id = cursor.execute('SELECT userID FROM ownerInfo').fetchone()[0]
            if char_owner_id != interaction.user.id:  # ? If interaction user doesn't own the character
                await interaction.response.send_message(f'You don\'t own {charactername}', ephemeral=True)
                return False

            # ? Resets commandvars & reroll_info
            cursor.execute(
                'UPDATE commandvars SET difficulty=?, rollPool=?, result=?, poolComp=?',
                (0, 0, 0, 'Base[0]'), )
            cursor.execute(
                'UPDATE rerollInfo SET regularCritDie=?, hungerCritDie=?, regularSuccess=?, '
                'hungerSuccess=?, regularFail=?, hungerFail=?, hungerSkull=?',
                (0, 0, 0, 0, 0, 0, 0), )

            url = cursor.execute('SELECT imgURL from charInfo').fetchone()[0]
            vE.selection_embed.set_thumbnail(url=f'{url}')

            db.commit()

            targetCache = f'cogs/vampire/characters/{str(interaction.user.id)}/{str(interaction.user.id)}.yaml'
            await yu.cacheClear(targetCache)
            await yu.cacheWrite(targetCache, dataInput={'characterName': f'{charactername}'})
            return True
    except sqlite3.Error as e:
        log.error(f'rollInitialize | SQLITE3 ERROR | {e}')


async def ownerChecker(interaction: discord.Interaction):
    # ! Runs basically any time someone does anything related to the vtm roller
    # ? Standard Usage:
    """
    targetcharacter = await ownerChecker(interaction)
    if targetcharacter is str:
            pass
    elif targetcharacter is False:
        return
    pass # ! Real Code Here
    """

    targetCache = f'cogs/vampire/characters/{str(interaction.user.id)}/{str(interaction.user.id)}.yaml'
    use_data: dict = {}
    use_data.update(await yu.cacheRead(f'{targetCache}'))
    targetcharacter: str = str(use_data['characterName'])

    try:
        with sqlite3.connect(f'cogs//vampire//characters//{str(interaction.user.id)}//{targetcharacter}//{targetcharacter}.sqlite') as db:
            char_owner_id = db.cursor().execute('SELECT userID FROM ownerInfo').fetchone()[0]

            if char_owner_id != interaction.user.id:  # ! User does __NOT__ own the Character
                await interaction.response.send_message(f'> You don\'t own any characters named: `{targetcharacter}`.\n\n'
                                                        f'Please double check the name input and try again, otherwise please contact\n'
                                                        f'* Bot\'s Current Runner:`{mc.RUNNER}`\n'
                                                        f'* Bot\'s Current Developer: `{mc.DEVELOPER}`')
                return False
            elif char_owner_id == interaction.user.id:  # ! User __DOES__ own the Character
                return targetcharacter
    except sqlite3.Error as e:
        log.error(f'ownerChecker | SQLITE3 ERROR | {e}')
