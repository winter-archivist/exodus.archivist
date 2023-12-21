import trackerEmbeds as tE  # ! SHOULD BE GONE WHEN trackerNavigator() IS FINISHED
from zenlog import log
from discord import Embed

from misc.config import mainConfig as mC

from trackerMisc import placeholder_img

KTE_TEMPLATE_TITLE = '_KTE_TEMPLATE_TITLE_'
KTE_TEMPLATE_DESCRIPTION = '=KTE_TEMPLATE_DESCRIPTION='
KTE_TEMPLATE_COLOR = mC.embed_colors["mint"]
KTE_TEMPLATE = Embed(title=f'{KTE_TEMPLATE_TITLE}', description=f'{KTE_TEMPLATE_DESCRIPTION}', color=KTE_TEMPLATE_COLOR)


async def tevNav(interaction, target_embed) -> Embed:  # ? tevNav = Tracker Embed-View Navigator
    log.debug()
    allowed_targets = ('home', 'hp/wp', '')
    if target_embed.lower() in allowed_targets:
        KTE_TEMPLATE.clear_fields()
        if target_embed == 'home':
            return target_embed
        pass
    elif target_embed.lower() in allowed_targets:
        pass
    else:
        pass

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
