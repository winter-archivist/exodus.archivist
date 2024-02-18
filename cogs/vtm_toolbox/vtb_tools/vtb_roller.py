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

    @discord.ui.button(label='Attributes', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.gray, row=0)
    async def attributes_button_callback(self, interaction, button):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.basic_page_builder(interaction, 'Attribute Page', '', 'dark_yellow')
        page: discord.Embed = await vp.standard_roller_page_modifications(page, CHARACTER)
        await interaction.response.send_message(embed=page, view=Attributes(self.CLIENT))
        return


class Attributes(discord.ui.View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Home', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.gray, row=0)
    async def home_button_callback(self, interaction, button):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page = await vp.basic_page_builder(interaction, 'Home', '', 'dark_yellow')
        page: discord.Embed = await vp.standard_roller_page_modifications(page, CHARACTER)
        await interaction.response.send_message(embed=page, view=Home(self.CLIENT))

    @discord.ui.select(placeholder='Select Attribute(s)', options=ro.attribute_options, max_values=3, min_values=1, row=1)
    async def attribute_select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.basic_page_builder(interaction, 'Attribute Page', '', 'dark_yellow')

        CHARACTER_INFORMATION: dict = await CHARACTER.__get_information__(('pool', 'composition'), 'roll/info')
        pool: int = CHARACTER_INFORMATION['pool']
        composition: str = CHARACTER_INFORMATION['composition']

        for_var = 0
        for selections in select.values:
            attribute_value: int = dict(await CHARACTER.__get_information__((f'{select.values[for_var]}',), 'attributes'))[
                select.values[for_var]]
            pool += attribute_value
            composition = f'{composition}, {(select.values[for_var]).capitalize()}[{attribute_value}]'
            for_var += 1

        await CHARACTER.__update_information__((('pool', 'composition'), (pool, composition)), 'roll/info')

        select.disabled = True

        page: discord.Embed = await vp.standard_roller_page_modifications(page, CHARACTER)
        await interaction.response.edit_message(embed=page, view=Attributes(self.CLIENT))
