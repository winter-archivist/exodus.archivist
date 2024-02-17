import os
import json
import discord
from zenlog import log
import discord.ext

import misc.config.main_config as mc

import cogs.vtm_toolbox.vtb_characters.vtb_character_manager as cm
import cogs.vtm_toolbox.vtb_misc.vtb_utils as vu
import cogs.vtm_toolbox.vtb_misc.vtb_pages as vp


class VTM_Toolbox(discord.ext.commands.Cog):
    def __init__(self, CLIENT):
        self.CLIENT = CLIENT

    @discord.app_commands.command(name='VTM-Toolbox', description='---DO-NOT-TOUCH---')
    @discord.app_commands.describe(character_name='Character Name')
    @discord.app_commands.describe(make='--DEVTOOL--')
    @discord.app_commands.choices(target_tool=[discord.app_commands.Choice(name="Vampire Tracker", value="tracker"),
                                               discord.app_commands.Choice(name="Vampire Roller", value="roller")])
    async def Toolbox(self, interaction: discord.Interaction, character_name: str,
                      target_tool: discord.app_commands.Choice[str], make: bool = False):

        if interaction.user.id != mc.RUNNER_ID:
            log.crit(f'{interaction.user.name} used the no touch.')
            dev_test_embed = discord.Embed(title='NO TOUCH!', description='NO TOUCH!', color=mc.EMBED_COLORS['red'])
            await interaction.response.send_message(embed=dev_test_embed)
            return

        if make:
            await cm.make_character_files(interaction, character_name)

        await vu.reset_character_roll_information(interaction, character_name)
        await vu.write_character_name(interaction, character_name)

        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)

        page: discord.Embed = await vu.basic_page_builder(interaction, 'TEST TITLE', 'TEST DESCRIPTION', 'cyan')
        if target_tool == 'tracker':
            page.add_field(name='TRACKER', value='', inline=True)
            await interaction.response.send_message(embed=page, view=cm.vtb_DEV_TEST_VIEW(self.CLIENT))
        elif target_tool == 'roller':
            page.add_field(name='ROLLER', value=f'', inline=True)
            await interaction.response.send_message(embed=page, view=cm.vtb_DEV_TEST_VIEW(self.CLIENT))
        return


async def setup(CLIENT):
    await CLIENT.add_cog(VTM_Toolbox(CLIENT))
