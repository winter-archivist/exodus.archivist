import os
import json
import random
import discord
from zenlog import log
from random import randint

from misc.config import main_config as mc


async def make_blank_character_files(interaction: discord.Interaction, CHARACTER_NAME):
    CHARACTER_DIRECTORY: str = f'cogs/vtm_toolbox/vtb_characters/{interaction.user.id}/{CHARACTER_NAME}/'

    if not os.path.exists(f'cogs/vtm_toolbox/vtb_characters/{interaction.user.id}'):
        os.mkdir(f'cogs/vtm_toolbox/vtb_characters/{interaction.user.id}')

    if os.path.exists(CHARACTER_DIRECTORY):
        log.debug(f'> | {interaction.user.name} | {interaction.user.id} | '
                  f'Attempted to make {CHARACTER_NAME}, but {CHARACTER_DIRECTORY} already exists.')
        raise FileExistsError

    os.mkdir(f'{CHARACTER_DIRECTORY}')
    os.mkdir(f'{CHARACTER_DIRECTORY}skills')
    os.mkdir(f'{CHARACTER_DIRECTORY}roll')

    MISC_DICT: dict = {'Owner ID'            : interaction.user.id,
                       'Character Name'      : CHARACTER_NAME,
                       'Blood Potency'       : 0,
                       'Clan'                : '',
                       'Bloodline'           : '',
                       'Generation'          : 0,
                       'Bane Severity'       : 0,
                       'Hunger'              : 0,
                       'Predator Type'       : '',
                       'Temperament'         : '',
                       'Resonance'           : '',
                       'Character Avatar URL': mc.PLACEHOLDER_IMG}

    HEALTH_DICT: dict = {'Base Health'              : 0,
                         'Superficial Health Damage': 0,
                         'Aggravated Health Damage' : 0}

    WILLPOWER_DICT: dict = {'Base Willpower'              : 0,
                            'Superficial Willpower Damage': 0,
                            'Aggravated Willpower Damage' : 0}

    ATTRIBUTES_DICT: dict = {'Strength'    : 0,
                             'Dexterity'   : 0,
                             'Stamina'     : 0,
                             'Charisma'    : 0,
                             'Manipulation': 0,
                             'Composure'   : 0,
                             'Intelligence': 0,
                             'Wits'        : 0,
                             'Resolve'     : 0}

    # All Non-Extra are sorted alphabetically
    DISCIPLINES_DICT: dict = {'Animalism'          : 0,
                              'Auspex'             : 0,
                              'Blood Sorcery'      : 0,
                              'Blood Rituals'      : 0,
                              'Celerity'           : 0,
                              'Chemeristry'        : 0,  # Non-v5
                              'Dementation'        : 0,  # Non-v5
                              'Dominate'           : 0,
                              'Fortitude'          : 0,
                              'Necromancy'         : 0,  # Non-v5
                              'Obfuscate'          : 0,
                              'Obtenebration'      : 0,  # Non-v5
                              'Potence'            : 0,
                              'Presence'           : 0,
                              'Protean'            : 0,
                              'Thin-Blood Alchemy' : 0,

                              # ! Comments are specific to my chronicle, feel free to remove these comments
                              'Hidden/Extra 1'     : 0,  # Hidden/Extra 1 [Temporis::Seven | Vicissitude::Elijah | Kyrvex::Nyctea]
                              'Hidden/Extra 2'     : 0,  # Hidden/Extra 2 [Spirit::Nyctea]
                              'Hidden/Extra 3'     : 0}

    PHYSICAL_SKILLS_DICT: dict = {'Athletics': 0,
                                  'Brawl'    : 0,
                                  'Craft'    : 0,
                                  'Drive'    : 0,
                                  'Firearms' : 0,
                                  'Larceny'  : 0,
                                  'Melee'    : 0,
                                  'Stealth'  : 0,
                                  'Survival' : 0}

    SOCIAL_SKILLS_DICT: dict = {'Animal Ken'  : 0,
                                'Etiquette'   : 0,
                                'Insight'     : 0,
                                'Intimidation': 0,
                                'Leadership'  : 0,
                                'Performance' : 0,
                                'Persuasion'  : 0,
                                'Streetwise'  : 0,
                                'Subterfuge'  : 0}

    MENTAL_SKILLS_DICT: dict = {'Academics'    : 0,
                                'Awareness'    : 0,
                                'Finance'      : 0,
                                'Investigation': 0,
                                'Medicine'     : 0,
                                'Occult'       : 0,
                                'Politics'     : 0,
                                'Science'      : 0,
                                'Technology'   : 0}

    ROLL_DICT: dict = {'Difficulty': 0,
                       'Pool' : 0,
                       'Result': '',
                       'Composition': 'Base[0]',

                       # These are NOT a dict as to make it friendlier with the get/update functions of vtb_Character
                       'Regular Crit Count': 0,
                       'Regular Success Count': 0,
                       'Regular Fail Count': 0,
                       'Hunger Crit Count': 0,
                       'Hunger Success Count' : 0,
                       'Hunger Fail Count' : 0,
                       'Hunger Skull': 0}

    HUMANITY_DICT: dict = {
        'Humanity': 0,
        'Stains': 0,
        'Path of Enlightenment': 'UNSET',
        'Degeneration Impairment': False}

    CHARACTER_FILES: tuple = ('misc', 'health', 'willpower', 'attributes', 'disciplines',
                              'skills/physical', 'skills/social', 'skills/mental', 'roll/info',
                              'humanity')

    FILE_CONTENTS: tuple = (MISC_DICT, HEALTH_DICT, WILLPOWER_DICT, ATTRIBUTES_DICT, DISCIPLINES_DICT,
                            PHYSICAL_SKILLS_DICT, SOCIAL_SKILLS_DICT, MENTAL_SKILLS_DICT, ROLL_DICT,
                            HUMANITY_DICT)

    for_var: int = 0
    for x in CHARACTER_FILES:
        with open(f'{CHARACTER_DIRECTORY}{CHARACTER_FILES[for_var]}.json', "w") as operate_file:
            json.dump(FILE_CONTENTS[for_var], operate_file)
        for_var += 1


class vtb_Character:
    def __init__(self, interaction: discord.Interaction):
        CHARACTER_NAME_FILE: str = f'cogs/vtm_toolbox/vtb_characters/{interaction.user.id}/target_character.json'
        with open(CHARACTER_NAME_FILE, 'r') as operate_file:
            CHARACTER_NAME = json.load(operate_file)['character_name']

        self.CHARACTER_NAME: str = CHARACTER_NAME
        self.CHARACTER_FILE_PATH: str = f'cogs/vtm_toolbox/vtb_characters/{interaction.user.id}/{self.CHARACTER_NAME}'

        if not os.path.isdir(self.CHARACTER_FILE_PATH):
            # This just means the user doesn't have any character with the name found in .../{user_id}/target_character.json.
            raise FileNotFoundError

        with open(f'{self.CHARACTER_FILE_PATH}/misc.json', 'r') as operate_file:
            CHARACTER_INFO = json.load(operate_file)

        self.OWNER_NAME = interaction.user.name
        self.OWNER_ID = interaction.user.id
        self.OWNER_AVATAR = interaction.user.display_avatar
        self.CHARACTER_AVATAR: str = CHARACTER_INFO['Character Avatar URL']

    # The get/update value/values functions are split since if you only need one value returned/updated
    # then there's no point in going through the for loop/using tuples, this just slightly increases performance;
    # not that this bot needs to be/is performant, especially being written in python, by a newbie.
    async def __get_values__(self, KEYS: tuple, FILE_NAME: str) -> dict:
        """
        Use when getting more than one value, otherwise use self.__get_value__()
        """

        with open(f'{self.CHARACTER_FILE_PATH}/{FILE_NAME}.json', 'r') as operate_file:
            CHARACTER_INFO: dict = json.load(operate_file)

        return_information: dict = {}
        loop_counter: int = 0
        for x in KEYS:
            return_information[f'{KEYS[loop_counter]}'] = CHARACTER_INFO[f'{KEYS[loop_counter]}']
            loop_counter += 1

        log.debug(f'> vtbCM __get_vals: {KEYS[loop_counter]}->{return_information} | {self.OWNER_ID} | {self.OWNER_NAME} |')
        return return_information

    async def __get_value__(self, KEY: str, FILE_NAME: str):
        """
        Use when getting one value, otherwise use self.__get_values__()
        """

        with open(f'{self.CHARACTER_FILE_PATH}/{FILE_NAME}.json', 'r') as operate_file:
            CHARACTER_INFO: dict = json.load(operate_file)

        RETURN_INFORMATION = CHARACTER_INFO[KEY]

        log.debug(f'> vtbCM __get_val: {KEY}->{RETURN_INFORMATION} | {self.OWNER_ID} | {self.OWNER_NAME} |')

        return RETURN_INFORMATION

    async def __update_values__(self, KEYS: tuple, VALUES: tuple, FILE_NAME: str) -> None:
        """
        Use when updating more than one value, otherwise use self.__update_value__()
        """

        with open(f'{self.CHARACTER_FILE_PATH}/{FILE_NAME}.json', 'r') as operate_file:
            character_info: dict = json.load(operate_file)

        loop_counter: int = 0
        for x in KEYS:
            dict_key = KEYS[loop_counter]
            dict_value = VALUES[loop_counter]
            log.debug(f'> vtbCM __update_vals loop: {dict_key} -> {dict_value} | {self.OWNER_ID} | {self.OWNER_NAME} |')
            character_info[dict_key] = dict_value
            loop_counter += 1

        with open(f'{self.CHARACTER_FILE_PATH}/{FILE_NAME}.json', 'w') as operate_file:
            json.dump(character_info, operate_file)

        return None

    async def __update_value__(self, KEY: str, VALUE, FILE_NAME: str) -> None:
        """
        Use when updating one value, otherwise use self.__update_values__()
        """

        with open(f'{self.CHARACTER_FILE_PATH}/{FILE_NAME}.json', 'r') as operate_file:
            character_info: dict = json.load(operate_file)

        log.debug(f'> vtbCM __update_val: {KEY}: {VALUE} -> {FILE_NAME} | {self.OWNER_ID} | {self.OWNER_NAME} |')
        character_info[KEY] = VALUE

        with open(f'{self.CHARACTER_FILE_PATH}/{FILE_NAME}.json', 'w') as operate_file:
            json.dump(character_info, operate_file)

        return None

    async def __impairment_flags__(self) -> tuple:
        """
        Checks all impairment flags, then returns a tuple of booleans.
        """

        #       === Typical Call ===

        #        FLAGS = await CHARACTER.__impairment_flags__()
        #        PHYSICAL_IMPAIRMENT_FLAG = FLAGS[0]
        #        MENTAL_IMPAIRMENT_FLAG = FLAGS[1]
        #        DEGENERATION_IMPAIRMENT_FLAG = FLAGS[2]

        physical_impairment_flag: bool = False
        HEALTH_BASE: int = await self.__get_value__('Base Health', 'health')
        HEALTH_SUPERFICIAL_DAMAGE: int = await self.__get_value__('Superficial Health Damage', 'health')
        if HEALTH_BASE <= HEALTH_SUPERFICIAL_DAMAGE:
            # count -= 1
            # page.add_field(name='Physically Impaired.', value='-1 to Physical Dice Pools', inline=False)
            physical_impairment_flag = True

        mental_impairment_flag: bool = False
        WILLPOWER_BASE: int = await self.__get_value__('Base Willpower', 'willpower')
        WILLPOWER_SUPERFICIAL_DAMAGE: int = await self.__get_value__('Superficial Willpower Damage', 'willpower')
        if WILLPOWER_BASE <= WILLPOWER_SUPERFICIAL_DAMAGE:
            # count -= 1
            # page.add_field(name='Mentally Impaired', value='-1 to Social & Mental Dice Pools', inline=False)
            mental_impairment_flag = True

        degeneration_impairment_flag: bool = await self.__get_value__('Degeneration Impairment', 'humanity')
        # count -= 2
        # page.add_field(name='Degeneration Impaired.', value='-2 to All Dice Pools', inline=False)

        FLAGS: tuple = (physical_impairment_flag, mental_impairment_flag, degeneration_impairment_flag)
        return FLAGS

    async def __rouse_check__(self) -> tuple:
        """
        Makes a Rouse Check then returns the result as a tuple (str(Result), int(Hunger))
        """
        HUNGER: int = await self.__get_value__('Hunger', 'misc')
        ROUSE_NUM_RESULT: int = random.randint(1, 10)

        if HUNGER >= 5:
            result: tuple = ('Frenzy', HUNGER)
            return result  # Hunger Frenzy, No Hunger Gain Too High Already

        elif ROUSE_NUM_RESULT >= 6:
            result: tuple = ('Pass', HUNGER)
            return result  # No Hunger Gain

        elif ROUSE_NUM_RESULT <= 5:
            await self.__update_value__('Hunger', (HUNGER+1), 'misc')
            result: tuple = ('Fail', HUNGER+1)
            return result  # 1 Hunger Gain

    async def __roll__(self, page: discord.Embed, RETURN_EXTRA: bool = False):
        """
        Typically just returns the page, if you require the flags of the roll or the exact results RETURN_EXTRA needs to be True.
        """

        # Could be merged, however I was encountering an odd error
        # where difficulty wasn't being assigned correctly.
        DIFFICULTY: int = int(await self.__get_value__('Difficulty', 'roll/info'))
        POOL: int = int(await self.__get_value__('Pool', 'roll/info'))

        if POOL >= 100:
            # This _should_ never be possible.
            raise OverflowError

        HUNGER: int = await self.__get_value__('Hunger', 'misc')

        result: dict = {
            # Can be Rerolled by self.__re_roll__
            'Regular Crit': 0,
            'Regular Success': 0,
            'Regular Fail': 0,

            # These can't be rerolled by self.__re_roll__
            'Hunger Crit': 0,
            'Hunger Success': 0,
            'Hunger Fail': 0,
            'Hunger Skull': 0}

        while_pool = POOL
        while_hunger = HUNGER
        while 0 < while_pool:
            die_result = randint(1, 10)

            if while_hunger <= 0:

                if die_result == 10:
                    result['Regular Crit'] += 1
                elif die_result >= 6:
                    result['Regular Success'] += 1
                elif die_result <= 5:
                    result['Regular Fail'] += 1

            else:
                while_hunger -= 1

                if die_result == 10:
                    result['Hunger Crit'] += 1
                elif die_result == 1:
                    result['Hunger Skull'] += 1
                elif die_result >= 6:
                    result['Hunger Success'] += 1
                elif die_result <= 5:
                    result['Hunger Fail'] += 1

            while_pool -= 1

        UPDATE_KEYS = ('Regular Crit', 'Regular Success', 'Regular Fail',
                       'Hunger Crit', 'Hunger Success', 'Hunger Fail', 'Hunger Skull')
        UPDATE_VALUES = (result['Regular Crit'], result['Regular Success'], result['Regular Fail'],
                         result['Hunger Crit'], result['Hunger Success'], result['Hunger Fail'], result['Hunger Skull'])
        await self.__update_values__(UPDATE_KEYS, UPDATE_VALUES, 'roll/info')

        roll_flag: str = ''
        crits: int = 0
        unused_crit_die: int = result['Regular Crit'] + result['Hunger Crit']
        while_total: int = unused_crit_die

        while while_total > -1:

            # If there are at-least 2 crit die continue
            # otherwise add the remaining crit die and stop
            if result['Regular Crit'] + result['Hunger Crit'] > 2:

                if result['Regular Crit'] >= 2:
                    crits += 1
                    roll_flag = 'Crit'
                    result['Regular Crit'] -= 2
                    unused_crit_die -= 2

                elif result['Hunger Crit'] >= 2:
                    crits += 1
                    roll_flag = 'Messy Crit'
                    result['Hunger Crit'] -= 2
                    unused_crit_die -= 2

                elif result['Regular Crit'] + result['Hunger Crit'] >= 2:
                    crits += 1
                    roll_flag = 'Messy Crit'
                    result['Regular Crit'] -= 1
                    result['Hunger Crit'] -= 1
                    unused_crit_die -= 2
            else:
                break
            while_total -= 1

        TOTAL_SUCCESSES: int = int((result['Regular Success'] + result['Hunger Success'] + unused_crit_die) + crits * 4)
        TOTAL_FAILS: int = int(result['Regular Fail'] + result['Hunger Fail'] + result['Hunger Skull'])

        if TOTAL_SUCCESSES >= DIFFICULTY and roll_flag == '':
            roll_flag = 'Regular Success'
        elif TOTAL_SUCCESSES <= DIFFICULTY and roll_flag == '':
            roll_flag = 'Regular Fail'
            if result['Hunger Skull'] >= 1:
                roll_flag = 'Bestial Failure'

        page.add_field(name='Success Count', value=f'{TOTAL_SUCCESSES}')
        page.add_field(name='Failure Count', value=f'{TOTAL_FAILS}')
        page.add_field(name='Roll Result', value=f'{roll_flag}')

        if RETURN_EXTRA is True:
            return page, result, roll_flag

        return page

    async def __hunt__(self, input_page: discord.Embed):
        """
        Will roll automatically, no need to do it prior.
        """
        page, _UNUSED_, ROLL_FLAG = await self.__roll__(input_page, True)

        MISC_DICT: dict = await self.__get_values__(('Hunger', 'Blood Potency'), 'misc')
        BLOOD_POTENCY: int = MISC_DICT['Blood Potency']
        hunger: int = MISC_DICT['Hunger']

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
                {1: 'Phlegmatic', 2: 'Phlegmatic', 3: 'Phlegmatic',
                 4: 'Melancholy', 5: 'Melancholy', 6: 'Melancholy',
                 7: 'Choleric', 8: 'Choleric',
                 9: 'Sanguine', 10: 'Sanguine'}
            RESONANCE: str = RESONANCE_DICT[randint(1, 10)]
            await self.__update_value__('Resonance', RESONANCE, 'misc')

            temperament_roll: int = randint(1, 10)
            TEMPERAMENT_DICT: dict = \
                {1: 'Negligible', 2: 'Negligible', 3: 'Negligible', 4: 'Negligible', 5: 'Negligible',
                 6: 'Fleeting', 7: 'Fleeting', 8: 'Fleeting',
                 9: 'Intense or Acute', 10: 'Intense or Acute'}

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

        await self.__update_value__('Hunger', hunger, 'roll/misc')
