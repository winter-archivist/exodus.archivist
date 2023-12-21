import discord
import sqlite3
import os as os
from zenlog import log
from discord import Embed
from discord.ui import View

from misc.utils import yamlUtils as yU
from misc.config import mainConfig as mC

import cogs.vampire.vTracker.trackerPageBuilders as tpb


async def trackerInitialize(interaction, character_name):
    targetDB = f'cogs//vampire//characters//{str(interaction.user.id)}//{character_name}//{character_name}.sqlite'

    log.debug(f'> Checking if [ `{targetDB}` ] exists')
    if not os.path.exists(targetDB):
        log.warn(f'*> Database [ `{targetDB}` ] does not exist')
        await interaction.response.send_message(embed=discord.Embed(
            title='Database Error', color=mC.embed_colors["red"],
            description=f'[ `{character_name}` ] Does Not Exist.. \n\n {mC.ISSUE_CONTACT}'), ephemeral=True)
        return
    else:
        log.debug(f'> Successful Connection to [ `{targetDB}` ]')

    with sqlite3.connect(targetDB) as db:
        char_owner_id = db.cursor().execute('SELECT userID FROM ownerInfo').fetchone()[0]
        if char_owner_id != interaction.user.id:  # ? If interaction user doesn't own the character
            await interaction.response.send_message(f'You don\'t own {character_name}', ephemeral=True)
            return False

        targetCache = f'cogs/vampire/characters/{str(interaction.user.id)}/{str(interaction.user.id)}.yaml'
        await yU.cacheClear(targetCache)
        await yU.cacheWrite(targetCache, dataInput={'characterName': f'{character_name}'})

    return True


async def tevNav(interaction, target_page) -> Embed and View:  # ? tevNav = Tracker Embed-View Navigator
    allowed_targets = ('home', 'hp/wp', 'hunger', 'attributes', 'skills', 'physical_skills', 'social_skills', 'mental_skills', 'discipline', 'extras')
    log.debug(f'> tevNav Start. [ {target_page} ]')
    if target_page.lower() in allowed_targets:
        # ? Find name of the intended character
        target_cache = f'cogs/vampire/characters/{str(interaction.user.id)}/{str(interaction.user.id)}.yaml'
        use_data: dict = {}; use_data.update(await yU.cacheRead(f'{target_cache}'))
        character_name: str = str(use_data['characterName'])

        user_info = {'user_name': interaction.user,
                     'user_id': interaction.user.id,
                     'user_avatar': interaction.user.display_avatar}

        return_embed = Embed(title='Kindred Tracker', description='If a button is __Gray__ that means its non-functional', colour=mC.embed_colors["mint"])

        # ? Resets Embed
        return_embed.clear_fields()

        with sqlite3.connect(f'cogs//vampire//characters//{str(interaction.user.id)}//{character_name}//{character_name}.sqlite') as db:
            cursor = db.cursor()

            # ? Adds information seen on all pages.
            character_avatar = cursor.execute('SELECT imgURL from charInfo').fetchone()[0]
            return_embed.set_thumbnail(url=character_avatar)
            return_embed.set_footer(text=f'{user_info["user_id"]}', icon_url=f'{user_info["user_avatar"]}')
            return_embed.set_author(name=f'{user_info["user_name"]}', icon_url=f'{user_info["user_avatar"]}')
            return_embed.add_field(name='Character Name', value=f'{character_name}', inline=False)

            # ? Adds information based on target_page
            try:
                if target_page == 'home':
                    return_embed, return_view = await tpb.homePageBuilder(return_embed)
                elif target_page == 'hp/wp':
                    return_embed, return_view = await tpb.hpwpPageBuilder(return_embed, cursor)
                elif target_page == 'hunger':
                    return_embed, return_view = await tpb.hungerPageBuilder(return_embed, cursor)
                elif target_page == 'attributes':
                    return_embed, return_view = await tpb.attributePageBuilder(return_embed, cursor)
                elif target_page == 'skills':
                    return_embed, return_view = await tpb.skillsPageBuilder(return_embed, cursor)
                elif target_page == 'physical_skills':
                    return_embed, return_view = await tpb.physicalSkillsPageBuilder(return_embed, cursor)
                elif target_page == 'social_skills':
                    return_embed, return_view = await tpb.socialSkillsPageBuilder(return_embed, cursor)
                elif target_page == 'mental_skills':
                    return_embed, return_view = await tpb.mentalSkillsPageBuilder(return_embed, cursor)
                elif target_page == 'discipline':
                    return_embed, return_view = await tpb.disciplinePageBuilder(return_embed, cursor)
                elif target_page == 'extras':
                    return_embed, return_view = await tpb.extrasPageBuilder(return_embed, cursor)
            except sqlite3.Error as e:
                log.error(f'**> tevNav | SQLITE3 ERROR | {e}')

        log.debug(f'> tevNav Success [ {target_page} ]')
        return return_embed, return_view
    elif target_page.lower() not in allowed_targets:
        log.error(f'*> Invalid tevNav target_page [ {target_page} ]')
    else:
        log.error(f'**> tevNav had received an incredibly invalid target_page. [ {target_page} ]')
