import discord
from zenlog import log

import misc.config.main_config as mc
import cogs.vtm_toolbox.vtb_characters.vtb_character_manager as cm


class EMPTY_VIEW(discord.ui.View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT


async def basic_page_builder(CHARACTER: cm.vtb_Character, page_title: str, page_description: str, page_color: str) -> discord.Embed:
    if page_color not in mc.EMBED_COLORS:
        raise ValueError(f'*> Bad Page Color')

    base_page: discord.Embed = discord.Embed(title=page_title, description=page_description, colour=mc.EMBED_COLORS[f"{page_color.lower()}"])

    base_page.set_thumbnail(url=CHARACTER.AVATAR_URL)
    base_page.set_footer(text=f'{CHARACTER.OWNER_ID}', icon_url=f'{CHARACTER.OWNER_AVATAR}')
    base_page.set_author(name=f'{CHARACTER.OWNER_NAME}', icon_url=f'{CHARACTER.OWNER_AVATAR}')
    base_page.add_field(name='Character Name', value=f'{CHARACTER.CHARACTER_NAME}', inline=False)

    return base_page


async def hp_wp_page_builder(CHARACTER: cm.vtb_Character):
    page: discord.Embed = await basic_page_builder(CHARACTER, 'Health & Willpower', '', 'mint')

    HEALTH: tuple = ('base_health', 'superficial_health_damage', 'aggravated_health_damage')
    HEALTH_DICT: dict = await CHARACTER.__get_values__(HEALTH, 'health')

    WILLPOWER: tuple = ('base_willpower', 'superficial_willpower_damage', 'aggravated_willpower_damage')
    WILLPOWER_DICT: dict = await CHARACTER.__get_values__(WILLPOWER, 'willpower')

    ACTUAL_HEALTH = HEALTH_DICT['base_health'] - HEALTH_DICT['superficial_health_damage'] - HEALTH_DICT['aggravated_health_damage']
    FULL_HEALTH = str(mc.HEALTH_FULL_EMOJI * ACTUAL_HEALTH)
    SUP_HEALTH = str(mc.HEALTH_SUP_EMOJI * HEALTH_DICT['superficial_health_damage'])
    AGG_HEALTH = str(mc.HEALTH_AGG_EMOJI * HEALTH_DICT['aggravated_health_damage'])

    if HEALTH_DICT['superficial_health_damage'] == HEALTH_DICT['base_health'] and HEALTH_DICT['aggravated_health_damage'] > 1:
        SUP_HEALTH = str(
            mc.HEALTH_SUP_EMOJI * int(HEALTH_DICT['superficial_health_damage'] - HEALTH_DICT['aggravated_health_damage']))

    actual_willpower = WILLPOWER_DICT['base_willpower'] - WILLPOWER_DICT['superficial_willpower_damage'] - WILLPOWER_DICT[
        'aggravated_willpower_damage']
    FULL_WILLPOWER = str(mc.WILLPOWER_FULL_EMOJI * actual_willpower)
    SUP_WILLPOWER = str(mc.WILLPOWER_SUP_EMOJI * WILLPOWER_DICT['superficial_willpower_damage'])
    AGG_WILLPOWER = str(mc.WILLPOWER_AGG_EMOJI * WILLPOWER_DICT['aggravated_willpower_damage'])

    page.add_field(name='Health', value=f'{FULL_HEALTH}{SUP_HEALTH}{AGG_HEALTH}', inline=False)
    page.add_field(name='Willpower', value=f'{FULL_WILLPOWER}{SUP_WILLPOWER}{AGG_WILLPOWER}', inline=False)
    return page


async def hunger_page_builder(CHARACTER: cm.vtb_Character):
    page: discord.Embed = await basic_page_builder(CHARACTER, 'Hunger & Predator Type', '', 'mint')
    CURRENT_HUNGER: int = await CHARACTER.__get_value__('hunger', 'misc')
    page.add_field(name='Hunger', value=f'{CURRENT_HUNGER * mc.HUNGER_EMOJI}', inline=True)
    return page


async def standard_roller_page_modifications(page: discord.Embed, CHARACTER: cm.vtb_Character) -> discord.Embed:
    page.add_field(name='', value='', inline=False)  # Just makes sure it isn't interfering with any other fields/elements

    CHARACTER_INFORMATION: dict = await CHARACTER.__get_values__(('pool', 'difficulty', 'composition'), 'roll/info')
    page.add_field(name='Pool', value=f'{CHARACTER_INFORMATION["pool"]}', inline=True)
    page.add_field(name='Difficulty', value=f'{CHARACTER_INFORMATION["difficulty"]}', inline=True)
    page.add_field(name='Composition', value=f'{CHARACTER_INFORMATION["composition"]}', inline=True)
    return page


async def standard_roll_select(CHARACTER: cm.vtb_Character, page, select, file_name: str):

    CHARACTER_INFORMATION: dict = await CHARACTER.__get_values__(('pool', 'composition'), 'roll/info')
    pool: int = CHARACTER_INFORMATION['pool']
    composition: str = CHARACTER_INFORMATION['composition']

    for_var: int = 0
    for selections in select.values:
        attribute_value: int = await CHARACTER.__get_value__(f'{select.values[for_var]}', file_name)
        pool += attribute_value
        composition = f'{composition}, {(select.values[for_var]).capitalize()}[{attribute_value}]'
        for_var += 1

    await CHARACTER.__update_values__(('pool', 'composition'), (pool, composition), 'roll/info')

    select.disabled = True

    page: discord.Embed = await standard_roller_page_modifications(page, CHARACTER)
    return page
