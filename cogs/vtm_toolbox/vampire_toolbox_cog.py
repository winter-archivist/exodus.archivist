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
import cogs.vtm_toolbox.vtm_cm.sections.vtb_list as vl
from cogs.vtm_toolbox.vtm_cm.sections.vtb_list import vtb_Book

class VTM_Toolbox(discord.ext.commands.Cog):
    def __init__(self, CLIENT):
        self.CLIENT = CLIENT
        self.vrf1_role_id: int = 1396813043622740069

    @discord.app_commands.command(name='vtm-toolbox', description='Toolbox for VTM!')
    @discord.app_commands.describe(character_name='Character Name')
    @discord.app_commands.choices(target_tool=[
        discord.app_commands.Choice(name="Tracker", value="tracker"),
        discord.app_commands.Choice(name="Roller", value="roller"),
        discord.app_commands.Choice(name="Character List", value="list"),
        discord.app_commands.Choice(name="[VRF1] Make Empty Kindred", value="make_empty")])
    async def Toolbox(self, interaction: discord.Interaction, character_name: str, target_tool: discord.app_commands.Choice[str]):

        # Updates target_character.json (stored in the uid folder)
        try:
            CHARACTER_NAME_FILE: str = f'cogs/vtm_toolbox/vtb_characters/{interaction.user.id}/target_character.json'
            CHARACTER_NAME_DICT: dict = {'character_name': character_name}
            with open(CHARACTER_NAME_FILE, "w") as operate_file:
                json.dump(CHARACTER_NAME_DICT, operate_file)
        except FileNotFoundError:
            page: discord.Embed = discord.Embed(title='Target Character File Not Found.', description='', colour=mc.EMBED_COLORS['red'])
            page.set_footer(text=f'{interaction.user.id}', icon_url=f'{interaction.user.display_avatar}')
            page.set_author(name=f'{interaction.user.name}', icon_url=f'{interaction.user.display_avatar}')
            await interaction.response.send_message(embed=page)
            return

        match target_tool.value:
            case 'tracker':
                CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
                page: discord.Embed = await vp.basic_page_builder(CHARACTER, 'Home', '', 'mint')
                await interaction.response.send_message(embed=page, view=vt.Home(self.CLIENT))
                return

            case 'roller':
                CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
                # Resets the currently stored Roll information for given character.
                try:
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
                except FileNotFoundError:
                    page: discord.Embed = discord.Embed(title='Character File Not Found.', description='',
                                                        colour=mc.EMBED_COLORS['red'])
                    page.set_footer(text=f'{interaction.user.id}', icon_url=f'{interaction.user.display_avatar}')
                    page.set_author(name=f'{interaction.user.name}', icon_url=f'{interaction.user.display_avatar}')
                    await interaction.response.send_message(embed=page)
                    return

                page: discord.Embed = await vp.basic_page_builder(CHARACTER, 'Home', '', 'purple')
                page: discord.Embed = await vp.standard_roller_page_modifications(page, CHARACTER)
                await interaction.response.send_message(embed=page, view=vr.Home(self.CLIENT))
                return

            case 'list':
                BOOK = vl.vtb_Book(interaction, self.CLIENT)
                await BOOK.__write_pages__(interaction)
                await interaction.response.send_message(embed=BOOK.PAGES[0], view=vl.PAGE_VIEW(self.CLIENT, BOOK))
                return

            case 'make_empty':

                # Verifies that the user has VRF1
                try:
                    if interaction.user.get_role(self.vrf1_role_id).name == 'VRF1':
                        log.warn(f'> {interaction.user.name} | {interaction.user.id} passed VTB-Make-Empty verification')
                except AttributeError as e:
                    log.warn(f'> {interaction.user.name} | {interaction.user.id} attempted to use VTB-Make-Empty without verification')
                    lacking_verification_page: discord.Embed = discord.Embed(title='VTB-Make-Empty', description='Lacking Verification', colour=mc.EMBED_COLORS[f"red"])
                    lacking_verification_page.set_footer(text=f'{interaction.user.id}', icon_url=f'{interaction.user.display_avatar}')
                    lacking_verification_page.set_author(name=f'{interaction.user.name}', icon_url=f'{interaction.user.display_avatar}')
                    await interaction.response.send_message(embed=lacking_verification_page, ephemeral=True)
                    return
                except Exception as e:
                    log.crit(f'> VTB-Make-Empty Verification Error: {e}')
                    failed_verification_page: discord.Embed = discord.Embed(title='VTB-Make-Empty', description='Verification Failed for Unknown Reasons', colour=mc.EMBED_COLORS[f"red"])
                    failed_verification_page.set_footer(text=f'{interaction.user.id}', icon_url=f'{interaction.user.display_avatar}')
                    failed_verification_page.set_author(name=f'{interaction.user.name}', icon_url=f'{interaction.user.display_avatar}')
                    await interaction.response.send_message(embed=failed_verification_page, ephemeral=True)
                    return

                # Creates Empty Character
                try:
                    await cm.make_blank_character_files(interaction, character_name)
                    log.info(f'> {interaction.user.name} | {interaction.user.id} made {character_name}.')
                    successful_creation_page: discord.Embed = discord.Embed(title='VTB-Make-Empty', description='Successful Creation', colour=mc.EMBED_COLORS[f"mint"])
                    successful_creation_page.set_footer(text=f'{interaction.user.id}', icon_url=f'{interaction.user.display_avatar}')
                    successful_creation_page.set_author(name=f'{interaction.user.name}', icon_url=f'{interaction.user.display_avatar}')
                    successful_creation_page.add_field(name='Character Name', value=f'{character_name}', inline=False)
                    await interaction.response.send_message(embed=successful_creation_page)
                    return
                except FileExistsError as e:
                    log.warn(f'> VTB-Make-Empty Creation Error, Files Already Exist: {e}')
                    failed_creation_page: discord.Embed = discord.Embed(title='VTB-Make-Empty', description='Creation Failed due to character already existing', colour=mc.EMBED_COLORS[f"red"])
                    failed_creation_page.set_footer(text=f'{interaction.user.id}', icon_url=f'{interaction.user.display_avatar}')
                    failed_creation_page.set_author(name=f'{interaction.user.name}', icon_url=f'{interaction.user.display_avatar}')
                    failed_creation_page.add_field(name='Character Name', value=f'{character_name}', inline=False)
                    await interaction.response.send_message(embed=failed_creation_page, ephemeral=True)
                    return
                except Exception as e:
                    log.warn(f'> VTB-Make-Empty Creation Error: {e}')
                    failed_creation_page: discord.Embed = discord.Embed(title='VTB-Make-Empty', description='Creation Failed for Unknown Reasons', colour=mc.EMBED_COLORS[f"red"])
                    failed_creation_page.set_footer(text=f'{interaction.user.id}', icon_url=f'{interaction.user.display_avatar}')
                    failed_creation_page.set_author(name=f'{interaction.user.name}', icon_url=f'{interaction.user.display_avatar}')
                    failed_creation_page.add_field(name='Character Name', value=f'{character_name}', inline=False)
                    await interaction.response.send_message(embed=failed_creation_page, ephemeral=True)
                    return

                log.crit('> VTB-Make-Empty | How Did We Get Here?')
                return

            case _:
                log.error('**> Unknown target_tool.value given to Toolbox()')
                raise ValueError


async def setup(CLIENT):
    await CLIENT.add_cog(VTM_Toolbox(CLIENT))
    log.info('> VTM Toolbox Setup Complete.')


async def teardown(CLIENT):
    await CLIENT.add_cog(VTM_Toolbox(CLIENT))
    log.info(f'> VTM Toolbox Teardown Complete')
