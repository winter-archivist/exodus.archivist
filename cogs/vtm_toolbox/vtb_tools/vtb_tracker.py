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


class Home(discord.ui.View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Attributes', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.gray, row=0)
    async def attributes_button_callback(self, interaction, button):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.basic_page_builder(interaction, 'Attribute Page', '', 'dark_yellow')
        attributes: tuple = \
            ('strength', 'dexterity', 'stamina', 'charisma', 'manipulation', 'composure', 'intelligence', 'wits', 'resolve')
        character_data: dict = await CHARACTER.__get_information__(attributes, 'attributes')

        emoji_result = f'{character_data["strength"] * mc.DOT_FULL_EMOJI} {abs(character_data["strength"] - 5) * mc.DOT_EMPTY_EMOJI}'
        page.add_field(name='Strength', value=emoji_result, inline=True)

        emoji_result = f'{character_data["dexterity"] * mc.DOT_FULL_EMOJI} {abs(character_data["dexterity"] - 5) * mc.DOT_EMPTY_EMOJI}'
        page.add_field(name='Dexterity', value=emoji_result, inline=True)

        emoji_result = f'{character_data["stamina"] * mc.DOT_FULL_EMOJI} {abs(character_data["stamina"] - 5) * mc.DOT_EMPTY_EMOJI}'
        page.add_field(name='Stamina', value=emoji_result, inline=True)

        page.add_field(name='', value='', inline=False)

        emoji_result = f'{character_data["charisma"] * mc.DOT_FULL_EMOJI} {abs(character_data["charisma"] - 5) * mc.DOT_EMPTY_EMOJI}'
        page.add_field(name='Charisma', value=emoji_result, inline=True)

        emoji_result = f'{character_data["manipulation"] * mc.DOT_FULL_EMOJI} {abs(character_data["manipulation"] - 5) * mc.DOT_EMPTY_EMOJI}'
        page.add_field(name='Manipulation', value=emoji_result, inline=True)

        emoji_result = f'{character_data["composure"] * mc.DOT_FULL_EMOJI} {abs(character_data["composure"] - 5) * mc.DOT_EMPTY_EMOJI}'
        page.add_field(name='Composure', value=emoji_result, inline=True)

        page.add_field(name='', value='', inline=False)

        emoji_result = f'{character_data["intelligence"] * mc.DOT_FULL_EMOJI} {abs(character_data["intelligence"] - 5) * mc.DOT_EMPTY_EMOJI}'
        page.add_field(name='Intelligence', value=emoji_result, inline=True)

        emoji_result = f'{character_data["wits"] * mc.DOT_FULL_EMOJI} {abs(character_data["wits"] - 5) * mc.DOT_EMPTY_EMOJI}'
        page.add_field(name='Wits', value=emoji_result, inline=True)

        emoji_result = f'{character_data["resolve"] * mc.DOT_FULL_EMOJI} {abs(character_data["resolve"] - 5) * mc.DOT_EMPTY_EMOJI}'
        page.add_field(name='Resolve', value=emoji_result, inline=True)

        await interaction.response.send_message(embed=page, view=Attributes(self.CLIENT))


class Attributes(discord.ui.View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Home', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.gray, row=1)
    async def home_button_callback(self, interaction, button):
        character: cm.vtb_Character = cm.vtb_Character(interaction)
        page = await vp.basic_page_builder(interaction, 'Home', '', 'dark_yellow')
        character = cm.vtb_Character(interaction)
        await interaction.response.send_message(embed=page, view=Home(self.CLIENT))
