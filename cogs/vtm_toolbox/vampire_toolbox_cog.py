import os
import json
import discord
from zenlog import log
import discord.ext

import misc.config.main_config as mc

import cogs.vtm_toolbox.vtm_cm.vtb_character_manager as cm
import cogs.vtm_toolbox.vtm_cm.vtb_pages as vp
import cogs.vtm_toolbox.vtm_cm.sections.vtb_roller as vr
import cogs.vtm_toolbox.vtm_cm.sections.vtb_tracker as vt


class VTM_Toolbox(discord.ext.commands.Cog):
    def __init__(self, CLIENT):
        self.CLIENT = CLIENT

    @discord.app_commands.command(name='vtm-toolbox', description='Toolbox for VTM!')
    @discord.app_commands.describe(character_name='Character Name')
    @discord.app_commands.choices(target_tool=[discord.app_commands.Choice(name="Vampire Tracker", value="tracker"),
                                               discord.app_commands.Choice(name="Vampire Roller", value="roller")])
    async def Toolbox(self, interaction: discord.Interaction, character_name: str, target_tool: discord.app_commands.Choice[str]):
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

    @discord.app_commands.command(name='vtb-make', description='[ADMIN]')
    @discord.app_commands.describe(character_name='Character Name')
    async def Make(self, interaction: discord.Interaction, character_name: str):
        if interaction.user.id == mc.RUNNER_ID:
            try:
                await cm.make_blank_character_files(interaction, character_name)
                log.crit(f'> {interaction.user.name} | {interaction.user.id} made {character_name}.')
                page: discord.Embed = discord.Embed(title='VTB-Make', description='Successful Creation', colour=mc.EMBED_COLORS[f"mint"])
            except Exception as e:
                log.crit(f'*> {interaction.user.name} | {interaction.user.id} failed at making {character_name}.')
                log.crit(f'*> Make Error: {e}')
                page: discord.Embed = discord.Embed(title='VTB-Make', description='Failed Creation', colour=mc.EMBED_COLORS[f"red"])
                page.add_field(name='Encountered Error', value=f'{e}', inline=False)

            page.set_footer(text=f'{interaction.user.id}', icon_url=f'{interaction.user.display_avatar}')
            page.set_author(name=f'{interaction.user.name}', icon_url=f'{interaction.user.display_avatar}')
            page.add_field(name='Character Name', value=f'{character_name}', inline=False)
        else:
            page: discord.Embed = discord.Embed(title='VTB-Make', description='Failed', colour=mc.EMBED_COLORS[f"red"])
            page.add_field(name='Uncounted Error', value=f'Non-Admin User-ID Provided', inline=False)

        await interaction.response.send_message(embed=page)
        return


async def setup(CLIENT):
    await CLIENT.add_cog(VTM_Toolbox(CLIENT))
