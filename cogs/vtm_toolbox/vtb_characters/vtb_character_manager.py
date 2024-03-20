import os
import json
import random
import discord
from zenlog import log
from random import randint

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
                       'temperament'         : '',
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

                       # These are NOT a dict as to make it friendlier
                       # with vtb_Character.__update_information__()
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
            self.OWNER_NAME = interaction.user.name
            self.OWNER_ID = interaction.user.id
            self.OWNER_AVATAR = interaction.user.display_avatar
            log.debug(f'> vtbCM __init__ Verified Owner of {CHARACTER_NAME} |  {self.OWNER_NAME} | {self.OWNER_ID} |')
        else:
            log.error('*> Bad Character Owner')
            raise Exception('Bad Character Owner')

        self.AVATAR_URL: str = CHARACTER_INFO['character_avatar_url']

    # The get/update value/values functions are split since if you only need one value returned/updated
    # then there's no point in going through the for loop/using tuples, this just slightly increases performance;
    # not that this bot needs to be/is performant, especially being written in python by a newbie.
    async def __get_values__(self, KEYS: tuple, FILE_NAME: str) -> dict:
        # Use when getting more than one value, otherwise use self.__get_value__()

        with open(f'{self.CHARACTER_FILE_PATH}/{FILE_NAME}.json', 'r') as operate_file:
            CHARACTER_INFO: dict = json.load(operate_file)

        return_information: dict = {}
        loop_counter: int = 0
        for x in KEYS:
            return_information[f'{KEYS[loop_counter]}'] = CHARACTER_INFO[f'{KEYS[loop_counter]}']
            loop_counter += 1

        log.debug(f'{self.OWNER_ID} | {self.OWNER_NAME} | __get_vals | {return_information}')
        return return_information

    async def __get_value__(self, KEY: str, FILE_NAME: str):
        # Use when getting one value, otherwise use self.__get_values__()

        with open(f'{self.CHARACTER_FILE_PATH}/{FILE_NAME}.json', 'r') as operate_file:
            CHARACTER_INFO: dict = json.load(operate_file)

        RETURN_INFORMATION = CHARACTER_INFO[KEY]

        log.debug(f'{self.OWNER_ID} | {self.OWNER_NAME} |  __get_val | {RETURN_INFORMATION}')

        return RETURN_INFORMATION

    async def __update_values__(self, KEYS: tuple, VALUES: tuple, FILE_NAME: str) -> None:
        # Use when updating more than one value, otherwise use self.__update_value__()

        with open(f'{self.CHARACTER_FILE_PATH}/{FILE_NAME}.json', 'r') as operate_file:
            character_info: dict = json.load(operate_file)

        loop_counter: int = 0
        for x in KEYS:
            dict_key = KEYS[loop_counter]
            dict_value = VALUES[loop_counter]
            log.debug(f'{self.OWNER_ID} | {self.OWNER_NAME} |  __update_vals loop | {dict_key} -> {dict_value}')
            character_info[dict_key] = dict_value
            loop_counter += 1

        with open(f'{self.CHARACTER_FILE_PATH}/{FILE_NAME}.json', 'w') as operate_file:
            json.dump(character_info, operate_file)

        return None

    async def __update_value__(self, KEY: str, VALUE, FILE_NAME: str) -> None:
        # Use when updating one value, otherwise use self.__update_values__()

        with open(f'{self.CHARACTER_FILE_PATH}/{FILE_NAME}.json', 'r') as operate_file:
            character_info: dict = json.load(operate_file)

        log.debug(f'{self.OWNER_ID} | {self.OWNER_NAME} |  __update_val | {KEY}: {VALUE} -> {FILE_NAME}')
        character_info[KEY] = VALUE

        with open(f'{self.CHARACTER_FILE_PATH}/{FILE_NAME}.json', 'w') as operate_file:
            json.dump(character_info, operate_file)

        return None

    async def __rouse_check__(self) -> tuple:
        HUNGER: int = await self.__get_value__('hunger', 'misc')
        ROUSE_NUM_RESULT: int = random.randint(1, 10)

        if HUNGER >= 5:
            result: tuple = ('Frenzy', HUNGER)
            return result  # Hunger Frenzy, No Hunger Gain Too High Already

        elif ROUSE_NUM_RESULT >= 6:
            result: tuple = ('Pass', HUNGER)
            return result  # No Hunger Gain

        elif ROUSE_NUM_RESULT <= 5:
            await self.__update_value__('hunger', (HUNGER+1), 'misc')
            result: tuple = ('Fail', HUNGER+1)
            return result  # 1 Hunger Gain

    async def __roll__(self, page: discord.Embed, RETURN_EXTRA: bool = False):

        # Could be merged, however I was encountering an odd error
        # where difficulty wasn't being assigned correctly.
        DIFFICULTY: int = int(await self.__get_value__('difficulty', 'roll/info'))
        POOL: int = int(await self.__get_value__('pool', 'roll/info'))

        if POOL >= 100:
            # This _should_ never be possible.
            raise OverflowError

        HUNGER: int = await self.__get_value__('hunger', 'misc')

        result: dict = {
            # Can be Rerolled by self.__re_roll__
            'regular_crit': 0,
            'regular_success': 0,
            'regular_fail': 0,

            # These can't be rerolled by self.__re_roll__
            'hunger_crit': 0,
            'hunger_success': 0,
            'hunger_fail': 0,
            'hunger_skull': 0}

        while_pool = POOL
        while_hunger = HUNGER
        while 0 < while_pool:
            die_result = randint(1, 10)

            if while_hunger <= 0:

                if die_result == 10:
                    result['regular_crit'] += 1
                elif die_result >= 6:
                    result['regular_success'] += 1
                elif die_result <= 5:
                    result['regular_fail'] += 1

            else:
                while_hunger -= 1

                if die_result == 10:
                    result['hunger_crit'] += 1
                elif die_result == 1:
                    result['hunger_skull'] += 1
                elif die_result >= 6:
                    result['hunger_success'] += 1
                elif die_result <= 5:
                    result['hunger_fail'] += 1

            while_pool -= 1

        UPDATE_KEYS = ('regular_crit', 'regular_success', 'regular_fail',
                       'hunger_crit', 'hunger_success', 'hunger_fail', 'hunger_skull')
        UPDATE_VALUES = (result['regular_crit'], result['regular_success'], result['regular_fail'],
                         result['hunger_crit'], result['hunger_success'], result['hunger_fail'], result['hunger_skull'])
        await self.__update_values__(UPDATE_KEYS, UPDATE_VALUES, 'roll/info')

        roll_flag: str = ''
        crits: int = 0
        unused_crit_die: int = result['regular_crit'] + result['hunger_crit']
        while_total: int = unused_crit_die

        while while_total > -1:

            # If there are at-least 2 crit die continue
            # otherwise add the remaining crit die and stop
            if result['regular_crit'] + result['hunger_crit'] > 2:

                if result['regular_crit'] >= 2:
                    crits += 1
                    roll_flag = 'Crit'
                    result['regular_crit'] -= 2
                    unused_crit_die -= 2

                elif result['hunger_crit'] >= 2:
                    crits += 1
                    roll_flag = 'Messy Crit'
                    result['hunger_crit'] -= 2
                    unused_crit_die -= 2

                elif result['regular_crit'] + result['hunger_crit'] >= 2:
                    crits += 1
                    roll_flag = 'Messy Crit'
                    result['regular_crit'] -= 1
                    result['hunger_crit'] -= 1
                    unused_crit_die -= 2
            else:
                break
            while_total -= 1

        TOTAL_SUCCESSES: int = int((result['regular_success'] + result['hunger_success'] + unused_crit_die) + crits * 4)
        TOTAL_FAILS: int = int(result['regular_fail'] + result['hunger_fail'] + result['hunger_skull'])

        if TOTAL_SUCCESSES >= DIFFICULTY and roll_flag == '':
            roll_flag = 'Regular Success'
        elif TOTAL_SUCCESSES <= DIFFICULTY and roll_flag == '':
            roll_flag = 'Regular Fail'
            if result['hunger_skull'] >= 1:
                roll_flag = 'Bestial Failure'

        page.add_field(name='Success Count', value=f'{TOTAL_SUCCESSES}')
        page.add_field(name='Failure Count', value=f'{TOTAL_FAILS}')
        page.add_field(name='Roll Result', value=f'{roll_flag}')

        if RETURN_EXTRA is True:
            return page, result, roll_flag

        return page

    async def __hunt__(self, input_page: discord.Embed):
        page, _UNUSED_, ROLL_FLAG = await self.__roll__(input_page, True)

        MISC_DICT: dict = await self.__get_values__(('hunger', 'blood_potency'), 'misc')
        BLOOD_POTENCY: int = MISC_DICT['blood_potency']
        hunger: int = MISC_DICT['hunger']

        page.add_field(name='Roll Mark:', value=f'**Hunt**')

        if ROLL_FLAG == 'Regular Fail':
            page.add_field(name='Hunt Failed.', value=f'Ask DM About Resulting Consequences')
            return page

        min_hunger_without_kill: int = 1
        if BLOOD_POTENCY >= 5:
            min_hunger_without_kill: int = 2

        if hunger == 0:
            min_hunger_without_kill: int = 0
        elif int(hunger - 2) <= min_hunger_without_kill:
            hunger: int = min_hunger_without_kill
        else:
            hunger -= 2

        TEMPERAMENT_CHANCE: int = randint(1, 10)
        if TEMPERAMENT_CHANCE >= 6:
            RESONANCE_DICT: dict = \
                {1: 'phlegmatic', 2: 'phlegmatic', 3: 'phlegmatic',
                 4: 'melancholy', 5: 'melancholy', 6: 'melancholy',
                 7: 'choleric', 8: 'choleric',
                 9: 'sanguine', 10: 'sanguine'}
            RESONANCE: str = RESONANCE_DICT[randint(1, 10)]
            await self.__update_value__('resonance', RESONANCE.capitalize(), 'misc')

            temperament_roll: int = randint(1, 10)
            TEMPERAMENT_DICT: dict = \
                {1: 'negligible', 2: 'negligible', 3: 'negligible', 4: 'negligible', 5: 'negligible',
                 6: 'fleeting', 7: 'fleeting', 8: 'fleeting',
                 9: 'intense_or_acute', 10: 'intense_or_acute'}

            # For an Acute (highest) temperament a 9/10 must be rolled *then* an additional 9/10 must be rolled
            # otherwise it'll just be Intense
            if temperament_roll >= 9:
                temperament_roll: int = randint(1, 10)
                if temperament_roll >= 9:
                    TEMPERAMENT: str = 'Acute'
                else:
                    TEMPERAMENT: str = 'Intense'
            else:
                TEMPERAMENT: str = TEMPERAMENT_DICT[temperament_roll]

            page.add_field(name=f'{TEMPERAMENT} {RESONANCE}', value='')

        else:
            page.add_field(name=f'No Temperament', value='')

        #
        if ROLL_FLAG == 'Regular Success':
            page.add_field(name='Hunt:', value=f'Success | {hunger * mc.HUNGER_EMOJI}')

        elif ROLL_FLAG == 'Messy Crit':
            page.add_field(name='Hunt:', value=f'Messy Crit | {hunger * mc.HUNGER_EMOJI}')

        elif ROLL_FLAG == 'Crit':
            page.add_field(name='Hunt:', value=f'Flawless | {hunger * mc.HUNGER_EMOJI}')

        elif ROLL_FLAG == 'Bestial Failure':
            page.add_field(name='Hunt:', value=f'BESTIAL FAILURE | {hunger * mc.HUNGER_EMOJI}')

        await self.__update_value__('hunger', hunger, 'roll/misc')
