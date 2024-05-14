import discord
from zenlog import log

import misc.config.main_config as mc
import cogs.vtm_toolbox.vtm_cm.vtb_character_manager as cm


class EMPTY_VIEW(discord.ui.View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT


async def basic_page_builder(CHARACTER: cm.vtb_Character, page_title: str, page_description: str, page_color: str) -> discord.Embed:
    if page_color not in mc.EMBED_COLORS:
        raise ValueError(f'*> Bad Page Color')

    base_page: discord.Embed = discord.Embed(title=page_title, description=page_description, colour=mc.EMBED_COLORS[f"{page_color.lower()}"])

    base_page.set_thumbnail(url=CHARACTER.CHARACTER_AVATAR)
    base_page.set_footer(text=f'{CHARACTER.OWNER_ID}', icon_url=f'{CHARACTER.OWNER_AVATAR}')
    base_page.set_author(name=f'{CHARACTER.OWNER_NAME}', icon_url=f'{CHARACTER.OWNER_AVATAR}')
    base_page.add_field(name='Character Name', value=f'{CHARACTER.CHARACTER_NAME}', inline=False)

    return base_page


async def hp_wp_page_builder(CHARACTER: cm.vtb_Character):
    page: discord.Embed = await basic_page_builder(CHARACTER, 'Health & Willpower', '', 'mint')

    HEALTH: tuple = ('Base Health', 'Superficial Health Damage', 'Aggravated Health Damage')
    HEALTH_DICT: dict = await CHARACTER.__get_values__(HEALTH, 'health')

    WILLPOWER: tuple = ('Base Willpower', 'Superficial Willpower Damage', 'Aggravated Willpower Damage')
    WILLPOWER_DICT: dict = await CHARACTER.__get_values__(WILLPOWER, 'willpower')

    ACTUAL_HEALTH = HEALTH_DICT['Base Health'] - HEALTH_DICT['Superficial Health Damage'] - HEALTH_DICT['Aggravated Health Damage']
    FULL_HEALTH = str(mc.HEALTH_FULL_EMOJI * ACTUAL_HEALTH)
    SUP_HEALTH = str(mc.HEALTH_SUP_EMOJI * HEALTH_DICT['Superficial Health Damage'])
    AGG_HEALTH = str(mc.HEALTH_AGG_EMOJI * HEALTH_DICT['Aggravated Health Damage'])

    if HEALTH_DICT['Superficial Health Damage'] == HEALTH_DICT['Base Health'] and HEALTH_DICT['Aggravated Health Damage'] > 1:
        SUP_HEALTH = str(mc.HEALTH_SUP_EMOJI * int(HEALTH_DICT['Superficial Health Damage'] - HEALTH_DICT['Aggravated Health Damage']))

    ACTUAL_WILLPOWER = WILLPOWER_DICT['Base Willpower'] - WILLPOWER_DICT['Superficial Willpower Damage'] - WILLPOWER_DICT['Aggravated Willpower Damage']
    FULL_WILLPOWER = str(mc.WILLPOWER_FULL_EMOJI * ACTUAL_WILLPOWER)
    SUP_WILLPOWER = str(mc.WILLPOWER_SUP_EMOJI * WILLPOWER_DICT['Superficial Willpower Damage'])
    AGG_WILLPOWER = str(mc.WILLPOWER_AGG_EMOJI * WILLPOWER_DICT['Aggravated Willpower Damage'])

    page.add_field(name='Health', value=f'{FULL_HEALTH}{SUP_HEALTH}{AGG_HEALTH}', inline=False)
    page.add_field(name='Willpower', value=f'{FULL_WILLPOWER}{SUP_WILLPOWER}{AGG_WILLPOWER}', inline=False)

    return page


async def hunger_page_builder(CHARACTER: cm.vtb_Character):
    page: discord.Embed = await basic_page_builder(CHARACTER, 'Hunger & Predator Type', '', 'mint')
    MISC_DICT: dict = await CHARACTER.__get_values__(('Hunger', 'Predator Type'), 'misc')
    page.add_field(name='Hunger', value=f'{MISC_DICT["Hunger"] * mc.HUNGER_EMOJI}', inline=True)

    if CHARACTER.CHARACTER_NAME != 'Nyctea':
        page.add_field(name='Predator Type', value=f'{MISC_DICT["Predator Type"]}', inline=True)
    elif CHARACTER.CHARACTER_NAME == 'Nyctea':
        # Remove the code within this else and take out the if statement, if you intend on using this in your chronicle
        # these limits have been set up due to a specific character in my Chronicle
        page.add_field(name='Predator Type', value='Beyond the Eye of Saulot', inline=True)

    return page


async def extra_page_builder(CHARACTER: cm.vtb_Character) -> discord.Embed:
    page: discord.Embed = await basic_page_builder(CHARACTER, 'Extra', '', 'mint')

    MISC_DICT: dict = await CHARACTER.__get_values__(('Clan', 'Generation', 'Blood Potency'), 'misc')
    HUMANITY_DICT: dict = await CHARACTER.__get_values__(('Humanity', 'Stains', 'Path of Enlightenment'), 'humanity')

    if CHARACTER.CHARACTER_NAME != 'Nyctea':
        page.add_field(name='Clan', value=f'{MISC_DICT["Clan"]}', inline=True)
        page.add_field(name='Path of Enlightenment', value=f'{HUMANITY_DICT["Path of Enlightenment"]}', inline=True)
        page.add_field(name='Generation', value=f'{MISC_DICT["Generation"] * mc.DOT_FULL_EMOJI}', inline=True)
        page.add_field(name='Blood Potency', value=f'{MISC_DICT["Blood Potency"] * mc.HUNGER_EMOJI}', inline=True)
    elif CHARACTER.CHARACTER_NAME == 'Nyctea':
        # Remove the code within this else and take out the if statement, if you intend on using this in your chronicle
        # these limits have been set up due to a specific character in my Chronicle
        page.add_field(name='Clan', value=f'Beyond The Eye of Saulot', inline=True)
        page.add_field(name='Path of Enlightenment', value=f'Beyond The Eye of Saulot', inline=True)
        page.add_field(name='Generation', value=f'Beyond The Eye of Saulot', inline=True)
        page.add_field(name='Blood Potency', value=f'Beyond The Eye of Saulot', inline=True)

    page.add_field(name='Humanity',
                   value=f'{HUMANITY_DICT["Humanity"] * mc.DOT_FULL_EMOJI} {HUMANITY_DICT["Stains"] * mc.DOT_EMPTY_EMOJI}',
                   inline=True)

    return page


async def standard_roller_page_modifications(page: discord.Embed, CHARACTER: cm.vtb_Character) -> discord.Embed:
    page.add_field(name='', value='', inline=False)  # Just makes sure it isn't interfering with any other fields/elements

    CHARACTER_INFORMATION: dict = await CHARACTER.__get_values__(('Pool', 'Difficulty', 'Composition'), 'roll/info')
    page.add_field(name='Pool', value=f'{CHARACTER_INFORMATION["Pool"]}', inline=True)
    page.add_field(name='Difficulty', value=f'{CHARACTER_INFORMATION["Difficulty"]}', inline=True)
    page.add_field(name='Composition', value=f'{CHARACTER_INFORMATION["Composition"]}', inline=True)
    return page


async def standard_roll_select(CHARACTER: cm.vtb_Character, page, select, file_name: str):

    CHARACTER_INFORMATION: dict = await CHARACTER.__get_values__(('Pool', 'Composition'), 'roll/info')
    pool: int = CHARACTER_INFORMATION['Pool']
    composition: str = CHARACTER_INFORMATION['Composition']

    FLAGS = await CHARACTER.__impairment_flags__()
    PHYSICAL_IMPAIRMENT_FLAG = FLAGS[0]
    MENTAL_IMPAIRMENT_FLAG = FLAGS[1]
    DEGENERATION_IMPAIRMENT_FLAG = FLAGS[2]

    for_var: int = 0
    for selections in select.values:
        value: int = await CHARACTER.__get_value__(f'{select.values[for_var]}', file_name)

        if 'attributes' in file_name:
            if DEGENERATION_IMPAIRMENT_FLAG is True:
                value -= 1  # Removes one from ALL attributes since the character is DEGENERATION impaired.

            if PHYSICAL_IMPAIRMENT_FLAG is True or MENTAL_IMPAIRMENT_FLAG is True:
                if select.values[for_var].lower() in ('strength', 'dexterity', 'stamina'):
                    value -= 1  # Removes one from PHYSICAL attributes since the character is PHYSICALLY impaired.

                if select.values[for_var].lower() in ('charisma', 'manipulation', 'composure', 'intelligence', 'wits', 'resolve'):
                    value -= 1  # Removes one from MENTAL & SOCIAL attributes since the character is MENTALLY impaired.

        elif 'skills' in file_name:

            if 'physical' in file_name:
                if PHYSICAL_IMPAIRMENT_FLAG is True:
                    value -= 1

            elif 'social' or 'mental' in file_name:
                if MENTAL_IMPAIRMENT_FLAG is True:
                    value -= 1

            if DEGENERATION_IMPAIRMENT_FLAG is True:
                value -= 2

        pool += value
        composition = f'{composition}, {(select.values[for_var]).capitalize()}[{value}]'
        for_var += 1

    await CHARACTER.__update_values__(('Pool', 'Composition'), (pool, composition), 'roll/info')

    select.disabled = True

    page: discord.Embed = await standard_roller_page_modifications(page, CHARACTER)
    return page
