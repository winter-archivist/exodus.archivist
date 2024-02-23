import discord
import json

import misc.config.main_config as mc
import cogs.vtm_toolbox.vtb_characters.vtb_character_manager as cm


class EMPTY_VIEW(discord.ui.View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT


async def basic_page_builder(interaction: discord.Interaction, page_title: str, page_description: str, page_color: str) -> discord.Embed:
    if page_color not in mc.EMBED_COLORS:
        raise ValueError(f'*> Bad Page Color')

    base_page: discord.Embed = discord.Embed(title=page_title, description=page_description, colour=mc.EMBED_COLORS[f"{page_color.lower()}"])

    CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
    CHARACTER_AVATAR_URL: str = (await CHARACTER.__get_information__(('character_avatar_url',), 'misc'))['character_avatar_url']

    USER_INFO = {'user_name'  : interaction.user,
                 'user_id'    : interaction.user.id,
                 'user_avatar': interaction.user.display_avatar}

    base_page.set_thumbnail(url=CHARACTER_AVATAR_URL)
    base_page.set_footer(text=f'{USER_INFO["user_id"]}', icon_url=f'{USER_INFO["user_avatar"]}')
    base_page.set_author(name=f'{USER_INFO["user_name"]}', icon_url=f'{USER_INFO["user_avatar"]}')
    base_page.add_field(name='Character Name', value=f'{CHARACTER.CHARACTER_NAME}', inline=False)

    return base_page


async def standard_roller_page_modifications(page: discord.Embed, CHARACTER: cm.vtb_Character) -> discord.Embed:
    page.add_field(name='', value='', inline=False)  # Just makes sure it isn't interfering with any other fields/elements

    CHARACTER_INFORMATION: dict = await CHARACTER.__get_information__(('pool', 'difficulty', 'composition'), 'roll/info')
    page.add_field(name='Pool', value=f'{CHARACTER_INFORMATION["pool"]}', inline=True)
    page.add_field(name='Difficulty', value=f'{CHARACTER_INFORMATION["difficulty"]}', inline=True)
    page.add_field(name='Composition', value=f'{CHARACTER_INFORMATION["composition"]}', inline=True)
    return page


async def standard_roll_select(interaction: discord.Interaction, page, select, file_name: str):
    CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)

    CHARACTER_INFORMATION: dict = await CHARACTER.__get_information__(('pool', 'composition'), 'roll/info')
    pool: int = CHARACTER_INFORMATION['pool']
    composition: str = CHARACTER_INFORMATION['composition']

    for_var: int = 0
    for selections in select.values:
        attribute_value: int = dict(await CHARACTER.__get_information__((f'{select.values[for_var]}',), file_name))[
            select.values[for_var]]
        pool += attribute_value
        composition = f'{composition}, {(select.values[for_var]).capitalize()}[{attribute_value}]'
        for_var += 1

    await CHARACTER.__update_information__((('pool', 'composition'), (pool, composition)), 'roll/info')

    select.disabled = True

    page: discord.Embed = await standard_roller_page_modifications(page, CHARACTER)
    return page
