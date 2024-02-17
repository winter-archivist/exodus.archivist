import discord
import json

import misc.config.main_config as mc
import cogs.vtm_toolbox.vtb_characters.vtb_character_manager as cm


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


async def tracker_home_builder():
    pass
