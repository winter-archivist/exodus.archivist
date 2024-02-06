import sqlite3
from zenlog import log
from discord import Embed
from discord.ui import View

import misc.config.mainConfig as mC

import cogs.vampire.vMisc.vampireUtils as vU
import cogs.vampire.vTracker.trackerPageBuilders as tPB
import cogs.vampire.vRoller.rollerPageBuilders as rPB


# Felt this may be useful for looking at the horrid Vampire Page System.
# These two are the two most common circumstances that the VPS is used
#
# Command Used
# - vampirePageCommand()
# -- writeCharacterName()
# Buttons using VPS start here
# -- pageEVNav()  # Assumes the user has used a VPS command before this point (basically impossible to not do)
# --- basicPageBuilder()  # The Embed/Page Doesn't Exist Until This Function; Color is Determined Here
# ---- getCharacterName()
# ---- ____UNIVERSAL Page Alterations Here____
# --- chosenPageDecider()
# ---- ____Chosen Page GROUP Alterations Here____
# ---- chosenPageBuilder()
# ----- ___Chosen Page SPECIFIC Alterations Here____


async def vampirePageCommand(self, interaction, character_name: str, initial_target_page_name: str, ephemeral: bool):
    if await vU.writeCharacterName(interaction, character_name) is True:
        initial_embed, initial_view = await pageEVNav(interaction, initial_target_page_name)
        if 'roller' in initial_target_page_name:
            await rPB.rollerBasicPageInformation(interaction, initial_embed)
        await interaction.response.send_message(embed=initial_embed, view=initial_view(self.CLIENT), ephemeral=ephemeral)


async def pageEVNav(interaction, target_page_name: str) -> Embed and View:  # ? pageEVNav = Page Embed-View Navigator
    roller_targets = ('roller.difficulty', 'roller.attribute', 'roller.physical', 'roller.social' , 'roller.mental',
                      'roller.discipline' , 'roller.extras',
                      'roller.rolled', 'roller.rerolled', 'roller.hunt_roll', 'roller.hunt_rerolled')
    tracker_targets = ('tracker.home', 'tracker.hp/wp', 'tracker.hunger', 'tracker.attributes', 'tracker.discipline',
                       'tracker.extras', 'tracker.skills', 'tracker.physical_skills', 'tracker.social_skills', 'tracker.mental_skills',
                       'tracker.regain_health', 'tracker.damage_health', 'tracker.damage_willpower',
                       'tracker.clan')

    allowed_targets = roller_targets + tracker_targets

    if target_page_name.lower() not in allowed_targets:
        log.error(f'*> Invalid pageEVNav target_page [ {target_page_name} ]')
        return

    elif target_page_name.lower() in tracker_targets:
        initial_page = await basicPageBuilder(interaction, 'Kindred Tracker', 'If a button is __Gray__ that means its non-functional', 'cyan')
        return_page, return_view = await tPB.trackerPageDecider(interaction, target_page_name.lower(), initial_page)
        return return_page, return_view

    elif target_page_name.lower() in roller_targets:
        initial_page = await basicPageBuilder(interaction, 'Kindred Roller', 'If a button is __Gray__ that means its non-functional', 'cyan')
        return_page, return_view = await rPB.rollerPageDecider(interaction, target_page_name.lower(), initial_page)
        return return_page, return_view


async def basicPageBuilder(interaction, page_title: str, page_description: str, page_color: str) -> Embed:
    # Makes the base embed
    base_page = Embed(title=page_title, description=page_description, colour=mC.embed_colors[f"{page_color.lower()}"])

    # Assigns basic user information
    user_info = {'user_name'  : interaction.user,
                 'user_id'    : interaction.user.id,
                 'user_avatar': interaction.user.display_avatar}

    # Finds name of the character
    character_name: str = await vU.getCharacterName(interaction)

    # Gets the character's avatar
    with sqlite3.connect(f'cogs//vampire//characters//{str(interaction.user.id)}//{character_name}//{character_name}.sqlite') as db:
        character_avatar = db.cursor().execute('SELECT imgURL from charInfo').fetchone()[0]

    # Adds the basic information to the page
    base_page.set_thumbnail(url=character_avatar)
    base_page.set_footer(text=f'{user_info["user_id"]}', icon_url=f'{user_info["user_avatar"]}')
    base_page.set_author(name=f'{user_info["user_name"]}', icon_url=f'{user_info["user_avatar"]}')
    base_page.add_field(name='Character Name', value=f'{character_name}', inline=False)

    # Returns Embed (now considered a "Page")
    return base_page

