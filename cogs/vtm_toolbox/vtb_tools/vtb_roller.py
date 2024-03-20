import random
import discord
import discord.ui
from zenlog import log

import misc.config.main_config as mc

import cogs.vtm_toolbox.vtb_misc.vtb_utils as vu
import cogs.vtm_toolbox.vtb_misc.vtb_pages as vp
import cogs.vtm_toolbox.vtb_characters.vtb_character_manager as cm

import cogs.vtm_toolbox.vtb_tools.vtb_roller_options as ro


async def return_to_home(self, interaction: discord.Interaction) -> None:
    CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
    page: discord.Embed = await vp.basic_page_builder(CHARACTER, 'Home', '', 'purple')
    page: discord.Embed = await vp.standard_roller_page_modifications(page, CHARACTER)
    await interaction.response.send_message(embed=page, view=Home(self.CLIENT))
    return None


class Home(discord.ui.View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Roll Types', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.red, row=0)
    async def roll_button_callback(self, interaction: discord.Interaction, button: discord.ui.Select):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.basic_page_builder(CHARACTER, 'Roll Types', '', 'purple')
        page: discord.Embed = await vp.standard_roller_page_modifications(page, CHARACTER)
        await interaction.response.edit_message(embed=page, view=RollTypes(self.CLIENT))
        return

    @discord.ui.button(label='Attributes', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=0)
    async def attributes_button_callback(self, interaction, button):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.basic_page_builder(CHARACTER, 'Attributes Page', '', 'purple')
        page: discord.Embed = await vp.standard_roller_page_modifications(page, CHARACTER)
        await interaction.response.send_message(embed=page, view=Attributes(self.CLIENT))
        return

    @discord.ui.button(label='Skills', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=0)
    async def skills_button_callback(self, interaction, button):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.basic_page_builder(CHARACTER, 'Skills Page', '', 'purple')
        page: discord.Embed = await vp.standard_roller_page_modifications(page, CHARACTER)
        await interaction.response.send_message(embed=page, view=Skills(self.CLIENT))
        return

    @discord.ui.button(label='Disciplines', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=0)
    async def disciplines_button_callback(self, interaction, button):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.basic_page_builder(CHARACTER, 'Disciplines Page', '', 'purple')
        page: discord.Embed = await vp.standard_roller_page_modifications(page, CHARACTER)
        await interaction.response.send_message(embed=page, view=Disciplines(self.CLIENT))
        return

    @discord.ui.button(label='Extras', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=0)
    async def extras_button_callback(self, interaction, button):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.basic_page_builder(CHARACTER, 'Extras Page', '', 'purple')
        page: discord.Embed = await vp.standard_roller_page_modifications(page, CHARACTER)
        await interaction.response.send_message(embed=page, view=Extras(self.CLIENT))
        return


class RollTypes(discord.ui.View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Home', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=0)
    async def home_button_callback(self, interaction, button):
        await return_to_home(self, interaction)
        return

    @discord.ui.button(label='Blood Surge', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.red, row=0)
    async def blood_surge_button_callback(self, interaction, button):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.basic_page_builder(CHARACTER, 'Roll Types', '', 'purple')

        ROUSE_RESULT_TUPLE = await CHARACTER.__rouse_check__()
        RR_TYPE: str = ROUSE_RESULT_TUPLE[0]
        HUNGER_EMOJI: str = str(mc.HUNGER_EMOJI * ROUSE_RESULT_TUPLE[1])

        if RR_TYPE == 'Frenzy':
            page.add_field(name='Blood Surge Rouse __Frenzy__', value=f'{HUNGER_EMOJI}')
            page: discord.Embed = await vp.standard_roller_page_modifications(page, CHARACTER)
            await interaction.response.send_message(embed=page, view=Home(self.CLIENT))
            return

        if RR_TYPE == 'Fail':
            page.add_field(name='Blood Surge Rouse Failed', value=f'{HUNGER_EMOJI}')

        elif RR_TYPE == 'Pass':
            page.add_field(name='Blood Surge Rouse Passed', value=f'{HUNGER_EMOJI}')

        ROLL_INFO: dict = await CHARACTER.__get_values__(('pool', 'composition'), 'roll/info')
        NEW_ROLL_POOL: int = int(ROLL_INFO['pool'])
        NEW_ROLL_COMPOSITION = f'{ROLL_INFO["composition"]}, Blood Surge[2]'

        await CHARACTER.__update_values__(('pool', 'composition'), (NEW_ROLL_POOL, NEW_ROLL_COMPOSITION), 'roll/info')

        page: discord.Embed = await vp.standard_roller_page_modifications(page, CHARACTER)
        await interaction.response.send_message(embed=page, view=Home(self.CLIENT))
        return

    @discord.ui.select(placeholder='Select Difficulty', options=ro.difficulty_options, max_values=1, min_values=1, row=1)
    async def difficulty_select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.basic_page_builder(CHARACTER, 'Home', '', 'purple')

        # Parenthesis on (select.values) are NOT redundant!!!
        await CHARACTER.__update_value__('difficulty', (select.values), 'roll/info')

        page: discord.Embed = await vp.standard_roller_page_modifications(page, CHARACTER)
        await interaction.response.edit_message(embed=page, view=Home(self.CLIENT))
        return

    @discord.ui.button(label='Standard Roll', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.red, row=2)
    async def roll_button_callback(self, interaction: discord.Interaction, button: discord.ui.Select):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.basic_page_builder(CHARACTER, 'Standard Roll', '', 'purple')

        page: discord.Embed = await CHARACTER.__roll__(page)

        page: discord.Embed = await vp.standard_roller_page_modifications(page, CHARACTER)
        await interaction.response.edit_message(embed=page, view=Reroll(self.CLIENT))
        return

    @discord.ui.button(label='Hunting Roll', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.red, row=2)
    async def hunt_button_callback(self, interaction, button):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.basic_page_builder(CHARACTER, 'Roll', '', 'purple')

        page = await CHARACTER.__hunt__(page)

        page: discord.Embed = await vp.standard_roller_page_modifications(page, CHARACTER)
        await interaction.response.edit_message(embed=page, view=Reroll(self.CLIENT))
        return


class Attributes(discord.ui.View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Home', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=0)
    async def home_button_callback(self, interaction, button):
        await return_to_home(self, interaction)
        return

    @discord.ui.select(placeholder='Select Attribute(s)', options=ro.attribute_options, max_values=3, min_values=1, row=1)
    async def attribute_select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.basic_page_builder(CHARACTER, 'Attributes Page', '', 'purple')
        page = await vp.standard_roll_select(CHARACTER, page, select, 'attributes')
        await interaction.response.edit_message(embed=page, view=Attributes(self.CLIENT))
        return


class Skills(discord.ui.View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Home', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=0)
    async def home_button_callback(self, interaction, button):
        await return_to_home(self, interaction)
        return

    @discord.ui.select(placeholder='Select Physical Skill(s)', options=ro.physical_skill_options, max_values=3, min_values=1, row=1)
    async def physical_select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.basic_page_builder(CHARACTER, 'Skills Page', '', 'purple')
        page = await vp.standard_roll_select(CHARACTER, page, select, 'skills/physical')
        await interaction.response.edit_message(embed=page, view=Skills(self.CLIENT))
        return

    @discord.ui.select(placeholder='Select Social Skill(s)', options=ro.social_skill_options, max_values=3, min_values=1, row=2)
    async def social_select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.basic_page_builder(CHARACTER, 'Skills Page', '', 'purple')
        page = await vp.standard_roll_select(CHARACTER, page, select, 'skills/social')
        await interaction.response.edit_message(embed=page, view=Skills(self.CLIENT))
        return

    @discord.ui.select(placeholder='Select Mental Skill(s)', options=ro.mental_skill_options, max_values=3, min_values=1, row=3)
    async def mental_select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.basic_page_builder(CHARACTER, 'Skills Page', '', 'purple')
        page = await vp.standard_roll_select(CHARACTER, page, select, 'skills/mental')
        await interaction.response.edit_message(embed=page, view=Skills(self.CLIENT))
        return


class Disciplines(discord.ui.View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Home', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=0)
    async def home_button_callback(self, interaction, button):
        await return_to_home(self, interaction)
        return

    @discord.ui.select(placeholder='Select Discipline(s)', options=ro.discipline_options, max_values=3, min_values=1, row=1)
    async def physical_select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.basic_page_builder(CHARACTER, 'Disciplines Page', '', 'purple')
        page = await vp.standard_roll_select(CHARACTER, page, select, 'disciplines')
        await interaction.response.edit_message(embed=page, view=Disciplines(self.CLIENT))
        return


class Extras(discord.ui.View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Home', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=0)
    async def home_button_callback(self, interaction, button):
        await return_to_home(self, interaction)
        return

    @discord.ui.select(placeholder='Extra Select', options=ro.extra_options, max_values=1, min_values=1, row=1)
    async def extra_select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.basic_page_builder(CHARACTER, 'Extras Page', '', 'purple')

        CHARACTER_INFORMATION: dict = await CHARACTER.__get_values__(('pool', 'composition'), 'roll/info')
        pool: int = CHARACTER_INFORMATION['pool']
        composition: str = CHARACTER_INFORMATION['composition']

        pool += int(select.values[0])
        composition = f'{composition}, [{select.values[0]}]'

        await CHARACTER.__update_values__(('pool', 'composition',), (pool, composition), 'roll/info')

        select.disabled = True

        page: discord.Embed = await vp.standard_roller_page_modifications(page, CHARACTER)
        await interaction.response.edit_message(embed=page, view=Extras(self.CLIENT))
        return


class Reroll(discord.ui.View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Reroll', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.red, row=0)
    async def reroll_button_callback(self, interaction, button):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.basic_page_builder(CHARACTER, 'Reroll', '', 'red')

        WANTED_WILLPOWER_INFORMATION: tuple = ('base_willpower', 'superficial_willpower_damage', 'aggravated_willpower_damage')
        WILLPOWER_FILE: str = 'willpower'
        WILLPOWER_DICT: dict = await CHARACTER.__get_values__(WANTED_WILLPOWER_INFORMATION, WILLPOWER_FILE)

        WANTED_ROLL_INFORMATION: tuple = ('regular_crit', 'regular_success', 'regular_fail', 'hunger_crit', 'hunger_success', 'hunger_fail', 'skull_count', 'difficulty')
        ROLL_FILE: str = 'roll/info'
        ROLL_DICT: dict = await CHARACTER.__get_values__(WANTED_ROLL_INFORMATION, ROLL_FILE)

        roll_results: dict = {'regular_crit': ROLL_DICT['regular_crit'], 'regular_success': ROLL_DICT['regular_success'], 'regular_fail': ROLL_DICT['regular_fail'],
                              'hunger_crit': ROLL_DICT['hunger_crit'], 'hunger_success': ROLL_DICT['hunger_success'], 'hunger_fail': ROLL_DICT['hunger_fail'],
                              'skull_count': ROLL_DICT['skull_count']}

        rerolls = roll_results['regular_fail']
        # Reroll up to 3 regular-failures
        if roll_results['regular_fail'] >= 3:
            rerolls = 3
            roll_results['regular_fail'] -= 3
        else:
            rerolls = roll_results['regular_fail']
            roll_results['regular_fail'] -= roll_results['regular_fail']

        # Find new roll numbers
        while 0 < rerolls:
            die_result = random.randint(1, 10)

            if die_result == 10:
                roll_results['regular_crit'] += 1
            elif die_result >= 6:
                roll_results['regular_success'] += 1
            elif die_result <= 5:
                roll_results['regular_fail'] += 1

            rerolls -= 1

        ROLL_KEYS: tuple = ('regular_crit', 'regular_success', 'regular_fail', 'hunger_crit', 'hunger_success', 'hunger_fail', 'skull_count')
        FINAL_ROLL_NUMBERS: tuple = (roll_results['regular_crit'], roll_results['regular_success'], roll_results['regular_fail'],
                                     roll_results['hunger_crit'], roll_results['hunger_success'], roll_results['hunger_fail'],
                                     roll_results['skull_count'])

        # Update roll info
        await CHARACTER.__update_values__(ROLL_KEYS, FINAL_ROLL_NUMBERS, 'roll/info')

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

        DIFFICULTY = ROLL_DICT['difficulty']

        if total_successes >= DIFFICULTY and flag == '':
            flag = 'Regular Success'
        elif total_successes <= DIFFICULTY and flag == '':
            flag = 'Regular Fail'

        if WILLPOWER_DICT['base_willpower'] <= WILLPOWER_DICT['aggravated_willpower_damage']:
            button.disabled = True
            button.label = 'Fate Sealed'
            await interaction.response.edit_message(view=vp.EMPTY_VIEW(self.CLIENT))
            return
        elif WILLPOWER_DICT['base_willpower'] <= WILLPOWER_DICT['superficial_willpower_damage']:
            await CHARACTER.__update_value__('aggravated_willpower_damage', int(WILLPOWER_DICT['aggravated_willpower_damage']+1), 'willpower')
        else:
            await CHARACTER.__update_value__('superficial_willpower_damage', int(WILLPOWER_DICT['superficial_willpower_damage']+1), 'willpower')

        button.disabled = True
        button.label = 'Fate Tempted'

        # Assigns Information
        page.add_field(name='Roll Result:', value=f'{total_successes} | {flag}')
        log.crit(f'{total_successes=} | {crits=} | {DIFFICULTY=}')

        page: discord.Embed = await vp.standard_roller_page_modifications(page, CHARACTER)
        await interaction.response.send_message(embed=page, view=vp.EMPTY_VIEW(self.CLIENT))
        return
