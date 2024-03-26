import os
import json
import discord
from zenlog import log
import discord.ext

import misc.config.main_config as mc

import cogs.vtm_toolbox.vtm_cm.vtb_character_manager as cm
import cogs.vtm_toolbox.vtb_pages as vp
import cogs.vtm_toolbox.vtm_cm.sections.vtb_roller as vr
import cogs.vtm_toolbox.vtm_cm.sections.vtb_tracker as vt


class VTM_Toolbox(discord.ext.commands.Cog):
    def __init__(self, CLIENT):
        self.CLIENT = CLIENT

    @discord.app_commands.command(name='vtm-toolbox', description='Toolbox for VTM!')
    @discord.app_commands.describe(character_name='Character Name')
    @discord.app_commands.choices(target_tool=[discord.app_commands.Choice(name="Vampire Tracker", value="tracker"),
                                               discord.app_commands.Choice(name="Vampire Roller", value="roller")])
    @discord.app_commands.choices(make=[discord.app_commands.Choice(name="True", value='True'),
                                        discord.app_commands.Choice(name="False [Default]", value='False')])
    async def Toolbox(self, interaction: discord.Interaction,
                      character_name: str, target_tool: discord.app_commands.Choice[str], make: str = 'False'):

        if interaction.user.id != mc.RUNNER_ID and make != 'False':
            log.crit(f'> {interaction.user.name} | {interaction.user.id}  used the no touch.')
            rando_used_devtool = discord.Embed(title='NO TOUCH!', description='The `make` option was selected, this is a devtool'
                                                                              ', do __not__ touch.', color=mc.EMBED_COLORS['red'])
            await interaction.response.send_message(embed=rando_used_devtool)
            return
        elif interaction.user.id == mc.RUNNER_ID and make == 'True':
            log.crit(f'> {interaction.user.name} | {interaction.user.id} made {character_name}.')
            await cm.make_character_files(interaction, character_name)

        ROLL_DICT: dict = {'Difficulty'           : 0,
                           'Pool'                 : 0,
                           'Result'               : '',
                           'Composition'          : 'Base[0]',

                           # These are NOT a dict as to make it friendlier
                           # with vtb_Character.__update_information__()
                           'Regular Success Count': 0,
                           'Regular Fail Count'   : 0,
                           'Hunger Crit Count'    : 0,
                           'Hunger Success Count' : 0,
                           'Hunger Fail Count'    : 0,
                           'Skull Count'          : 0}
        ROLL_FILE_DIRECTORY: str = f'cogs/vtm_toolbox/vtb_characters/{interaction.user.id}/{character_name}/roll/info.json'
        with open(ROLL_FILE_DIRECTORY, "w") as operate_file:
            json.dump(ROLL_DICT, operate_file)

        CHARACTER_NAME_FILE: str = f'cogs/vtm_toolbox/vtb_characters/{interaction.user.id}/target_character.json'
        CHARACTER_NAME_DICT: dict = {'character_name': character_name}
        with open(CHARACTER_NAME_FILE, "w") as operate_file:
            json.dump(CHARACTER_NAME_DICT, operate_file)

        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)

        if target_tool.value == 'tracker':
            page: discord.Embed = await vp.basic_page_builder(CHARACTER, 'Home', '', 'mint')
            await interaction.response.send_message(embed=page, view=vt.Home(self.CLIENT))

        elif target_tool.value == 'roller':
            page: discord.Embed = await vp.basic_page_builder(CHARACTER, 'Home', '', 'purple')
            page: discord.Embed = await vp.standard_roller_page_modifications(page, CHARACTER)
            await interaction.response.send_message(embed=page, view=vr.Home(self.CLIENT))
        else:
            log.error('**> Unknown target_tool.value given to Toolbox()')
            raise ValueError

        return


async def setup(CLIENT):
    await CLIENT.add_cog(VTM_Toolbox(CLIENT))
