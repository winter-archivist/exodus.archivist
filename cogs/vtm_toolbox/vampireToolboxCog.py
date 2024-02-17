import os
import json
import sqlite3
import discord
from zenlog import log
from discord.ext import commands
from discord import Embed, app_commands

from misc.config import mainConfig as mC

import cogs.vtm_toolbox.vtb_characters.vtb_character_manager as vtb_cm

import cogs.vtm_toolbox.vtb_misc.vtbUtils as vU
import cogs.vtm_toolbox.vtb_misc.vtbPageSystem as vPS


class VampireRoll(commands.Cog):
    def __init__(self, CLIENT):
        self.CLIENT = CLIENT

    @app_commands.command(name='dev-test', description='---DO NOT TOUCH---')
    @app_commands.describe(character_name='Character Name')
    @app_commands.describe(make='Make New Files')
    async def DevTestNEWTRACKER(self, interaction: discord.Interaction, character_name: str, make: bool = False):

        if interaction.user.id != mC.RUNNER_ID:
            log.crit(f'{interaction.user.name} used the no touch.')
            dev_test_embed = discord.Embed(title='NO TOUCH!', description='NO TOUCH!', color=mC.EMBED_COLORS['red'])
            await interaction.response.send_message(embed=dev_test_embed)
            return

        if make:
            await vtb_cm.make_character_files(interaction, character_name)

        CHARACTER_NAME_FILE: str = f'cogs/vtm_toolbox/vtb_characters/{interaction.user.id}/target_character.json'
        CHARACTER_NAME_DICT: dict = {'character_name': character_name}
        with open(CHARACTER_NAME_FILE, "w") as operate_file:
            json.dump(CHARACTER_NAME_DICT, operate_file)

        character_class = vtb_cm.vtb_Character(interaction)

        dev_test_embed = discord.Embed(title='`!__DEV__DEBUG__TESTS__!`', description='`!__ONLY__PRESS__THINGS__IF__INSTRUCTED__!`', color=mC.EMBED_COLORS['red'])
        dev_test_embed.add_field(name='Char Name', value=f'{character_class.CHARACTER_NAME}', inline=True)
        dev_test_embed.add_field(name='Char Owner ID', value=f'{character_class.OWNER_ID}', inline=True)
        dev_test_embed.add_field(name='Interactor ID', value=f'{interaction.user.id}', inline=True)

        await interaction.response.send_message(embed=dev_test_embed, view=vtb_cm.vtb_DEV_TEST_VIEW(self.CLIENT))


async def setup(CLIENT):
    await CLIENT.add_cog(VampireRoll(CLIENT))
