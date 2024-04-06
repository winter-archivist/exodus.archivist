import random
import discord
import discord.ui
from zenlog import log

import misc.config.main_config as mc

import cogs.vtm_toolbox.vtm_cm.vtb_pages as vp
import cogs.vtm_toolbox.vtm_cm.vtb_character_manager as cm

import cogs.vtm_toolbox.vtm_cm.sections.options.vtb_roller_options as ro


async def return_to_home(self, interaction: discord.Interaction) -> None:
    CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
    page: discord.Embed = await vp.basic_page_builder(CHARACTER, 'Home', '', 'purple')
    page: discord.Embed = await vp.standard_roller_page_modifications(page, CHARACTER)
    await interaction.response.edit_message(embed=page, view=Home(self.CLIENT))
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
        await interaction.response.edit_message(embed=page, view=Attributes(self.CLIENT))
        return

    @discord.ui.button(label='Skills', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=0)
    async def skills_button_callback(self, interaction, button):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.basic_page_builder(CHARACTER, 'Skills Page', '', 'purple')
        page: discord.Embed = await vp.standard_roller_page_modifications(page, CHARACTER)
        await interaction.response.edit_message(embed=page, view=Skills(self.CLIENT))
        return

    @discord.ui.button(label='Disciplines', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=0)
    async def disciplines_button_callback(self, interaction, button):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.basic_page_builder(CHARACTER, 'Disciplines Page', '', 'purple')
        page: discord.Embed = await vp.standard_roller_page_modifications(page, CHARACTER)
        await interaction.response.edit_message(embed=page, view=Disciplines(self.CLIENT))
        return

    @discord.ui.button(label='Extras', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=0)
    async def extras_button_callback(self, interaction, button):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.basic_page_builder(CHARACTER, 'Extras Page', '', 'purple')
        page: discord.Embed = await vp.standard_roller_page_modifications(page, CHARACTER)
        await interaction.response.edit_message(embed=page, view=Extras(self.CLIENT))
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
            await interaction.response.edit_message(embed=page, view=Home(self.CLIENT))
            return

        if RR_TYPE == 'Fail':
            page.add_field(name='Blood Surge Rouse Failed', value=f'{HUNGER_EMOJI}')

        elif RR_TYPE == 'Pass':
            page.add_field(name='Blood Surge Rouse Passed', value=f'{HUNGER_EMOJI}')

        ROLL_INFO: dict = await CHARACTER.__get_values__(('Pool', 'Composition'), 'roll/info')
        NEW_ROLL_POOL: int = int(ROLL_INFO['Pool'])
        NEW_ROLL_COMPOSITION = f'{ROLL_INFO["Composition"]}, Blood Surge[2]'

        await CHARACTER.__update_values__(('Pool', 'Composition'), (NEW_ROLL_POOL, NEW_ROLL_COMPOSITION), 'roll/info')

        page: discord.Embed = await vp.standard_roller_page_modifications(page, CHARACTER)
        await interaction.response.edit_message(embed=page, view=Home(self.CLIENT))
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

        CHARACTER_INFORMATION: dict = await CHARACTER.__get_values__(('Pool', 'Composition'), 'roll/info')
        pool: int = CHARACTER_INFORMATION['Pool']
        composition: str = CHARACTER_INFORMATION['Composition']

        pool += int(select.values[0])
        composition = f'{composition}, [{select.values[0]}]'

        await CHARACTER.__update_values__(('Pool', 'Composition',), (pool, composition), 'roll/info')

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

        WANTED_WILLPOWER_INFORMATION: tuple = ('Base Willpower', 'Superficial Willpower Damage', 'Aggravated Willpower Damage')
        WILLPOWER_FILE: str = 'willpower'
        WILLPOWER_DICT: dict = await CHARACTER.__get_values__(WANTED_WILLPOWER_INFORMATION, WILLPOWER_FILE)

        WANTED_ROLL_INFORMATION: tuple = ('Regular Crit', 'Regular Success', 'Regular Fail', 'Hunger Crit', 'Hunger Success', 'Hunger Fail', 'Skull Count', 'Difficulty')
        ROLL_FILE: str = 'roll/info'
        ROLL_DICT: dict = await CHARACTER.__get_values__(WANTED_ROLL_INFORMATION, ROLL_FILE)

        roll_results: dict = {'Regular Crit': ROLL_DICT['Regular Crit'], 'Regular Success': ROLL_DICT['Regular Success'], 'Regular Fail': ROLL_DICT['Regular Fail'],
                              'Hunger Crit': ROLL_DICT['Hunger Crit'], 'Hunger Success': ROLL_DICT['Hunger Success'], 'Hunger Fail': ROLL_DICT['Hunger Fail'],
                              'Skull Count': ROLL_DICT['Skull Count']}

        rerolls = roll_results['Regular Fail']
        # Reroll up to 3 regular-failures
        if roll_results['Regular Fail'] >= 3:
            rerolls = 3
            roll_results['Regular Fail'] -= 3
        else:
            rerolls = roll_results['Regular Fail']
            roll_results['Regular Fail'] -= roll_results['Regular Fail']

        # Find new roll numbers
        while 0 < rerolls:
            die_result = random.randint(1, 10)

            if die_result == 10:
                roll_results['Regular Crit'] += 1
            elif die_result >= 6:
                roll_results['Regular Success'] += 1
            elif die_result <= 5:
                roll_results['Regular Fail'] += 1

            rerolls -= 1

        ROLL_KEYS: tuple = ('Regular Crit', 'Regular Success', 'Regular Fail', 'Hunger_Crit', 'Hunger Success', 'Hunger Fail', 'Skull Count')
        FINAL_ROLL_NUMBERS: tuple = (roll_results['Regular Crit'], roll_results['Regular Success'], roll_results['Regular Fail'],
                                     roll_results['Hunger Crit'], roll_results['Hunger Success'], roll_results['Hunger Fail'],
                                     roll_results['Skull Count'])

        # Update roll info
        await CHARACTER.__update_values__(ROLL_KEYS, FINAL_ROLL_NUMBERS, 'roll/info')

        # Find New Crits
        crits = 0
        flag = ''
        while_total = roll_results['Regular Crit'] + roll_results['Hunger Crit']
        while while_total > 0:
            if roll_results['Regular Crit'] + roll_results['Hunger Crit'] > 2:
                if roll_results['Regular Crit'] >= 2:
                    crits += 4
                    roll_results['Regular Crit'] -= 2

                elif roll_results['Hunger Crit'] >= 2:
                    crits += 4
                    flag = 'Messy Crit'
                    roll_results['Hunger Crit'] -= 2

                elif roll_results['Regular Crit'] + roll_results['Hunger Crit'] >= 2:
                    crits += 4
                    flag = 'Messy Crit'
                    break
            else:
                break
            while_total -= 1

        crits += roll_results['Hunger Crit'] + roll_results['Regular Crit']
        total_successes = int(roll_results['Regular Success'] + roll_results['Hunger Success'] + crits)

        DIFFICULTY = ROLL_DICT['Difficulty']

        if total_successes >= DIFFICULTY and flag == '':
            flag = 'Regular Success'
        elif total_successes <= DIFFICULTY and flag == '':
            flag = 'Regular Fail'

        if WILLPOWER_DICT['Base Willpower'] <= WILLPOWER_DICT['Aggravated Willpower Damage']:
            button.disabled = True
            button.label = 'Fate Sealed'
            await interaction.response.edit_message(view=vp.EMPTY_VIEW(self.CLIENT))
            return
        elif WILLPOWER_DICT['Base Willpower'] <= WILLPOWER_DICT['Superficial Willpower Damage']:
            await CHARACTER.__update_value__('Aggravated Willpower Damage', int(WILLPOWER_DICT['Aggravated Willpower Damage']+1), 'willpower')
        else:
            await CHARACTER.__update_value__('Superficial Willpower Damage', int(WILLPOWER_DICT['Superficial Willpower Damage']+1), 'willpower')

        button.disabled = True
        button.label = 'Fate Tempted'

        # Assigns Information
        page.add_field(name='Roll Result:', value=f'{total_successes} | {flag}')
        log.crit(f'{total_successes=} | {crits=} | {DIFFICULTY=}')

        page: discord.Embed = await vp.standard_roller_page_modifications(page, CHARACTER)
        await interaction.response.edit_message(embed=page, view=vp.EMPTY_VIEW(self.CLIENT))
        return
