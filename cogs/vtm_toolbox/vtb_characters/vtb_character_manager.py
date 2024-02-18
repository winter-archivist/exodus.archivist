import os
import json
import random
import discord
from zenlog import log

from misc.config import main_config as mc


async def make_character_files(interaction: discord.Interaction, character_name):
    CHARACTER_DIRECTORY: str = f'cogs/vtm_toolbox/vtb_characters/{interaction.user.id}/{character_name}/'

    os.mkdir(f'cogs/vtm_toolbox/vtb_characters/{interaction.user.id}')
    os.mkdir(f'{CHARACTER_DIRECTORY}')
    os.mkdir(f'{CHARACTER_DIRECTORY}skills')
    os.mkdir(f'{CHARACTER_DIRECTORY}roll')

    MISC_DICT: dict = {'owner_id'            : interaction.user.id,
                       'character_name'      : character_name,
                       'blood_potency'       : 0,
                       'clan'                : 'UNSET',
                       'generation'          : 0,
                       'humanity'            : 0,
                       'bane_severity'       : 0,
                       'hunger'              : 0,
                       'predator_type'       : 'UNSET',
                       'character_avatar_url': mc.PLACEHOLDER_IMG}
    HEALTH_DICT: dict = {'base_health'              : 0,
                         'superficial_health_damage': 0,
                         'aggravated_health_damage' : 0}
    WILLPOWER_DICT: dict = {'base_willpower'              : 0,
                            'superficial_willpower_damage': 0,
                            'aggravated_willpower_damage' : 0}
    ATTRIBUTES_DICT: dict = {'strength'    : 0,
                             'dexterity'   : 0,
                             'stamina'     : 0,
                             'charisma'    : 0,
                             'manipulation': 0,
                             'composure'   : 0,
                             'intelligence': 0,
                             'wits'        : 0,
                             'resolve'     : 0}
    DISCIPLINES_DICT: dict = {'obfuscate'          : 0,
                              'animalism'          : 0,
                              'potence'            : 0,
                              'dominate'           : 0,
                              'auspex'             : 0,
                              'protean'            : 0,
                              'presence'           : 0,
                              'fortitude'          : 0,
                              'thin_blood_alchemy' : 0,
                              'blood_sorcery'      : 0,
                              'chemeristry'        : 0,
                              'seven_specific'     : 0,
                              'myr_specific'       : 0,
                              'selena_specific'    : 0,
                              'nyctea_specific_one': 0,
                              'nyctea_specific_two': 0,
                              'elijah_specific'    : 0}
    PHYSICAL_SKILLS_DICT: dict = {'athletics': 0,
                                  'brawl'    : 0,
                                  'craft'    : 0,
                                  'drive'    : 0,
                                  'firearms' : 0,
                                  'larceny'  : 0,
                                  'melee'    : 0,
                                  'stealth'  : 0,
                                  'survival' : 0}
    SOCIAL_SKILLS_DICT: dict = {'animal_ken'  : 0,
                                'etiquette'   : 0,
                                'insight'     : 0,
                                'intimidation': 0,
                                'leadership'  : 0,
                                'performance' : 0,
                                'persuasion'  : 0,
                                'streetwise'  : 0,
                                'subterfuge'  : 0}
    MENTAL_SKILLS_DICT: dict = {'academics'    : 0,
                                'awareness'    : 0,
                                'finance'      : 0,
                                'investigation': 0,
                                'medicine'     : 0,
                                'occult'       : 0,
                                'politics'     : 0,
                                'science'      : 0,
                                'technology'   : 0}
    ROLL_DICT: dict = {'difficulty': 0,
                       'pool' : 0,
                       'result': '',
                       'composition': 'Base[0]',
                       'regular_crit_count': 0,
                       'regular_success_count': 0,
                       'regular_fail_count': 0,
                       'hunger_crit_count': 0,
                       'hunger_success_count' : 0,
                       'hunger_fail_count' : 0,
                       'skull_count': 0}

    with open(f'{CHARACTER_DIRECTORY}misc.json', "w") as operate_file:
        json.dump(MISC_DICT, operate_file)

    with open(f'{CHARACTER_DIRECTORY}health.json', "w") as operate_file:
        json.dump(HEALTH_DICT, operate_file)

    with open(f'{CHARACTER_DIRECTORY}willpower.json', "w") as operate_file:
        json.dump(WILLPOWER_DICT, operate_file)

    with open(f'{CHARACTER_DIRECTORY}attributes.json', "w") as operate_file:
        json.dump(ATTRIBUTES_DICT, operate_file)

    with open(f'{CHARACTER_DIRECTORY}disciplines.json', "w") as operate_file:
        json.dump(DISCIPLINES_DICT, operate_file)

    with open(f'{CHARACTER_DIRECTORY}skills/physical.json', "w") as operate_file:
        json.dump(PHYSICAL_SKILLS_DICT, operate_file)

    with open(f'{CHARACTER_DIRECTORY}skills/social.json', "w") as operate_file:
        json.dump(SOCIAL_SKILLS_DICT, operate_file)

    with open(f'{CHARACTER_DIRECTORY}skills/mental.json', "w") as operate_file:
        json.dump(MENTAL_SKILLS_DICT, operate_file)

    with open(f'{CHARACTER_DIRECTORY}roll/info.json', "w") as operate_file:
        json.dump(ROLL_DICT, operate_file)


class vtb_Character:
    def __init__(self, interaction: discord.Interaction):
        CHARACTER_NAME_FILE: str = f'cogs/vtm_toolbox/vtb_characters/{interaction.user.id}/target_character.json'
        with open(CHARACTER_NAME_FILE, 'r') as operate_file:
            CHARACTER_NAME = json.load(operate_file)['character_name']

        self.CHARACTER_NAME: str = CHARACTER_NAME

        self.CHARACTER_FILE_PATH: str = f'cogs/vtm_toolbox/vtb_characters/{interaction.user.id}/{self.CHARACTER_NAME}'

        if not os.path.isdir(self.CHARACTER_FILE_PATH):
            # This just means the interactor doesn't have any character with the given name.
            raise FileNotFoundError

        with open(f'{self.CHARACTER_FILE_PATH}/misc.json', 'r') as operate_file:
            CHARACTER_INFO = json.load(operate_file)

        if int(CHARACTER_INFO['owner_id']) == interaction.user.id:
            self.OWNER_ID = interaction.user.id
        else:
            log.error('*> Bad Character Owner')
            raise Exception('Bad Character Owner')

    async def __get_information__(self, WANTED_INFORMATION: tuple, FILE_NAME: str) -> dict:
        with open(f'{self.CHARACTER_FILE_PATH}/{FILE_NAME}.json', 'r') as operate_file:
            CHARACTER_INFO: dict = json.load(operate_file)

        return_information: dict = {}
        loop_counter: int = 0
        for x in WANTED_INFORMATION:
            return_information[f'{WANTED_INFORMATION[loop_counter]}'] = CHARACTER_INFO[f'{WANTED_INFORMATION[loop_counter]}']
            loop_counter += 1

        log.debug(f'{self.OWNER_ID} __get | {return_information}')
        return return_information

    async def __update_information__(self, NEW_INFORMATION: tuple, FILE_NAME: str) -> None:
        with open(f'{self.CHARACTER_FILE_PATH}/{FILE_NAME}.json', 'r') as operate_file:
            character_info: dict = json.load(operate_file)

        loop_counter: int = 0
        for x in NEW_INFORMATION[0]:
            dict_key = NEW_INFORMATION[0][loop_counter]
            new_value = NEW_INFORMATION[1][loop_counter]
            log.debug(f'{self.OWNER_ID} __update loop | {dict_key} -> {new_value}')
            character_info[dict_key] = new_value
            loop_counter += 1

        with open(f'{self.CHARACTER_FILE_PATH}/{FILE_NAME}.json', 'w') as operate_file:
            json.dump(character_info, operate_file)

    async def __rouse_check__(self) -> tuple:
        HUNGER: int = (await self.__get_information__(('hunger',), 'misc'))['hunger']
        ROUSE_NUM_RESULT: int = random.randint(1, 10)

        if HUNGER >= 5:
            result: tuple = ('Frenzy', HUNGER)
            return result  # Hunger Frenzy, No Hunger Gain Too High Already

        elif ROUSE_NUM_RESULT >= 6:
            result: tuple = ('Pass', HUNGER)
            return result  # No Hunger Gain

        elif ROUSE_NUM_RESULT <= 5:
            await self.__update_information__((('hunger',), (HUNGER+1,)), 'misc')
            result: tuple = ('Fail', HUNGER+1)
            return result  # 1 Hunger Gain
