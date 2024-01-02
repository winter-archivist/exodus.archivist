import discord
import sqlite3
from zenlog import log
from random import randint
from discord.ui import View

import cogs.vampire.vMisc.vampirePageSystem as vPS
import cogs.vampire.vMisc.vampireUtils as vU

import cogs.vampire.vRoller.rollerPageBuilders as rPB
import cogs.vampire.vRoller.rollerOptions as rO


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
    log.crit(f'{total_successes} | {crits} | {difficulty}')
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
    log.crit(f'{total_successes} | {crits} | {difficulty}')
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

    @discord.ui.button(label='Blood Surge', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.red, row=2)
    async def blood_surge_button_callback(self, interaction, button):
        response_page, response_view = await vPS.pageEVNav(interaction, 'roller.extras')

        # Actual Button Logic
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

