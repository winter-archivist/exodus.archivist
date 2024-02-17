import os
import json
import discord
from zenlog import log
import discord.ext

from misc.config import mainConfig as mC

import cogs.vtm_toolbox.vtb_characters.vtb_character_manager as cm
import cogs.vtm_toolbox.vtb_misc.vtb_utils as vu


class VampireRoll(discord.ext.commands.Cog):
    def __init__(self, CLIENT):
        self.CLIENT = CLIENT

    @discord.app_commands.command(name='dev-test', description='---DO NOT TOUCH---')
    @discord.app_commands.describe(character_name='Character Name')
    @discord.app_commands.describe(make='Make New Files')
    async def DevTestNEWROLLER(self, interaction: discord.Interaction, character_name: str, make: bool = False):

        if interaction.user.id != mC.RUNNER_ID:
            log.crit(f'{interaction.user.name} used the no touch.')
            dev_test_embed = discord.Embed(title='NO TOUCH!', description='NO TOUCH!', color=mC.EMBED_COLORS['red'])
            await interaction.response.send_message(embed=dev_test_embed)
            return

        if make:
            await cm.make_character_files(interaction, character_name)

        await vu.reset_character_roll_information(interaction, character_name)
        await vu.write_character_name(interaction, character_name)

        character_class = cm.vtb_Character(interaction)

        dev_test_embed = discord.Embed(title='`!__DEV__DEBUG__TESTS__!`', description='`!__ONLY__PRESS__THINGS__IF__INSTRUCTED__!`', color=mC.EMBED_COLORS['red'])
        dev_test_embed.add_field(name='Char Name', value=f'{character_class.CHARACTER_NAME}', inline=True)
        dev_test_embed.add_field(name='Char Owner ID', value=f'{character_class.OWNER_ID}', inline=True)
        dev_test_embed.add_field(name='Interactor ID', value=f'{interaction.user.id}', inline=True)

        await interaction.response.send_message(embed=dev_test_embed, view=cm.vtb_DEV_TEST_VIEW(self.CLIENT))


async def setup(CLIENT):
    await CLIENT.add_cog(VampireRoll(CLIENT))
