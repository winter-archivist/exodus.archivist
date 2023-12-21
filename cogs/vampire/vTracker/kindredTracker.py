import time
import discord
import sqlite3
import os as os
from zenlog import log
from discord import Embed
from discord.ui import View

from misc.utils import yamlUtils as yU
from misc.config import mainConfig as mC

import cogs.vampire.vTracker.trackerResources as tR


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

    return True


# ? Until Functional, the button will be gray
class KTV_HOME(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Home Page', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=1)
    async def home_button_callback(self, interaction, button):
        response_embed, response_view = await tevNav(interaction, 'home')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))

    @discord.ui.button(label='HP/WP Page', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.green, row=1)
    async def hpwp_page_button_callback(self, interaction, button):
        response_embed, response_view = await tevNav(interaction, 'hp/wp')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))

    @discord.ui.button(label='Hunger Page', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.green, row=1)
    async def hunger_page_button_callback(self, interaction, button):
        response_embed, response_view = await tevNav(interaction, 'hunger')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))

    @discord.ui.button(label='Attributes Page', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.green, row=2)
    async def attributes_page_button_callback(self, interaction, button):
        response_embed, response_view = await tevNav(interaction, 'attributes')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))

    @discord.ui.button(label='Skills Page', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.gray, row=2)
    async def skills_page_button_callback(self, interaction, button):
        response_embed, response_view = await tevNav(interaction, 'skills')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))

    @discord.ui.button(label='Extras Page', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.green, row=2)
    async def extras_page_button_callback(self, interaction, button):
        response_embed, response_view = await tevNav(interaction, 'extras')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))


class KTV_HPWP(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Home Page', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=1)
    async def home_button_callback(self, interaction, button):
        response_embed, response_view = await tevNav(interaction, 'home')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))

    @discord.ui.button(label='Damage Health', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.gray, row=1)
    async def health_damage_button_callback(self, interaction, button):
        response_embed, response_view = await tevNav(interaction, 'home')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))

    @discord.ui.button(label='Regain Health', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.gray, row=1)
    async def health_regain_button_callback(self, interaction, button):
        response_embed, response_view = await tevNav(interaction, 'home')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))

    @discord.ui.button(label='Damage Willpower', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.gray, row=1)
    async def willpower_damage_button_callback(self, interaction, button):
        response_embed, response_view = await tevNav(interaction, 'home')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))

    @discord.ui.button(label='Regain Willpower', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.gray, row=1)
    async def willpower_regain_button_callback(self, interaction, button):
        response_embed, response_view = await tevNav(interaction, 'home')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))


class KTV_HUNGER(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Home Page', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=1)
    async def home_button_callback(self, interaction, button):
        response_embed, response_view = await tevNav(interaction, 'home')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))

    @discord.ui.button(label='Hunt [Predator-Type]', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.gray, row=1)
    async def predhunt_button_callback(self, interaction, button):
        response_embed, response_view = await tevNav(interaction, 'home')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))

    @discord.ui.button(label='Hunt [Select]', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.gray, row=1)
    async def hunt_button_callback(self, interaction, button):
        response_embed, response_view = await tevNav(interaction, 'home')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))

    @discord.ui.button(label='Rouse', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.gray, row=1)
    async def rouse_button_callback(self, interaction, button):
        response_embed, response_view = await tevNav(interaction, 'home')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))


class KTV_ATTRIBUTE(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Home Page', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=1)
    async def home_button_callback(self, interaction, button):
        response_embed, response_view = await tevNav(interaction, 'home')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))

    @discord.ui.button(label='Roll', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.gray, row=1)
    async def roll_button_callback(self, interaction, button):
        # ! Send to Roller
        response_embed, response_view = await tevNav(interaction, 'home')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))


class KTV_SKILL(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Home Page', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=1)
    async def home_button_callback(self, interaction, button):
        response_embed, response_view = await tevNav(interaction, 'home')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))

    @discord.ui.button(label='Roll', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.gray, row=1)
    async def roll_button_callback(self, interaction, button):
        # ! Send to Roller
        response_embed, response_view = await tevNav(interaction, 'home')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))


class KTV_EXTRA(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Home Page', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=1)
    async def home_button_callback(self, interaction, button):
        response_embed, response_view = await tevNav(interaction, 'home')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))

    @discord.ui.button(label='Diablerie', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.gray, row=1)
    async def diablerie_button_callback(self, interaction, button):
        response_embed, response_view = await tevNav(interaction, 'home')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))

    @discord.ui.button(label='Remorse', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.gray, row=1)
    async def diablerie_button_callback(self, interaction, button):
        response_embed, response_view = await tevNav(interaction, 'home')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))

    @discord.ui.button(label='Path Rules', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.gray, row=1)
    async def path_rules_button_callback(self, interaction, button):
        response_embed, response_view = await tevNav(interaction, 'home')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))


async def tevNav(interaction, target_page) -> Embed and View:  # ? tevNav = Tracker Embed-View Navigator
    allowed_targets = ('home', 'hp/wp', 'hunger', 'attributes', 'skills', 'extras')
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
        return_view = KTV_HOME

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
                    return_embed.add_field(name='Select Page', value='', inline=False)
                    return_view = KTV_HOME
                elif target_page == 'hp/wp':
                    # ! Needs a hp/wp add/remove
                    # ? hc = health_count | wpc = willpower_count
                    hc_full: str = str(tR.health_full_emoji * int(cursor.execute('SELECT healthBase from health').fetchone()[0]))
                    hc_sup: str = str(tR.health_sup_emoji * int(cursor.execute('SELECT healthSUP from health').fetchone()[0]))
                    hc_agg: str = str(tR.health_agg_emoji * int(cursor.execute('SELECT healthAGG from health').fetchone()[0]))
                    wpc_full: str = str(tR.willpower_full_emoji * int(cursor.execute('SELECT willpowerBase from willpower').fetchone()[0]))
                    wpc_sup: str = str(tR.willpower_sup_emoji * int(cursor.execute('SELECT willpowerSUP from willpower').fetchone()[0]))
                    wpc_agg: str = str(tR.willpower_agg_emoji * int(cursor.execute('SELECT willpowerAGG from willpower').fetchone()[0]))

                    return_embed.add_field(name='Health', value=f'{hc_full}{hc_sup}{hc_agg}', inline=False)
                    return_embed.add_field(name='Willpower', value=f'{wpc_full}{wpc_sup}{wpc_agg}', inline=False)
                    return_view = KTV_HPWP
                elif target_page == 'hunger':
                    # ! Needs a Hunt Button (Lets use Selected Pool or Pred Pool)
                    hunger: str = str(cursor.execute('SELECT hunger from charInfo').fetchone()[0])
                    pred_type: str = str(cursor.execute('SELECT predator_type from charInfo').fetchone()[0])
                    return_embed.add_field(name='Hunger', value=f'{hunger}', inline=False)
                    return_embed.add_field(name='Predator Type', value=f'{pred_type}', inline=False)
                    return_view = KTV_HUNGER
                elif target_page == 'attributes':
                    # ! Needs to be affected by Impairment & Allow for Leveling
                    attributes = ('Strength', 'Dexterity', 'Stamina',
                                  'Charisma' , 'Manipulation', 'Composure',
                                  'Intelligence', 'Wits', 'Resolve')

                    for_var = 0
                    for x in attributes:
                        if for_var / 3 in (1, 2):
                            return_embed.add_field(name='', value='', inline=False)
                        count = int(cursor.execute(f'SELECT {attributes[for_var].lower()} from charAttributes').fetchone()[0])
                        emojis = f'{count * tR.dot_full_emoji} {abs(count - 5) * tR.dot_empty_emoji}'

                        return_embed.add_field(name=f'{attributes[for_var]}', value=f'{emojis}', inline=True)
                        for_var += 1

                    return_view = KTV_ATTRIBUTE
                elif target_page == 'skills':
                    return_view = KTV_SKILL
                elif target_page == 'extras':
                    # ! Needs Diablerie Button [Clan & Generation]
                    # ! Needs Stain/Remorse Button [Humanity & Stains]
                    # ! Needs PoE Rule Checker [Path of Enlightenment]
                    clan: str = cursor.execute(f'SELECT clan from charInfo').fetchone()[0]
                    gen: int = cursor.execute(f'SELECT generation from charInfo').fetchone()[0]
                    bp: int = cursor.execute(f'SELECT blood_potency FROM charInfo').fetchone()[0]
                    humanity: int = cursor.execute(f'SELECT humanity from charInfo').fetchone()[0]
                    stains: int = cursor.execute(f'SELECT stains from charInfo').fetchone()[0]
                    path_of_enlightenment = cursor.execute(f'SELECT path_of_enlightenment from charInfo').fetchone()[0]
                    return_embed.add_field(name='Clan', value=f'{clan}', inline=True)

                    return_embed.add_field(name='', value=f'', inline=False)

                    return_embed.add_field(name='Generation', value=f'{gen * tR.dot_full_emoji}', inline=True)
                    return_embed.add_field(name='Blood Potency', value=f'{bp * tR.dot_full_emoji}', inline=True)

                    return_embed.add_field(name='', value=f'', inline=False)

                    return_embed.add_field(name='Humanity', value=f'{humanity * tR.dot_full_emoji} {stains * tR.dot_empty_emoji}', inline=True)
                    return_embed.add_field(name='Path of Enlightenment', value=f'{path_of_enlightenment}', inline=True)
                    return_view = KTV_EXTRA
            except sqlite3.Error as e:
                log.error(f'**> tevNav | SQLITE3 ERROR | {e}')

        log.debug(f'> tevNav Success [ {target_page} ]')
        return return_embed, return_view
    elif target_page.lower() not in allowed_targets:
        log.error(f'*> Invalid tevNav target_page [ {target_page} ]')
    else:
        log.error(f'**> tevNav had received an incredibly invalid target_page. [ {target_page} ]')

"""
async def trackerEmbedInitialize(interaction, character_name, target_embed):
    # Make Owner info another database, get user's profile picture
    user_avatar = interaction.user.display_avatar
    user_name = interaction.user
    user_id = interaction.user.id

    clan = 1
    generation = 1
    humanity = 1
    hunger = 1
    health = 1
    willpower = 1
    predtype = 1
    str = 1
    dex = 1
    sta = 1
    cha = 1
    man = 1
    com = 1
    inte = 1
    wit = 1
    res = 1
    disci = 1
    target_embed.set_author(name=f'{user_name}', icon_url=f'{user_avatar}')
    target_embed.set_footer(text=f'{user_id}', icon_url=f'{user_avatar}')
    target_embed.set_thumbnail(url=placeholder_img)
    target_embed.set_field_at(index=0, name='Character Name', value=f'{character_name}', inline=False)

    tE.extra_kte.set_field_at(index=1, name='Clan', value=f'{clan}', inline=False)
    tE.extra_kte.set_field_at(index=2, name='Generation', value=f'{generation}', inline=False)
    tE.extra_kte.set_field_at(index=3, name='Humanity', value=f'{humanity}', inline=False)

    health_full_emoji = ' <:full_hp:1186583370382188574> '; health_full_count = 2
    health_sup_emoji = ' <:sup_hp:1186583396068102154> '; health_sup_count = 3
    health_agg_emoji = ' <:agg_hp:1186583405631123538> '; health_agg_count = 4

    tE.hpwp_kte.set_field_at(index=1, name='Health', value=f'{health_full_emoji * health_full_count} {health_sup_emoji * health_sup_count} {health_agg_emoji * health_agg_count}', inline=False)

    willpower_full_emoji = ' <:full_wp:1186586608712028160> '; willpower_full_count = 2
    willpower_sup_emoji = ' <:sup_wp:1186586616798650470> '; willpower_sup_count = 3
    willpower_agg_emoji = ' <:agg_wp:1186586594568851506> '; willpower_agg_count = 4
    tE.hpwp_kte.set_field_at(index=2, name='Willpower', value=f'{willpower_full_emoji * willpower_full_count} {willpower_sup_emoji * willpower_sup_count} {willpower_agg_emoji * willpower_agg_count}', inline=False)

    tE.hunger_kte.set_field_at(index=1, name='Hunger', value=f'{hunger}', inline=False)
    tE.hunger_kte.set_field_at(index=2, name='Predator Type', value=f'{predtype}', inline=False)

    tE.attributes_kte.set_field_at(index=1, name='Strength', value=f'{str}', inline=False)
    tE.attributes_kte.set_field_at(index=2, name='Dexterity', value=f'{dex}', inline=False)
    tE.attributes_kte.set_field_at(index=3, name='Stamina', value=f'{sta}', inline=False)
    tE.attributes_kte.set_field_at(index=4, name='Charisma', value=f'{cha}', inline=False)
    tE.attributes_kte.set_field_at(index=5, name='Manipulation', value=f'{man}', inline=False)
    tE.attributes_kte.set_field_at(index=6, name='Composure', value=f'{com}', inline=False)
    tE.attributes_kte.set_field_at(index=7, name='Intelligence', value=f'{inte}', inline=False)
    tE.attributes_kte.set_field_at(index=8, name='Wits', value=f'{wit}', inline=False)
    tE.attributes_kte.set_field_at(index=9, name='Resolve', value=f'{res}', inline=False)

    tE.disciplines_kte.set_field_at(index=1, name='Disciplines', value=f'{disci}', inline=False)
"""

"""
disciplines_kte = Embed(title='Kindred Tracker | Disciplines', description='', color=mc.embed_colors["red"])
disciplines_kte.add_field(name='Character Name', value='INSERT_VALUE', inline=False)
disciplines_kte.add_field(name='Disciplines', value='INSERT_VALUE', inline=False)
"""
