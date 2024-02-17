import os
import json
import random
import discord
import discord.ui
from zenlog import log

import misc.config.main_config as mc

import cogs.vtm_toolbox.vtb_misc.vtb_utils as vu
import cogs.vtm_toolbox.vtb_characters.vtb_character_manager as cm


class Vampire_Tracker(discord.ui.View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Vampire Tracker', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.gray, row=1)
    async def home_button_callback(self, interaction, button):
        character: cm.vtb_Character = cm.vtb_Character(interaction)
        page = await vu.basic_page_builder(interaction, 'HP/WP', '', '')

        character
