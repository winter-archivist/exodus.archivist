import os
import json
import random
import discord
import discord.ui
from zenlog import log

import misc.config.main_config as mc

import cogs.vtm_toolbox.vtb_misc.vtb_utils as vu
import cogs.vtm_toolbox.vtb_misc.vtb_pages as vp
import cogs.vtm_toolbox.vtb_characters.vtb_character_manager as cm

import cogs.vtm_toolbox.vtb_tools.vtb_roller_options as ro


class Home(discord.ui.View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Roll Types', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.red, row=0)
    async def roll_button_callback(self, interaction: discord.Interaction, button: discord.ui.Select):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.basic_page_builder(interaction, 'Roll Types', '', 'dark_yellow')
        page: discord.Embed = await vp.standard_roller_page_modifications(page, CHARACTER)
        await interaction.response.edit_message(embed=page, view=RollTypes(self.CLIENT))
        return

    @discord.ui.button(label='Attributes', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.gray, row=0)
    async def attributes_button_callback(self, interaction, button):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.basic_page_builder(interaction, 'Attributes Page', '', 'dark_yellow')
        page: discord.Embed = await vp.standard_roller_page_modifications(page, CHARACTER)
        await interaction.response.send_message(embed=page, view=Attributes(self.CLIENT))
        return

    @discord.ui.button(label='Skills', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.gray, row=0)
    async def skills_button_callback(self, interaction, button):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.basic_page_builder(interaction, 'Skills Page', '', 'dark_yellow')
        page: discord.Embed = await vp.standard_roller_page_modifications(page, CHARACTER)
        await interaction.response.send_message(embed=page, view=Skills(self.CLIENT))
        return

    @discord.ui.button(label='Disciplines', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.gray, row=0)
    async def disciplines_button_callback(self, interaction, button):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.basic_page_builder(interaction, 'Disciplines Page', '', 'dark_yellow')
        page: discord.Embed = await vp.standard_roller_page_modifications(page, CHARACTER)
        await interaction.response.send_message(embed=page, view=Disciplines(self.CLIENT))
        return

    @discord.ui.button(label='Extras', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.gray, row=0)
    async def extras_button_callback(self, interaction, button):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.basic_page_builder(interaction, 'Extras Page', '', 'dark_yellow')
        page: discord.Embed = await vp.standard_roller_page_modifications(page, CHARACTER)
        await interaction.response.send_message(embed=page, view=Extras(self.CLIENT))
        return


class RollTypes(discord.ui.View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Home', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.gray, row=0)
    async def home_button_callback(self, interaction, button):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.basic_page_builder(interaction, 'Home', '', 'dark_yellow')
        page: discord.Embed = await vp.standard_roller_page_modifications(page, CHARACTER)
        await interaction.response.send_message(embed=page, view=Home(self.CLIENT))
        return

    @discord.ui.button(label='Blood Surge', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.red, row=0)
    async def blood_surge_button_callback(self, interaction, button):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.basic_page_builder(interaction, 'Roll Types', '', 'dark_yellow')

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

        ROLL_INFO: dict = await CHARACTER.__get_information__(('pool', 'composition'), 'roll/info')
        NEW_ROLL_POOL: int = int(ROLL_INFO['pool'])
        NEW_ROLL_COMPOSITION = f'{ROLL_INFO["composition"]}, Blood Surge[2]'

        await CHARACTER.__update_information__((('pool', 'composition'), (NEW_ROLL_POOL, NEW_ROLL_COMPOSITION)), 'roll/info')

        page: discord.Embed = await vp.standard_roller_page_modifications(page, CHARACTER)
        await interaction.response.send_message(embed=page, view=Home(self.CLIENT))
        return

    @discord.ui.select(placeholder='Select Difficulty', options=ro.difficulty_options, max_values=1, min_values=1, row=1)
    async def difficulty_select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.basic_page_builder(interaction, 'Home', '', 'dark_yellow')

        # Parenthesis on (select.values) are NOT redundant!!!
        await CHARACTER.__update_information__((('difficulty',), (select.values,)), 'roll/info')

        page: discord.Embed = await vp.standard_roller_page_modifications(page, CHARACTER)
        await interaction.response.edit_message(embed=page, view=Home(self.CLIENT))
        return

    @discord.ui.button(label='Standard Roll', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.red, row=2)
    async def roll_button_callback(self, interaction: discord.Interaction, button: discord.ui.Select):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.basic_page_builder(interaction, 'Standard Roll', '', 'dark_yellow')

        page: discord.Embed = await CHARACTER.__roll__(page)

        page: discord.Embed = await vp.standard_roller_page_modifications(page, CHARACTER)
        await interaction.response.edit_message(embed=page, view=vp.EMPTY_VIEW(self.CLIENT))
        return

    @discord.ui.button(label='Hunting Roll', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.red, row=2)
    async def hunt_button_callback(self, interaction, button):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.basic_page_builder(interaction, 'Roll', '', 'dark_yellow')

        page = await CHARACTER.__hunt__(page)

        page: discord.Embed = await vp.standard_roller_page_modifications(page, CHARACTER)
        await interaction.response.edit_message(embed=page, view=vp.EMPTY_VIEW(self.CLIENT))
        return


class Attributes(discord.ui.View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Home', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.gray, row=0)
    async def home_button_callback(self, interaction, button):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.basic_page_builder(interaction, 'Home', '', 'dark_yellow')
        page: discord.Embed = await vp.standard_roller_page_modifications(page, CHARACTER)
        await interaction.response.send_message(embed=page, view=Home(self.CLIENT))
        return

    @discord.ui.select(placeholder='Select Attribute(s)', options=ro.attribute_options, max_values=3, min_values=1, row=1)
    async def attribute_select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        page: discord.Embed = await vp.basic_page_builder(interaction, 'Attributes Page', '', 'dark_yellow')
        page = await vp.standard_roll_select(interaction, page, select, 'attributes')
        await interaction.response.edit_message(embed=page, view=Skills(self.CLIENT))
        return


class Skills(discord.ui.View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Home', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.gray, row=0)
    async def home_button_callback(self, interaction, button):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.basic_page_builder(interaction, 'Home', '', 'dark_yellow')
        page: discord.Embed = await vp.standard_roller_page_modifications(page, CHARACTER)
        await interaction.response.send_message(embed=page, view=Home(self.CLIENT))
        return

    @discord.ui.select(placeholder='Select Physical Skill(s)', options=ro.physical_skill_options, max_values=3, min_values=1, row=1)
    async def physical_select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        page: discord.Embed = await vp.basic_page_builder(interaction, 'Skills Page', '', 'dark_yellow')
        page = await vp.standard_roll_select(interaction, page, select, 'skills/physical')
        await interaction.response.edit_message(embed=page, view=Skills(self.CLIENT))
        return

    @discord.ui.select(placeholder='Select Social Skill(s)', options=ro.social_skill_options, max_values=3, min_values=1, row=2)
    async def social_select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        page: discord.Embed = await vp.basic_page_builder(interaction, 'Skills Page', '', 'dark_yellow')
        page = await vp.standard_roll_select(interaction, page, select, 'skills/social')
        await interaction.response.edit_message(embed=page, view=Skills(self.CLIENT))
        return

    @discord.ui.select(placeholder='Select Mental Skill(s)', options=ro.mental_skill_options, max_values=3, min_values=1, row=3)
    async def mental_select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        page: discord.Embed = await vp.basic_page_builder(interaction, 'Skills Page', '', 'dark_yellow')
        page = await vp.standard_roll_select(interaction, page, select, 'skills/mental')
        await interaction.response.edit_message(embed=page, view=Skills(self.CLIENT))
        return


class Disciplines(discord.ui.View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Home', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.gray, row=0)
    async def home_button_callback(self, interaction, button):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.basic_page_builder(interaction, 'Home', '', 'dark_yellow')
        page: discord.Embed = await vp.standard_roller_page_modifications(page, CHARACTER)
        await interaction.response.send_message(embed=page, view=Home(self.CLIENT))
        return

    @discord.ui.select(placeholder='Select Discipline(s)', options=ro.discipline_options, max_values=3, min_values=1, row=1)
    async def physical_select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        page: discord.Embed = await vp.basic_page_builder(interaction, 'Disciplines Page', '', 'dark_yellow')
        page = await vp.standard_roll_select(interaction, page, select, 'disciplines')
        await interaction.response.edit_message(embed=page, view=Disciplines(self.CLIENT))
        return


class Extras(discord.ui.View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Home', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.gray, row=0)
    async def home_button_callback(self, interaction, button):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.basic_page_builder(interaction, 'Home', '', 'dark_yellow')
        page: discord.Embed = await vp.standard_roller_page_modifications(page, CHARACTER)
        await interaction.response.send_message(embed=page, view=Home(self.CLIENT))
        return

    @discord.ui.select(placeholder='Extra Select', options=ro.extra_options, max_values=1, min_values=1, row=1)
    async def extra_select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        page: discord.Embed = await vp.basic_page_builder(interaction, 'Extras Page', '', 'dark_yellow')
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)

        CHARACTER_INFORMATION: dict = await CHARACTER.__get_information__(('pool', 'composition'), 'roll/info')
        pool: int = CHARACTER_INFORMATION['pool']
        composition: str = CHARACTER_INFORMATION['composition']

        pool += int(select.values[0])
        composition = f'{composition}, [{select.values[0]}]'

        await CHARACTER.__update_information__((('pool', 'composition'), (pool, composition)), 'roll/info')

        select.disabled = True

        page: discord.Embed = await vp.standard_roller_page_modifications(page, CHARACTER)
        await interaction.response.edit_message(embed=page, view=Extras(self.CLIENT))
        return
