import discord
import json

import misc.config.main_config as mc
import cogs.vtm_toolbox.vtb_characters.vtb_character_manager as cm


async def reset_character_roll_information(interaction: discord.Interaction, character_name):
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


async def write_character_name(interaction: discord.Interaction, character_name):
    CHARACTER_NAME_FILE: str = f'cogs/vtm_toolbox/vtb_characters/{interaction.user.id}/target_character.json'
    CHARACTER_NAME_DICT: dict = {'character_name': character_name}
    with open(CHARACTER_NAME_FILE, "w") as operate_file:
        json.dump(CHARACTER_NAME_DICT, operate_file)
