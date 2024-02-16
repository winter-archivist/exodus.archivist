import discord
import sqlite3
import datetime
from zenlog import log
from random import randint
from discord.ui import View

import cogs.vtm_toolbox.vtb_misc.vtbPageSystem as vPS
import cogs.vtm_toolbox.vtb_misc.vtbUtils as vU

import cogs.vtm_toolbox.vtb_roller.rollerPageBuilders as rPB
import cogs.vtm_toolbox.vtb_roller.rollerOptions as rO

from misc.config import mainConfig as mC
from misc.utils import yamlUtils as yU


async def basicSelection(select, targetDB, targetTable):
    with sqlite3.connect(targetDB) as db:
        cursor = db.cursor()

        roll_pool = cursor.execute('SELECT rollPool FROM commandvars').fetchone()[0]
        roll_comp = cursor.execute('SELECT poolComp from commandVars').fetchone()[0]

        for_var = 0
        for x in select.values:
            skill_value_grab = cursor.execute(f'SELECT {select.values[for_var]} FROM {targetTable}')
            skill_value = skill_value_grab.fetchone()[0]
            roll_pool += skill_value
            roll_comp = f'{roll_comp} + {select.values[for_var]}[{skill_value}]'
            db.commit()
            for_var += 1

        cursor.execute('UPDATE commandvars SET poolComp=?', (roll_comp,))
        cursor.execute('UPDATE commandvars SET rollPool=?', (roll_pool,))
        db.commit()

    select.disabled = True


async def clearDBRollInfo(interaction):
    character_name = await vU.getCharacterName(interaction)

    # This will be fixed in the future, I just want to get this small thing pushed out soon.
    # For more info, just look up "atrocious" in this file lower down.
    await yU.cacheClear(f'cogs//vampire//characters//{str(interaction.user.id)}//{character_name}//roll_mark.yaml')

    with sqlite3.connect(f'cogs//vampire//characters//{str(interaction.user.id)}//{character_name}//{character_name}.sqlite') as db:
        cursor = db.cursor()  # ? Resets commandvars & reroll_info
        cursor.execute('UPDATE commandvars SET difficulty=?, rollPool=?, result=?, poolComp=?', (0, 0, 0, 'Base[0]'), )
        cursor.execute('UPDATE rerollInfo SET regularCritDie=?, hungerCritDie=?, regularSuccess=?, hungerSuccess=?, regularFail=?, hungerFail=?, hungerSkull=?', (0, 0, 0, 0, 0, 0, 0), )
        db.commit()


async def normalRoller(interaction, return_page):

    character_name = await vU.getCharacterName(interaction)

    # Finding Starting Roll Pool, Difficulty, and Hunger before rolling die.
    try:
        with sqlite3.connect(f'cogs//vampire//characters//{str(interaction.user.id)}//{character_name}//{character_name}.sqlite') as db:
            cursor = db.cursor()
            roll_pool = int(cursor.execute('SELECT rollPool FROM commandVars').fetchone()[0])
            difficulty = int(cursor.execute('SELECT difficulty from commandVars').fetchone()[0])
            hunger = int(cursor.execute('SELECT hunger from charInfo').fetchone()[0])
    except sqlite3.Error as e:
        log.error(f'*> normalRoller_1 | SQLITE3 ERROR | {e}')

    result: dict = {'regular_crit': 0, 'hunger_crit': 0, 'regular_success': 0, 'hunger_success': 0, 'regular_fail': 0,
                    'hunger_fail' : 0, 'hunger_skull': 0}

    # Determines what Dice is what Number
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

    # Updating rerollInfo in the database
    try:
        with sqlite3.connect(f'cogs//vampire//characters//{str(interaction.user.id)}//{character_name}//{character_name}.sqlite') as db:
            cursor = db.cursor()
            cursor.execute(
                'UPDATE rerollInfo SET regularCritDie=?, hungerCritDie=?, regularSuccess=?, hungerSuccess=?, regularFail=?, hungerFail=?, hungerSkull=?',
                (result['regular_crit'], result['hunger_crit'], result['regular_success'], result['hunger_success'],
                 result['regular_fail'], result['hunger_fail'], result['hunger_skull']))
            db.commit()
    except sqlite3.Error as e:
        log.error(f'normalRoller_2 | SQLITE3 ERROR | {e}')

    # Finds Crits
    crits = 0
    flag = ''
    while_total = result['regular_crit'] + result['hunger_crit']
    while while_total > -1:
        if result['regular_crit'] + result['hunger_crit'] > 2:
            if result['regular_crit'] >= 2:
                crits += 4
                flag = 'Crit'
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

    if total_successes >= difficulty and flag == '':
        flag = 'Regular Success'
    elif total_successes <= difficulty and flag == '':
        flag = 'Regular Fail'

    # Assigns Information
    return_page.add_field(name='Roll Result:', value=f'{total_successes} | {flag}')
    log.crit(f'{total_successes=} | {crits=} | {difficulty=}')

    #
    # TODO: Add to ReRoller
    # atrocious [goto next result atrocious result]
    target_cache = f'cogs//vampire//characters//{str(interaction.user.id)}//{character_name}//roll_mark.yaml'
    data_check = await yU.cacheDataExist(target_cache, 'mark')
    if data_check is True:
        data = await yU.cacheRead(f'{target_cache}')
        use_data = {}
        use_data.update(data)
        roll_mark = str(use_data['mark'])
        if roll_mark == 'hunt':
            current_time = datetime.datetime.now()
            await yU.cacheWrite(f'cogs//vampire//characters//{str(interaction.user.id)}//{character_name}//hunt_history.yaml', {f'{current_time}': f'{flag}'})

            with sqlite3.connect(f'cogs//vampire//characters//{str(interaction.user.id)}//{character_name}//{character_name}.sqlite') as db:
                cursor = db.cursor()
                hunt_hunger = int(cursor.execute('SELECT hunger from charInfo').fetchone()[0])
                blood_potency = int(cursor.execute('SELECT blood_potency from charInfo').fetchone()[0])

            return_page.add_field(name='Roll Mark:', value=f'**Hunt**')

            if flag == 'Regular Fail':
                return_page.add_field(name='Hunt Failed.', value=f'Ask DM About Resulting Consequences')
                return  # return_page; MAY NEED THIS TO FIX

            min_hunger_without_kill = 1
            if blood_potency >= 5:
                min_hunger_without_kill = 2

            if hunt_hunger == 0:
                min_hunger_without_kill = 0
            elif int(hunt_hunger - 2) <= min_hunger_without_kill:
                hunt_hunger = min_hunger_without_kill
            else:
                hunt_hunger -= 2

            temperament_check = randint(1, 10)
            if temperament_check >= 6:
                random_temperament_num = randint(1, 10)
                random_resonance_num = randint(1, 10)

                phlegmatic_resonances = (1, 2, 3)
                melancholy_resonances = (4, 5, 6)
                choleric_resonances = (7, 8)
                sanguine_resonances = (9, 10)
                # Eventually this should be stored in the character's sheet.
                if random_temperament_num in phlegmatic_resonances:
                    resonance = 'Phlegmatic'
                elif random_temperament_num in melancholy_resonances:
                    resonance = 'Melancholy'
                elif random_temperament_num in choleric_resonances:
                    resonance = 'Choleric'
                elif random_temperament_num in sanguine_resonances:
                    resonance = 'Sanguine'
                else:
                    resonance = 'ERROR'

                negligible_resonances = (1, 2, 3, 4, 5)
                fleeting_resonances = (6, 7, 8)
                intense_or_acute_resonances = (9, 10)
                if random_temperament_num in intense_or_acute_resonances:
                    second_temperament_roll = randint(1, 10)
                    if second_temperament_roll >= 9:
                        temperament = 'Acute'
                    else:
                        temperament = 'Intense'

                elif random_temperament_num in fleeting_resonances: temperament = 'Fleeting'

                elif random_temperament_num in negligible_resonances: temperament = 'Negligible'

                else: temperament = 'ERROR'

                return_page.add_field(name=f'{temperament} {resonance} Temperament', value='')
            else:
                return_page.add_field(name=f'No Temperament', value='')

            if flag == 'Regular Success':
                return_page.add_field(name='Hunt:', value=f'Success | {hunt_hunger * mC.HUNGER_EMOJI}')

            elif flag == 'Messy Crit':
                return_page.add_field(name='Hunt:', value=f'Messy Crit | {hunt_hunger * mC.HUNGER_EMOJI}')

            elif flag == 'Crit':
                return_page.add_field(name='Hunt:', value=f'Flawless | {hunt_hunger * mC.HUNGER_EMOJI}')

            with sqlite3.connect(f'cogs//vampire//characters//{str(interaction.user.id)}//{character_name}//{character_name}.sqlite') as db:
                cursor = db.cursor()
                cursor.execute('UPDATE charInfo SET hunger=?', (str(int(hunt_hunger))))  # str(int()) is over excessive, however.
            await yU.cacheClear(target_cache)
            await yU.cacheWrite(target_cache, {'mark': 'hunt_success'})

    return return_page


async def reRoller(self, interaction, button, return_page):
    character_name = await vU.getCharacterName(interaction)

    # Finding Starting Roll Pool, Difficulty, & Roll Info
    with sqlite3.connect(f'cogs//vampire//characters//{str(interaction.user.id)}//{character_name}//{character_name}.sqlite') as db:
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

    roll_results: dict = {'regular_crit'  : regular_crit, 'hunger_crit': hunger_crit, 'regular_success': regular_success,
                          'hunger_success': hunger_success, 'regular_fail': regular_fail, 'hunger_skull': hunger_skulls}

    # Reroll up to 3 regular-failures
    if roll_results['regular_fail'] >= 3:
        rerolls = 3
        roll_results['regular_fail'] -= 3
    else:
        rerolls = roll_results['regular_fail']
        roll_results['regular_fail'] -= roll_results['regular_fail']

    # Find new roll numbers
    while 0 < rerolls:
        die_result = randint(1, 10)

        if die_result == 10:
            roll_results['regular_crit'] += 1
        elif die_result >= 6:
            roll_results['regular_success'] += 1
        elif die_result <= 5:
            roll_results['regular_fail'] += 1

        rerolls -= 1

    # Update roll info
    try:
        with sqlite3.connect(f'cogs//vampire//characters//{str(interaction.user.id)}//{character_name}//{character_name}.sqlite') as db:
            cursor = db.cursor()
            cursor.execute('UPDATE rerollInfo SET regularCritDie=?, regularSuccess=?, regularFail=?',
                           (roll_results['regular_crit'], roll_results['regular_success'], roll_results['regular_fail']))
            db.commit()
    except sqlite3.Error as e:
        log.error(f'reRoller_2 | SQLITE3 ERROR | {e}')

    # Find New Crits
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

    if total_successes >= difficulty and flag == '':
        flag = 'Regular Success'
    elif total_successes <= difficulty and flag == '':
        flag = 'Regular Fail'

    if wp_base <= wp_AGG:
        button.disabled = True
        button.label = 'Fate Sealed'
        await interaction.response.edit_message(view=self)
        return
    elif wp_base <= wp_SUP:
        db.cursor().execute('UPDATE willpower SET willpowerAGG=?', (str(wp_AGG + 1),))
    else:
        db.cursor().execute('UPDATE willpower SET willpowerSUP=?', (str(wp_SUP + 1),))
    db.commit()

    button.disabled = True
    button.label = 'Fate Tempted'

    # Assigns Information
    return_page.add_field(name='Roll Result:', value=f'{total_successes} | {flag}')
    log.crit(f'{total_successes=} | {crits=} | {difficulty=}')
    return return_page


# ? Until Functional, the button will be gray
# ? KRV = KINDRED_ROLLER_VIEW
class KRV_DIFFICULTY(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Attributes', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.green, row=2)
    async def attribute_button_callback(self, interaction, button):
        response_page, response_view = await vPS.pageEVNav(interaction, 'roller.attribute')
        response_page = await rPB.rollerBasicPageInformation(interaction, response_page)  # ! Roller Exclusive
        await interaction.response.edit_message(embed=response_page, view=response_view(self.CLIENT))

    @discord.ui.button(label='Physical Skills', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.green, row=3)
    async def physical_button_callback(self, interaction, button):
        response_page, response_view = await vPS.pageEVNav(interaction, 'roller.physical')
        response_page = await rPB.rollerBasicPageInformation(interaction, response_page)  # ! Roller Exclusive
        await interaction.response.edit_message(embed=response_page, view=response_view(self.CLIENT))

    @discord.ui.button(label='Social Skills', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.green, row=3)
    async def social_button_callback(self, interaction, button):
        response_page, response_view = await vPS.pageEVNav(interaction, 'roller.social')
        response_page = await rPB.rollerBasicPageInformation(interaction, response_page)  # ! Roller Exclusive
        await interaction.response.edit_message(embed=response_page, view=response_view(self.CLIENT))

    @discord.ui.button(label='Mental Skills', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.green, row=3)
    async def mental_button_callback(self, interaction, button):
        response_page, response_view = await vPS.pageEVNav(interaction, 'roller.mental')
        response_page = await rPB.rollerBasicPageInformation(interaction, response_page)  # ! Roller Exclusive
        await interaction.response.edit_message(embed=response_page, view=response_view(self.CLIENT))

    @discord.ui.button(label='Discipline', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.green, row=2)
    async def discipline_button_callback(self, interaction, button):
        response_page, response_view = await vPS.pageEVNav(interaction, 'roller.discipline')
        response_page = await rPB.rollerBasicPageInformation(interaction, response_page)  # ! Roller Exclusive
        await interaction.response.edit_message(embed=response_page, view=response_view(self.CLIENT))

    @discord.ui.button(label='Extras', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.green, row=2)
    async def extras_button_callback(self, interaction, button):
        response_page, response_view = await vPS.pageEVNav(interaction, 'roller.extras')
        response_page = await rPB.rollerBasicPageInformation(interaction, response_page)  # ! Roller Exclusive
        await interaction.response.edit_message(embed=response_page, view=response_view(self.CLIENT))

    @discord.ui.button(label='Home', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.gray, row=0)
    async def stay_button_callback(self, interaction, button):
        response_page, response_view = await vPS.pageEVNav(interaction, 'roller.difficulty')
        response_page = await rPB.rollerBasicPageInformation(interaction, response_page)  # ! Roller Exclusive
        await interaction.response.edit_message(embed=response_page, view=response_view(self.CLIENT))

    @discord.ui.button(label='Marks', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=0)
    async def marks_button_callback(self, interaction, button):
        response_page, response_view = await vPS.pageEVNav(interaction, 'roller.marks')
        response_page = await rPB.rollerBasicPageInformation(interaction, response_page)  # ! Roller Exclusive
        await interaction.response.edit_message(embed=response_page, view=response_view(self.CLIENT))

    @discord.ui.select(placeholder='Select Difficulty', options=rO.difficulty_options, max_values=1, min_values=1, row=1)
    async def difficulty_select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        response_page, response_view = await vPS.pageEVNav(interaction, 'roller.difficulty')
        character_name = await vU.getCharacterName(interaction)

        # Actual Logic of the Selection
        with sqlite3.connect(f'cogs//vampire//characters//{str(interaction.user.id)}//{character_name}//{character_name}.sqlite') as db:
            db.cursor().execute('UPDATE commandvars SET difficulty=?', (select.values))  # ! Parentheses are NOT redundant
            db.commit()
        # Actual Logic of the Selection

        response_page = await rPB.rollerBasicPageInformation(interaction, response_page)  # ! Roller Exclusive
        await interaction.response.edit_message(embed=response_page, view=response_view(self.CLIENT))

    @discord.ui.button(label='Roll', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.red, row=0)
    async def roll_button_callback(self, interaction, button):
        response_page, response_view = await vPS.pageEVNav(interaction, 'roller.rolled')

        # Actual Button Logic
        response_page = await normalRoller(interaction, response_page)
        # Actual Button Logic

        response_page = await rPB.rollerBasicPageInformation(interaction, response_page)  # ! Roller Exclusive
        await interaction.response.edit_message(embed=response_page, view=response_view(self.CLIENT))

    @discord.ui.button(label='Clear', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.red, row=0)
    async def clear_button_callback(self, interaction, button):
        response_page, response_view = await vPS.pageEVNav(interaction, 'roller.difficulty')

        # Actual Logic of the Selection
        await clearDBRollInfo(interaction)
        # Actual Logic of the Selection

        response_page = await rPB.rollerBasicPageInformation(interaction, response_page)  # ! Roller Exclusive
        await interaction.response.edit_message(embed=response_page, view=response_view(self.CLIENT))


class KRV_ATTRIBUTE(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Back', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=0)
    async def back_button_callback(self, interaction, button):
        response_page, response_view = await vPS.pageEVNav(interaction, 'roller.difficulty')
        response_page = await rPB.rollerBasicPageInformation(interaction, response_page)  # ! Roller Exclusive
        await interaction.response.edit_message(embed=response_page, view=response_view(self.CLIENT))

    @discord.ui.select(placeholder='Select Attribute(s)', options=rO.attribute_options, max_values=3, min_values=1, row=1)
    async def attribute_select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        response_page, response_view = await vPS.pageEVNav(interaction, 'roller.attribute')
        character_name = await vU.getCharacterName(interaction)

        targetDB = f'cogs//vampire//characters//{str(interaction.user.id)}//{character_name}//{character_name}.sqlite'

        # Actual Logic of the Selection
        await basicSelection(select, targetDB, 'charAttributes')
        # Actual Logic of the Selection

        response_page = await rPB.rollerBasicPageInformation(interaction, response_page)  # ! Roller Exclusive
        await interaction.response.edit_message(embed=response_page, view=response_view(self.CLIENT))

    @discord.ui.button(label='Roll', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.red, row=0)
    async def roll_button_callback(self, interaction, button):
        response_page, response_view = await vPS.pageEVNav(interaction, 'roller.rolled')

        # Actual Button Logic
        response_page = await normalRoller(interaction, response_page)
        # Actual Button Logic

        response_page = await rPB.rollerBasicPageInformation(interaction, response_page)  # ! Roller Exclusive
        await interaction.response.edit_message(embed=response_page, view=response_view(self.CLIENT))

    @discord.ui.button(label='Clear', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.red, row=0)
    async def clear_button_callback(self, interaction, button):
        response_page, response_view = await vPS.pageEVNav(interaction, 'roller.difficulty')

        # Actual Logic of the Selection
        await clearDBRollInfo(interaction)
        # Actual Logic of the Selection

        response_page = await rPB.rollerBasicPageInformation(interaction, response_page)  # ! Roller Exclusive
        await interaction.response.edit_message(embed=response_page, view=response_view(self.CLIENT))


class KRV_PHYSICAL(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Back', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=0)
    async def back_button_callback(self, interaction, button):
        response_page, response_view = await vPS.pageEVNav(interaction, 'roller.difficulty')
        response_page = await rPB.rollerBasicPageInformation(interaction, response_page)  # ! Roller Exclusive
        await interaction.response.edit_message(embed=response_page, view=response_view(self.CLIENT))

    @discord.ui.select(placeholder='Select Physical Skill(s)', options=rO.physical_skill_options, max_values=3, min_values=1, row=1)
    async def attribute_select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        response_page, response_view = await vPS.pageEVNav(interaction, 'roller.physical')
        character_name = await vU.getCharacterName(interaction)

        targetDB = f'cogs//vampire//characters//{str(interaction.user.id)}//{character_name}//{character_name}.sqlite'

        # Actual Logic of the Selection
        await basicSelection(select, targetDB, 'physicalSkills')
        # Actual Logic of the Selection

        response_page = await rPB.rollerBasicPageInformation(interaction, response_page)  # ! Roller Exclusive
        await interaction.response.edit_message(embed=response_page, view=response_view(self.CLIENT))

    @discord.ui.button(label='Roll', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.red, row=0)
    async def roll_button_callback(self, interaction, button):
        response_page, response_view = await vPS.pageEVNav(interaction, 'roller.rolled')

        # Actual Button Logic
        response_page = await normalRoller(interaction, response_page)
        # Actual Button Logic

        response_page = await rPB.rollerBasicPageInformation(interaction, response_page)  # ! Roller Exclusive
        await interaction.response.edit_message(embed=response_page, view=response_view(self.CLIENT))

    @discord.ui.button(label='Clear', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.red, row=0)
    async def clear_button_callback(self, interaction, button):
        response_page, response_view = await vPS.pageEVNav(interaction, 'roller.difficulty')

        # Actual Logic of the Selection
        await clearDBRollInfo(interaction)
        # Actual Logic of the Selection

        response_page = await rPB.rollerBasicPageInformation(interaction, response_page)  # ! Roller Exclusive
        await interaction.response.edit_message(embed=response_page, view=response_view(self.CLIENT))


class KRV_SOCIAL(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Back', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=0)
    async def back_button_callback(self, interaction, button):
        response_page, response_view = await vPS.pageEVNav(interaction, 'roller.difficulty')
        response_page = await rPB.rollerBasicPageInformation(interaction, response_page)  # ! Roller Exclusive
        await interaction.response.edit_message(embed=response_page, view=response_view(self.CLIENT))

    @discord.ui.select(placeholder='Select Social Skill(s)', options=rO.social_skill_options, max_values=3, min_values=1, row=1)
    async def social_select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        response_page, response_view = await vPS.pageEVNav(interaction, 'roller.social')
        character_name = await vU.getCharacterName(interaction)

        targetDB = f'cogs//vampire//characters//{str(interaction.user.id)}//{character_name}//{character_name}.sqlite'

        # Actual Logic of the Selection
        await basicSelection(select, targetDB, 'socialSkills')
        # Actual Logic of the Selection

        response_page = await rPB.rollerBasicPageInformation(interaction, response_page)  # ! Roller Exclusive
        await interaction.response.edit_message(embed=response_page, view=response_view(self.CLIENT))

    @discord.ui.button(label='Roll', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.red, row=0)
    async def roll_button_callback(self, interaction, button):
        response_page, response_view = await vPS.pageEVNav(interaction, 'roller.rolled')

        # Actual Button Logic
        response_page = await normalRoller(interaction, response_page)
        # Actual Button Logic

        response_page = await rPB.rollerBasicPageInformation(interaction, response_page)  # ! Roller Exclusive
        await interaction.response.edit_message(embed=response_page, view=response_view(self.CLIENT))

    @discord.ui.button(label='Clear', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.red, row=0)
    async def clear_button_callback(self, interaction, button):
        response_page, response_view = await vPS.pageEVNav(interaction, 'roller.difficulty')

        # Actual Logic of the Selection
        await clearDBRollInfo(interaction)
        # Actual Logic of the Selection

        response_page = await rPB.rollerBasicPageInformation(interaction, response_page)  # ! Roller Exclusive
        await interaction.response.edit_message(embed=response_page, view=response_view(self.CLIENT))


class KRV_MENTAL(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Back', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=0)
    async def back_button_callback(self, interaction, button):
        response_page, response_view = await vPS.pageEVNav(interaction, 'roller.difficulty')
        response_page = await rPB.rollerBasicPageInformation(interaction, response_page)  # ! Roller Exclusive
        await interaction.response.edit_message(embed=response_page, view=response_view(self.CLIENT))

    @discord.ui.select(placeholder='Select Mental Skill(s)', options=rO.mental_skill_options, max_values=3, min_values=1, row=1)
    async def mental_select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        response_page, response_view = await vPS.pageEVNav(interaction, 'roller.mental')
        character_name = await vU.getCharacterName(interaction)

        targetDB = f'cogs//vampire//characters//{str(interaction.user.id)}//{character_name}//{character_name}.sqlite'

        # Actual Logic of the Selection
        await basicSelection(select, targetDB, 'mentalSkills')
        # Actual Logic of the Selection

        response_page = await rPB.rollerBasicPageInformation(interaction, response_page)  # ! Roller Exclusive
        await interaction.response.edit_message(embed=response_page, view=response_view(self.CLIENT))

    @discord.ui.button(label='Roll', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.red, row=0)
    async def roll_button_callback(self, interaction, button):
        response_page, response_view = await vPS.pageEVNav(interaction, 'roller.rolled')

        # Actual Button Logic
        response_page = await normalRoller(interaction, response_page)
        # Actual Button Logic

        response_page = await rPB.rollerBasicPageInformation(interaction, response_page)  # ! Roller Exclusive
        await interaction.response.edit_message(embed=response_page, view=response_view(self.CLIENT))

    @discord.ui.button(label='Clear', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.red, row=0)
    async def clear_button_callback(self, interaction, button):
        response_page, response_view = await vPS.pageEVNav(interaction, 'roller.difficulty')

        # Actual Logic of the Selection
        await clearDBRollInfo(interaction)
        # Actual Logic of the Selection

        response_page = await rPB.rollerBasicPageInformation(interaction, response_page)  # ! Roller Exclusive
        await interaction.response.edit_message(embed=response_page, view=response_view(self.CLIENT))


class KRV_DISCIPLINE(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Back', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=0)
    async def back_button_callback(self, interaction, button):
        response_page, response_view = await vPS.pageEVNav(interaction, 'roller.difficulty')
        response_page = await rPB.rollerBasicPageInformation(interaction, response_page)  # ! Roller Exclusive
        await interaction.response.edit_message(embed=response_page, view=response_view(self.CLIENT))

    @discord.ui.select(placeholder='Select Discipline(s)', options=rO.discipline_options, max_values=3, min_values=1, row=1)
    async def discipline_select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        response_page, response_view = await vPS.pageEVNav(interaction, 'roller.discipline')
        character_name = await vU.getCharacterName(interaction)

        targetDB = f'cogs//vampire//characters//{str(interaction.user.id)}//{character_name}//{character_name}.sqlite'

        # Actual Logic of the Selection
        await basicSelection(select, targetDB, 'disciplines')
        # Actual Logic of the Selection

        response_page = await rPB.rollerBasicPageInformation(interaction, response_page)  # ! Roller Exclusive
        await interaction.response.edit_message(embed=response_page, view=response_view(self.CLIENT))

    @discord.ui.button(label='Roll', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.red, row=0)
    async def roll_button_callback(self, interaction, button):
        response_page, response_view = await vPS.pageEVNav(interaction, 'roller.rolled')

        # Actual Button Logic
        response_page = await normalRoller(interaction, response_page)
        # Actual Button Logic

        response_page = await rPB.rollerBasicPageInformation(interaction, response_page)  # ! Roller Exclusive
        await interaction.response.edit_message(embed=response_page, view=response_view(self.CLIENT))

    @discord.ui.button(label='Clear', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.red, row=0)
    async def clear_button_callback(self, interaction, button):
        response_page, response_view = await vPS.pageEVNav(interaction, 'roller.difficulty')

        # Actual Logic of the Selection
        await clearDBRollInfo(interaction)
        # Actual Logic of the Selection

        response_page = await rPB.rollerBasicPageInformation(interaction, response_page)  # ! Roller Exclusive
        await interaction.response.edit_message(embed=response_page, view=response_view(self.CLIENT))


class KRV_EXTRAS(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Back', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=0)
    async def back_button_callback(self, interaction, button):
        response_page, response_view = await vPS.pageEVNav(interaction, 'roller.difficulty')
        response_page = await rPB.rollerBasicPageInformation(interaction, response_page)  # ! Roller Exclusive
        await interaction.response.edit_message(embed=response_page, view=response_view(self.CLIENT))

    @discord.ui.button(label='Roll', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.red, row=0)
    async def roll_button_callback(self, interaction, button):
        response_page, response_view = await vPS.pageEVNav(interaction, 'roller.rolled')

        # Actual Button Logic
        response_page = await normalRoller(interaction, response_page)
        # Actual Button Logic

        response_page = await rPB.rollerBasicPageInformation(interaction, response_page)  # ! Roller Exclusive
        await interaction.response.edit_message(embed=response_page, view=response_view(self.CLIENT))

    @discord.ui.button(label='Clear', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.red, row=0)
    async def clear_button_callback(self, interaction, button):
        response_page, response_view = await vPS.pageEVNav(interaction, 'roller.difficulty')

        # Actual Button Logic
        await clearDBRollInfo(interaction)
        # Actual Button Logic

        response_page = await rPB.rollerBasicPageInformation(interaction, response_page)  # ! Roller Exclusive
        await interaction.response.edit_message(embed=response_page, view=response_view(self.CLIENT))

    @discord.ui.select(placeholder='Select Extra(s)', options=rO.extra_options, max_values=3, min_values=1, row=1)
    async def extra_select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        response_page, response_view = await vPS.pageEVNav(interaction, 'roller.extras')
        character_name = await vU.getCharacterName(interaction)

        targetDB = f'cogs//vampire//characters//{str(interaction.user.id)}//{character_name}//{character_name}.sqlite'

        # Actual Logic of the Selection
        with sqlite3.connect(targetDB) as db:
            cursor = db.cursor()

            roll_pool = cursor.execute('SELECT rollPool FROM commandvars').fetchone()[0]
            roll_comp = cursor.execute('SELECT poolComp from commandVars').fetchone()[0]

            for_var = 0
            for x in select.values:
                value = select.values[for_var]
                roll_pool += int(value)
                roll_comp = f'{roll_comp} + {select.values[for_var]}[{value}]'
                for_var += 1

            cursor.execute('UPDATE commandvars SET poolComp=?', (roll_comp,))
            cursor.execute('UPDATE commandvars SET rollPool=?', (roll_pool,))
            db.commit()

        select.disabled = True
        # Actual Logic of the Selection

        response_page = await rPB.rollerBasicPageInformation(interaction, response_page)  # ! Roller Exclusive
        await interaction.response.edit_message(embed=response_page, view=response_view(self.CLIENT))

    @discord.ui.button(label='Blood Surge [Rolls]', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.red, row=2)
    async def blood_surge_button_callback(self, interaction, button):

        # Actual Button Logic
        character_name = await vU.getCharacterName(interaction)
        targetDB = f'cogs//vampire//characters//{str(interaction.user.id)}//{character_name}//{character_name}.sqlite'

        with sqlite3.connect(targetDB) as db:
            response_page, response_view = await vPS.pageEVNav(interaction, 'roller.rolled')

            # Actual Button Logic Start
            cursor = db.cursor()

            roll_pool = cursor.execute('SELECT rollPool FROM commandVars').fetchone()[0]
            roll_comp = cursor.execute('SELECT poolComp from commandVars').fetchone()[0]

            hunger = int(cursor.execute('SELECT hunger from charInfo').fetchone()[0])
            hunger_emoji = str(mC.HUNGER_EMOJI * hunger)

            rouse_result = await vU.rouseCheck(interaction)

            if rouse_result == 'Frenzy':
                # Should be moved away from roller.extras when Frenzy stuff is completed
                response_page, response_view = await vPS.pageEVNav(interaction, 'roller.extras')
                response_page = await rPB.rollerBasicPageInformation(interaction, response_page)  # ! Roller Exclusive

                response_page.add_field(name='Blood Surge Rouse __Frenzy__', value=f'{hunger_emoji}')
                await interaction.response.edit_message(embed=response_page, view=response_view(self.CLIENT))
                return

            if rouse_result == 'Fail':
                response_page.add_field(name='Blood Surge Rouse Failed', value=f'{hunger_emoji}')

            elif rouse_result == 'Pass':
                response_page.add_field(name='Blood Surge Rouse Passed', value=f'{hunger_emoji}')

            roll_pool += 2
            roll_comp = f'{roll_comp} + Blood Surge[2]'

            cursor.execute('UPDATE commandvars SET poolComp=?', (roll_comp,))
            cursor.execute('UPDATE commandvars SET rollPool=?', (roll_pool,))
            db.commit()

        response_page = await normalRoller(interaction, response_page)
        # Actual Button Logic End

        response_page = await rPB.rollerBasicPageInformation(interaction, response_page)  # ! Roller Exclusive
        await interaction.response.edit_message(embed=response_page, view=response_view(self.CLIENT))


class KRV_ROLLED(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Reroll', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.red, row=0)
    async def back_button_callback(self, interaction, button):
        response_page, response_view = await vPS.pageEVNav(interaction, 'roller.rerolled')

        # Actual Button Logic
        response_page = await reRoller(self, interaction, button, response_page)
        # Actual Button Logic End

        response_page = await rPB.rollerBasicPageInformation(interaction, response_page)  # ! Roller Exclusive
        await interaction.response.edit_message(embed=response_page, view=response_view(self.CLIENT))


class KRV_REROLLED(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT


class KRV_MARKS(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Roll', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.red, row=0)
    async def roll_button_callback(self, interaction, button):
        response_page, response_view = await vPS.pageEVNav(interaction, 'roller.rolled')

        # Actual Button Logic
        response_page = await normalRoller(interaction, response_page)
        # Actual Button Logic

        response_page = await rPB.rollerBasicPageInformation(interaction, response_page)  # ! Roller Exclusive
        await interaction.response.edit_message(embed=response_page, view=response_view(self.CLIENT))

    @discord.ui.button(label='Home', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=0)
    async def stay_button_callback(self, interaction, button):
        response_page, response_view = await vPS.pageEVNav(interaction, 'roller.difficulty')
        response_page = await rPB.rollerBasicPageInformation(interaction, response_page)  # ! Roller Exclusive
        await interaction.response.edit_message(embed=response_page, view=response_view(self.CLIENT))

    @discord.ui.button(label='Mark Roll as Hunt', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.red, row=1)
    async def hunt_mark_button_callback(self, interaction, button):
        response_page, response_view = await vPS.pageEVNav(interaction, 'roller.difficulty')
        character_name = await vU.getCharacterName(interaction)

        # This is atrocious, but I'm just throwing it together, will fix.
        # I may give the roller an entire system based on "Marks", but its TBD
        # Such system may assist with adding things such as: Blood Surge; Remorse; Clan Bane; Diablerie; Frenzy; Compulsions; etc.
        # Actual Button Logic
        target_cache = f'cogs//vampire//characters//{str(interaction.user.id)}//{character_name}//roll_mark.yaml'
        await yU.cacheClear(target_cache)
        await yU.cacheWrite(target_cache, {'mark': 'hunt'})
        button.disabled = True  # DOESN'T WORK
        # Actual Button Logic End

        response_page = await rPB.rollerBasicPageInformation(interaction, response_page)  # ! Roller Exclusive
        await interaction.response.edit_message(embed=response_page, view=self)

