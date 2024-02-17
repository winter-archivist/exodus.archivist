import discord
import json

import misc.config.main_config as mc
import cogs.vtm_toolbox.vtb_characters.vtb_character_manager as cm


async def reset_character_roll_information(interaction: discord.Interaction, character_name):
    ROLL_DICT: dict = {'difficulty'           : 0,
                       'pool'                 : 0,
                       'result'               : '',
                       'composition'          : (),
                       'regular_crit_count'   : 0,
                       'regular_success_count': 0,
                       'regular_fail_count'   : 0,
                       'hunger_crit_count'    : 0,
                       'hunger_success_count' : 0,
                       'hunger_fail_count'    : 0,
                       'skull_count'          : 0}
    ROLL_FILE_DIRECTORY: str = f'cogs/vtm_toolbox/vtb_characters/{interaction.user.id}/{character_name}/roll/info.json'
    with open(ROLL_FILE_DIRECTORY, "w") as operate_file:
        json.dump(ROLL_DICT, operate_file)


async def write_character_name(interaction: discord.Interaction, character_name):
    CHARACTER_NAME_FILE: str = f'cogs/vtm_toolbox/vtb_characters/{interaction.user.id}/target_character.json'
    CHARACTER_NAME_DICT: dict = {'character_name': character_name}
    with open(CHARACTER_NAME_FILE, "w") as operate_file:
        json.dump(CHARACTER_NAME_DICT, operate_file)
