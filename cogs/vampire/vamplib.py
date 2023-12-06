import discord
from discord.ui import View
from zenlog import log

import sqlite3
from random import randint
import os

from misc.utils import yaml_utils as yu
from misc.config import main_config as mc

selection_embed = discord.Embed(title='', description=f'', color=mc.embed_colors["purple"])
selection_embed.add_field(name='Roll Information', value='', inline=False)
selection_embed.add_field(name='Roll Pool:', value=f'')
selection_embed.add_field(name='Difficulty:', value=f'')
selection_embed.add_field(name='Roll Composition:', value=f'')

roll_details_embed = discord.Embed(title='Extra Details:', description=f'{mc.ISSUE_CONTACT}', color=mc.embed_colors["black"])
not_enough_wp_embed = discord.Embed(title='Willpower Reroll',
                                    description=f'You don\'t have enough willpower. \n\n {mc.ISSUE_CONTACT}',
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
attribute_options = [
            discord.SelectOption(
                label='Strength', value='strength',
                emoji='<:gem_red:813815883754766356>',
            ),
            discord.SelectOption(
                label='Dexterity', value='dexterity',
                emoji='<:gem_red:813815883754766356>',
            ),
            discord.SelectOption(
                label='Stamina', value='stamina',
                emoji='<:gem_red:813815883754766356>',
            ),
            discord.SelectOption(
                label='Charisma', value='charisma',
                emoji='<:greenessential:885489197169926195>',
            ),
            discord.SelectOption(
                label='Manipulation', value='manipulation',
                emoji='<:greenessential:885489197169926195>',
            ),
            discord.SelectOption(
                label='Composure', value='composure',
                emoji='<:greenessential:885489197169926195>',
            ),
            discord.SelectOption(
                label='Intelligence', value='intelligence',
                emoji='<:blueprint:1053308562127994991>',
            ),
            discord.SelectOption(
                label='Wits', value='wits',
                emoji='<:blueprint:1053308562127994991>',
            ),
            discord.SelectOption(
                label='Resolve', value='resolve',
                emoji='<:blueprint:1053308562127994991>',
            )]
physical_skill_options = [
    discord.SelectOption(
        label='Athletics', value='athletics', emoji='<:gem_red:813815883754766356>'
    ),
    discord.SelectOption(
        label='Brawl', value='brawl', emoji='<:gem_red:813815883754766356>'
    ),
    discord.SelectOption(
        label='Craft', value='craft', emoji='<:gem_red:813815883754766356>'
    ),
    discord.SelectOption(
        label='Drive', value='drive', emoji='<:gem_red:813815883754766356>'
    ),
    discord.SelectOption(
        label='Firearms', value='firearms', emoji='<:gem_red:813815883754766356>'
    ),
    discord.SelectOption(
        label='Larceny', value='larceny', emoji='<:gem_red:813815883754766356>'
    ),
    discord.SelectOption(
        label='Melee', value='melee', emoji='<:gem_red:813815883754766356>'
    ),
    discord.SelectOption(
        label='Stealth', value='stealth', emoji='<:gem_red:813815883754766356>'
    ),
    discord.SelectOption(
        label='Survival', value='survival', emoji='<:gem_red:813815883754766356>'
    ), ]
social_skill_options = [
    discord.SelectOption(
        label='Animal Ken', value='animal_ken', emoji='<:greenessential:885489197169926195>'
    ),
    discord.SelectOption(
        label='Etiquette', value='etiquette', emoji='<:greenessential:885489197169926195>'
    ),
    discord.SelectOption(
        label='Insight', value='insight', emoji='<:greenessential:885489197169926195>'
    ),
    discord.SelectOption(
        label='Intimidation', value='intimidation', emoji='<:greenessential:885489197169926195>'
    ),
    discord.SelectOption(
        label='Leadership', value='leadership', emoji='<:greenessential:885489197169926195>'
    ),
    discord.SelectOption(
        label='Performance', value='performance', emoji='<:greenessential:885489197169926195>'
    ),
    discord.SelectOption(
        label='Persuasion', value='persuasion', emoji='<:greenessential:885489197169926195>'
    ),
    discord.SelectOption(
        label='Streetwise', value='streetwise', emoji='<:greenessential:885489197169926195>'
    ),
    discord.SelectOption(
        label='Subterfuge', value='subterfuge', emoji='<:greenessential:885489197169926195>'
    ), ]
mental_skill_options = [
    discord.SelectOption(
        label='Academics', value='academics', emoji='<:blueprint:1053308562127994991>'
    ),
    discord.SelectOption(
        label='Awareness', value='awareness', emoji='<:blueprint:1053308562127994991>'
    ),
    discord.SelectOption(
        label='Finance', value='finance', emoji='<:blueprint:1053308562127994991>'
    ),
    discord.SelectOption(
        label='Investigation', value='investigation', emoji='<:blueprint:1053308562127994991>'
    ),
    discord.SelectOption(
        label='Medicine', value='medicine', emoji='<:blueprint:1053308562127994991>'
    ),
    discord.SelectOption(
        label='Occult', value='occult', emoji='<:blueprint:1053308562127994991>'
    ),
    discord.SelectOption(
        label='Politics', value='politics', emoji='<:blueprint:1053308562127994991>'
    ),
    discord.SelectOption(
        label='Science', value='science', emoji='<:blueprint:1053308562127994991>'
    ),
    discord.SelectOption(
        label='Technology', value='technology', emoji='<:blueprint:1053308562127994991>'
    ), ]
discipline_options = [
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
extra_options = [
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


async def normalRoller(interaction, self, targetcharacter):
    try:
        with sqlite3.connect(f'cogs//vampire//characters//{str(interaction.user.id)}//{targetcharacter}.sqlite') as db:
            cursor = db.cursor()
            roll_pool = int(cursor.execute('SELECT rollPool FROM commandVars').fetchone()[0])
            difficulty = int(cursor.execute('SELECT difficulty from commandVars').fetchone()[0])
            hunger = int(cursor.execute('SELECT hunger from charInfo').fetchone()[0])
    except sqlite3.Error as e:
        log.error(f'normalRoller_1 | SQLITE3 ERROR | {e}')

    result: dict = {'regular_crit': 0, 'hunger_crit': 0, 'regular_success': 0, 'hunger_success': 0, 'regular_fail': 0, 'hunger_fail': 0, 'hunger_skull': 0}
    while_pool = roll_pool
    while 0 < while_pool:
        die_result = randint(1, 10)

        if hunger <= 0:

            if die_result == 10:
                result['regular_crit'] += 1
            elif die_result >= 6:
                result['regular_success'] += 1
            elif die_result <= 5 :
                result['regular_fail'] += 1

        else:
            hunger -= 1

            if die_result == 10:
                result['hunger_crit'] += 1
            elif die_result == 1:
                result['hunger_skull'] += 1
            elif die_result >= 6:
                result['hunger_success'] += 1
            elif die_result <= 5 :
                result['hunger_fail'] += 1

        while_pool -= 1
    try:
        with sqlite3.connect(f'cogs//vampire//characters//{str(interaction.user.id)}//{targetcharacter}.sqlite') as db:
            cursor = db.cursor()
            cursor.execute('UPDATE rerollInfo SET regularCritDie=?, hungerCritDie=?, regularSuccess=?, hungerSuccess=?, regularFail=?, hungerFail=?, hungerSkull=?', (result['regular_crit'], result['hunger_crit'], result['regular_success'], result['hunger_success'], result['regular_fail'], result['hunger_fail'], result['hunger_skull']))
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
            roll_embed = discord.Embed(title='Roll Results', description=f'`{targetcharacter}` - `{interaction.user}`', color=mc.embed_colors["black"])
        else:
            flag = 'Fail'
            roll_embed = discord.Embed(title='Roll Results', description=f'`{targetcharacter}` - `{interaction.user}`', color=mc.embed_colors["red"])
    elif total_successes >= int(difficulty) and flag != 'Messy Crit':
        flag = 'Success'
        roll_embed = discord.Embed(title='Roll Results', description=f'`{targetcharacter}` - `{interaction.user}`', color=mc.embed_colors["green"])

    try:
        with sqlite3.connect(f'cogs//vampire//characters//{str(interaction.user.id)}//{targetcharacter}.sqlite') as db:
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

    await interaction.response.edit_message(embed=roll_embed, view=StandardRerollView(self.CLIENT))


async def reRoller(interaction, self, targetcharacter):
    try:
        with sqlite3.connect(f'cogs//vampire//characters//{str(interaction.user.id)}//{targetcharacter}.sqlite') as db:
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

    roll_results: dict = {'regular_crit': regular_crit, 'hunger_crit': hunger_crit, 'regular_success': regular_success, 'hunger_success': hunger_success, 'regular_fail': regular_fail, 'hunger_skull': hunger_skulls}

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
        with sqlite3.connect(f'cogs//vampire//characters//{str(interaction.user.id)}//{targetcharacter}.sqlite') as db:
            cursor = db.cursor()
            cursor.execute('UPDATE rerollInfo SET regularCritDie=?, regularSuccess=?, regularFail=?', (roll_results['regular_crit'], roll_results['regular_success'], roll_results['regular_fail']))
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
        await interaction.response.send_message(embed=not_enough_wp_embed, view=None, ephemeral=True)
        return
    elif wp_base <= wp_SUP:
        db.cursor().execute('UPDATE willpower SET willpowerAGG=?', (str(wp_AGG + 1),))
    else:
        db.cursor().execute('UPDATE willpower SET willpowerSUP=?', (str(wp_SUP + 1),))
    db.commit()

    try:
        with sqlite3.connect(f'cogs//vampire//characters//{str(interaction.user.id)}//{targetcharacter}.sqlite') as db:
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
            reroll_embed.add_field(name='Untouched, Superficial, and Aggravated Willpower:', value=f'{wp_untouched}, {wp_SUP_new}, {wp_AGG_new}')
            reroll_embed.set_thumbnail(url=f'{url}')
    except sqlite3.Error as e:
        log.error(f'reRoller_3 | SQLITE3 ERROR | {e}')

    await interaction.response.edit_message(embed=reroll_embed)


async def simpleSelection(interaction, select, self, targetDB, func_callback):
    targetcharacter = await ownerChecker(interaction)
    if targetcharacter is str:
        pass
    elif targetcharacter is False:
        return

    try:
        with sqlite3.connect(f'cogs//vampire//characters//{str(interaction.user.id)}//{targetcharacter}.sqlite') as db:
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
            await interaction.response.edit_message(embed=selection_embed, view=self)
    except sqlite3.Error as e:
        log.error(f'{func_callback} | SQLITE3 ERROR | {e}')


async def rouseCheck(interaction, targetcharacter) -> str:
    try:
        with sqlite3.connect(f'cogs//vampire//characters//{str(interaction.user.id)}//{targetcharacter}.sqlite') as db:
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
        with sqlite3.connect(f'cogs//vampire//characters//{str(interaction.user.id)}//{targetcharacter}.sqlite') as db:
            cursor = db.cursor()
            roll_pool = int(cursor.execute('SELECT rollPool FROM commandVars').fetchone()[0])
            difficulty = int(cursor.execute('SELECT difficulty from commandVars').fetchone()[0])
            roll_comp = cursor.execute('SELECT poolComp from commandVars').fetchone()[0]
            url = cursor.execute('SELECT imgURL from charInfo').fetchone()[0]

            selection_embed.set_field_at(index=0, name=f'Roll Information', value=f'`{targetcharacter}` - `{interaction.user}`', inline=False)
            selection_embed.set_field_at(index=1, name='Roll Pool:', value=f'{roll_pool}')
            selection_embed.set_field_at(index=2, name='Difficulty:', value=f'{difficulty}')
            selection_embed.set_field_at(index=3, name='Roll Composition:', value=f'{roll_comp}')
            selection_embed.set_thumbnail(url=f'{url}')
    except sqlite3.Error as e:
        log.error(f'selectionEmbedSetter | SQLITE3 ERROR | {e}')


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
            selection_embed.set_thumbnail(url=f'{url}')

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
        with sqlite3.connect(f'cogs//vampire//characters//{str(interaction.user.id)}//{targetcharacter}.sqlite') as db:
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

        await interaction.response.edit_message(embed=selection_embed, view=StandardSelectionView(self.CLIENT))

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

        try:
            with sqlite3.connect(f'cogs//vampire//characters//{str(interaction.user.id)}//{targetcharacter}.sqlite') as db:
                cursor = db.cursor()

                bp = int(cursor.execute('SELECT blood_potency FROM charInfo').fetchone()[0])
                bp_mapping = {1: 2, 2: 2, 3: 3, 4: 3, 5: 4, 6: 5}
                bp_add = bp_mapping[bp]

                new_roll_pool = int(cursor.execute('SELECT rollPool FROM commandvars').fetchone()[0] + bp_add)
                cursor.execute('UPDATE commandvars SET rollPool=?', (new_roll_pool,))
                cursor.execute('UPDATE commandvars SET poolComp=?', (f"Blood Surge[{bp_add}]",))
                db.commit()

                await selectionEmbedSetter(interaction, targetcharacter)

                button.disabled = True
                button.style = discord.ButtonStyle.gray
                await interaction.response.edit_message(embed=selection_embed, view=self)
        except sqlite3.Error as e:
            log.error(f'blood_surge_button_callback | SQLITE3 ERROR | {e}')

    @discord.ui.select(placeholder='Select Difficulty', options=difficulty_options, max_values=1, min_values=1)
    async def difficulty_select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        targetcharacter = await ownerChecker(interaction)
        if targetcharacter is str:
            pass
        elif targetcharacter is False:
            return
        try:
            with sqlite3.connect(f'cogs//vampire//characters//{str(interaction.user.id)}//{targetcharacter}.sqlite') as db:
                db.cursor().execute('UPDATE commandvars SET difficulty=?', (select.values))  # ! Parentheses are NOT redundant
                db.commit()

                await selectionEmbedSetter(interaction, targetcharacter)

                await interaction.response.edit_message(embed=selection_embed, view=self)
        except sqlite3.Error as e:
            log.error(f'difficulty_select_callback | SQLITE3 ERROR | {e}')


class StandardSelectionView(View):
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

        await interaction.response.edit_message(embed=selection_embed, view=StandardDisciplineSelectionView(self.CLIENT))

    @discord.ui.select(placeholder='Select Attributes', min_values=1, max_values=3, options=attribute_options)
    async def attribute_select_callback(self, interaction, select: discord.ui.Select):
        await simpleSelection(interaction, select, self, 'charAttributes', 'attribute_select_callback')

    @discord.ui.select(placeholder='Select Physical Skills', min_values=1, max_values=3, options=physical_skill_options)
    async def physical_skill_select_callback(self, interaction, select: discord.ui.Select):
        await simpleSelection(interaction, select, self, 'physicalSkills', 'physical_skill_select_callback')

    @discord.ui.select(placeholder='Select Social Skills', min_values=1, max_values=3, options=social_skill_options)
    async def social_skill_select_callback(self, interaction, select: discord.ui.Select):
        await simpleSelection(interaction, select, self, 'socialSkills', 'social_skill_select_callback')

    @discord.ui.select(placeholder='Select Mental Skills', min_values=1, max_values=3, options=mental_skill_options)
    async def mental_skill_select_callback(self, interaction, select: discord.ui.Select):
        await simpleSelection(interaction, select, self, 'mentalSkills', 'mental_skill_select_callback')


class StandardDisciplineSelectionView(View):
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

        await interaction.response.edit_message(embed=selection_embed, view=StandardExtraSelectionView(self.CLIENT))

    @discord.ui.select(placeholder='Select Discipline', min_values=1, options=discipline_options)
    async def discipline_select_callback(self, interaction, select: discord.ui.Select):
        await simpleSelection(interaction, select, self, 'disciplines', 'discipline_select_callback')


class StandardExtraSelectionView(View):
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

        await interaction.response.edit_message(embed=selection_embed, view=StandardRollView(self.CLIENT))

    @discord.ui.select(placeholder='Select Extra', min_values=1, options=extra_options)
    async def extra_select_callback(self, interaction, select: discord.ui.Select):
        targetcharacter = await ownerChecker(interaction)
        if targetcharacter is str:
            pass
        elif targetcharacter is False:
            return

        try:
            with sqlite3.connect(f'cogs//vampire//characters//{str(interaction.user.id)}//{targetcharacter}.sqlite') as db:
                cursor = db.cursor()

                roll_pool = int(cursor.execute('SELECT rollPool FROM commandvars').fetchone()[0])
                roll_comp = cursor.execute('SELECT poolComp from commandVars').fetchone()[0]

                extra_value = select.values[0]
                roll_pool += int(extra_value)
                roll_comp = f'{roll_comp} + Extra[{extra_value}]'

                cursor.execute('UPDATE commandvars SET poolComp=?', (roll_comp,))
                cursor.execute('UPDATE commandvars SET rollPool=?', (roll_pool,))
                db.commit()

                await selectionEmbedSetter(interaction, targetcharacter)

                select.disabled = True
                await interaction.response.edit_message(embed=selection_embed, view=self)
        except sqlite3.Error as e:
            log.error(f'extra_select_callback | SQLITE3 ERROR | {e}')


class StandardRollView(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Roll', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.green, row=1)
    async def roll_button_callback(self, interaction, button):
        targetcharacter = await ownerChecker(interaction)
        if targetcharacter is str:
            pass
        elif targetcharacter is False:
            return

        await normalRoller(interaction, self, targetcharacter)


class StandardRerollView(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Reroll', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.red, row=1)
    async def roll_button_callback(self, interaction, button):
        targetcharacter = await ownerChecker(interaction)
        if targetcharacter is str:
            pass
        elif targetcharacter is False:
            return

        await reRoller(interaction, self, targetcharacter)
