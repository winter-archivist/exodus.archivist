import sqlite3
from discord import Embed
from discord.ui import View
from zenlog import log

import misc.config.mainConfig as mC
import cogs.vampire.vMisc.vampireUtils as vU
import cogs.vampire.vTracker.trackerViews as tV


async def trackerPageDecider(interaction, target_page_name, initial_page) -> Embed and View:
    try:
        character_name = await vU.getCharacterName(interaction)
        with sqlite3.connect(f'cogs//vampire//characters//{str(interaction.user.id)}//{character_name}//{character_name}.sqlite') as db:
            cursor = db.cursor()
            match target_page_name:
                case 'tracker.home':
                    return_page, return_view = await homePageBuilder(initial_page)
                case 'tracker.hp/wp':
                    return_page, return_view = await hpwpPageBuilder(initial_page, cursor)

                case 'tracker.hunger':
                    return_page, return_view = await hungerPageBuilder(initial_page, cursor)

                case 'tracker.attributes':
                    return_page, return_view = await attributePageBuilder(initial_page, cursor)
                case 'tracker.discipline':
                    return_page, return_view = await disciplinePageBuilder(initial_page, cursor)
                case 'tracker.extras':
                    return_page, return_view = await extrasPageBuilder(initial_page, cursor)

                case 'tracker.skills':
                    return_page, return_view = await skillsPageBuilder(initial_page, cursor)
                case 'tracker.physical_skills':
                    return_page, return_view = await physicalSkillsPageBuilder(initial_page, cursor)
                case 'tracker.social_skills':
                    return_page, return_view = await socialSkillsPageBuilder(initial_page, cursor)
                case 'tracker.mental_skills':
                    return_page, return_view = await mentalSkillsPageBuilder(initial_page, cursor)

                case 'tracker.regain_health':
                    return_page, return_view = await regainhealthPageBuilder(initial_page, cursor)
                case 'tracker.damage_health':
                    return_page, return_view = await damagehealthPageBuilder(initial_page, cursor)
                case 'tracker.damage_willpower':
                    return_page, return_view = await damagewillpowerPageBuilder(initial_page, cursor)

                case 'tracker.clan':
                    return_page, return_view = await clanPageBuilder(initial_page, cursor)

                case _:
                    log.error('**> Provided target_page_name does not exist.')
                    raise Exception('Provided target_page_name does not exist.')
        return return_page, return_view
    except sqlite3.Error as e:
        log.error(f'**> trackerPageDecider | SQLITE3 ERROR | {e}')


async def homePageBuilder(return_page):
    return_page.add_field(name='Select Page', value='', inline=False)
    return_view = tV.KTV_HOME
    return return_page, return_view


async def hpwpPageBuilder(return_embed, cursor):
    # ? hc = health_count | wpc = willpower_count
    hc_base: int = int(cursor.execute('SELECT healthBase from health').fetchone()[0])
    hc_sup: int = int(cursor.execute('SELECT healthSUP from health').fetchone()[0])
    hc_agg: int = int(cursor.execute('SELECT healthAGG from health').fetchone()[0])
    wpc_base: int = int(cursor.execute('SELECT willpowerBase from willpower').fetchone()[0])
    wpc_sup: int = int(cursor.execute('SELECT willpowerSUP from willpower').fetchone()[0])
    wpc_agg: int = int(cursor.execute('SELECT willpowerAGG from willpower').fetchone()[0])

    actual_health = hc_base - hc_sup - hc_agg
    full_health = str(mC.HEALTH_FULL_EMOJI * actual_health)
    sup_health = str(mC.HEALTH_SUP_EMOJI * hc_sup)
    agg_health = str(mC.HEALTH_AGG_EMOJI * hc_agg)

    if hc_sup == hc_base and hc_agg > 1:
        sup_health = str(mC.HEALTH_SUP_EMOJI * int(hc_sup - hc_agg))

    actual_willpower = wpc_base - wpc_sup - wpc_agg
    full_willpower = str(mC.WILLPOWER_FULL_EMOJI * actual_willpower)
    sup_willpower = str(mC.WILLPOWER_SUP_EMOJI * wpc_sup)
    agg_willpower = str(mC.WILLPOWER_AGG_EMOJI * wpc_agg)

    return_embed.add_field(name='Health', value=f'{full_health}{sup_health}{agg_health}', inline=False)
    return_embed.add_field(name='Willpower', value=f'{full_willpower}{sup_willpower}{agg_willpower}', inline=False)
    return_view = tV.KTV_HPWP
    return return_embed, return_view


async def hungerPageBuilder(return_embed, cursor):
    hunger: int = int(cursor.execute('SELECT hunger from charInfo').fetchone()[0])
    predator_type: str = str(cursor.execute('SELECT predator_type from charInfo').fetchone()[0])
    supported_pred_types: tuple = ('SECRET_PRED_TYPE', 'Grim Reaper', 'Sandman', 'Cryptid', 'Alleycat',
                                   'Grave Robber', 'Trapdoor')

    if predator_type not in supported_pred_types:
        log.error('**> Bad predator_type given to hungerPageBuilder()')
        return

    # pt = predator type
    match predator_type:
        case 'SECRET_PRED_TYPE':
            pt_pool: str = ''  # Mechanical Stuff
            pt_desc: str = ''
            pt_disciplines: str = ''  # The potential disciplines gained from the predator type
            pt_spec: str = ''  # Specialty/ies from pt
            pt_merit: str = ''  # Advantages/Merits given by pt
            pt_flaws: str = ''  # Flaws given by pt

        case 'Grim Reaper':
            pt_pool: str = 'Intelligence + Awareness/Medicine in order to find victims.'
            pt_desc: str = ('Hunting inside hospice care facilities, assisted living homes, and other places where those'
                            ' who are near death reside. Grim Reapers are constantly on the move in an effort to locate '
                            'new victims near the end of their lives to feed from. Hunting in this style may also earn a'
                            ' taste for specific diseases making them easier to identify. ')
            pt_disciplines: str = 'Auspex or Oblivion (Necromancy/Obtenebration)'
            pt_spec: str = 'Awareness (Death) or Larceny (Forgery)'
            pt_merit: str = 'One dot of Allies or Influence associated with the medical community & Gain 1 Humanity'
            pt_flaws: str = '(•) Prey Exclusion (Healthy Mortals)'

        case 'Sandman':
            pt_pool: str = 'Dexterity + Stealth is for casing a location, breaking in and feeding without leaving a trace.'
            pt_desc: str = ('If they never wake during the feed it never happened, right? Sandman prefers to hunt on '
                            'sleeping mortals than anyone else by using stealth or Disciplines to feed from their '
                            'victims they are rarely caught in the act, though when they are, problems are sure to occur'
                            '. Maybe they were anti-social in life or perhaps they find the route of seduction or '
                            'violence too much for them and find comfort in the silence of this feeding style. ')
            pt_disciplines: str = 'Auspex or Obfuscate'
            pt_spec: str = 'Medicine (Anesthetics) or Stealth (Break-in)'
            pt_merit: str = 'Gain one dot of Resources'
            pt_flaws: str = 'None!'

        case 'Cryptid':
            pt_pool: str = ''
            pt_desc: str = ('Nobody believes in vampires, right? Well, not "nobody", exactly. Know what nobody-nobody '
                            'believes in? Aliens, chupacabras, and sasquatches. You have concocted some incredibly '
                            'fanciful identity for yourself in which you present yourself as some obscure piece of '
                            'occult apocrypha. True Believers are so ready to believe in ghosts or mermaids or whatever,'
                            ' that it will never occur to them you\')re a vampire. Some even seek to serve their '
                            'paranormal masters. "After the probe, the alien took blood samples." "The chupacabra jumped'
                            ' out of nowhere! It got my dog!" "The succubus appears at midnight, and it feels sooo good!"'
                            ' "The Delaware Water Gap Mermaid? That\'s just a tourist legend, still, be careful if you '
                            'swim or boat at night."')
            pt_disciplines: str = 'Obfuscate, Dominate, or Clan Specific'
            pt_spec: str = 'Occult (Cryptids) or Performance (Impersonating Urban Legends)'
            pt_merit: str = 'Three Dots to spend between Herd and/or Retainer'
            pt_flaws: str = 'Stalkers & Suspect'

        case 'Alleycat':
            pt_pool: str = 'Strength + Brawl is to take blood by force or threat. Wits + Streetwise can be used to find criminals as if a vigilante figure.'
            pt_desc: str = ('Those who find violence to be the quickest way to get what they want might gravitate '
                            'towards this hunting style. Alleycats are a vampire who feeds by brute force and outright '
                            'attack and feeds from whomever they can when they can. Intimidation is a route easily taken'
                            ' to make their victims cower or even Dominating the victims to not report the attack or '
                            'mask it as something else entirely.')
            pt_disciplines: str = 'Celerity or Potence'
            pt_spec: str = 'Intimidation (Stickups) or Brawl (Grappling)'
            pt_merit: str = 'Gain three dots of Criminal Contacts'
            pt_flaws: str = 'Lose 1 Humanity'

        case 'Grave Robber':
            pt_pool: str = ('Resolve + Medicine for sifting through the dead for a body with blood. Manipulation + '
                            'Insight for moving among miserable mortals.')
            pt_desc: str = ('Similar to Baggers these kindred understand there\'s no good in wasting good blood, even if'
                            ' others cannot consume it. Often they find themselves digging up corpses or working or '
                            'mortuaries to obtain their bodies, yet regardless of what the name suggests, they prefer '
                            'feeding from mourners at a gravesite or a hospital. This Predator Type often requires a '
                            'haven or other connections to a church, hospital, or morgue as a way to obtain the bodies. ')
            pt_disciplines: str = 'Fortitude or Oblivion (Necromancy)'
            pt_spec: str = 'Occult (Grave Rituals) or Medicine (Cadavers)'
            pt_merit: str = 'Feeding Merit (•••) Iron Gullet & Haven Advantage (•)'
            pt_flaws: str = 'Herd Flaw: (••) Obvious Predator'

        case 'Trapdoor':
            pt_pool: str = ('Charisma + Stealth for the victims that enter expecting a fun-filled night. Dexterity + '
                            'Stealth to feed upon trespassers. Wits + Awareness + Haven dots is used to navigate the '
                            'maze of the den itself. ')
            pt_desc: str = ('Much like the spider, this vampire builds a nest and lures their prey inside. Be it an '
                            'amusement park, an abandoned house, or an underground club, the victim comes to them. '
                            'There the trapdoor might only play with their mind and terrorize them, imprison them to '
                            'drain them slowly, or take a deep drink and then send them home. ')
            pt_disciplines: str = 'Protean or Obfuscate'
            pt_spec: str = 'Persuasion (Marketing) or Stealth (Ambushes or Traps)'
            pt_merit: str = 'Gain one dot of Haven & Gain one dot of either Retainers or Herd, or a second Haven dot.'
            pt_flaws: str = 'Gain one Haven Flaw, either (•) Creepy or (•) Haunted.'

        case _:
            log.error('**> Bad predator_type #2')
            return

    return_embed.add_field(name='Hunger', value=f'{hunger * mC.HUNGER_EMOJI}', inline=True)
    return_embed.add_field(name='Predator Type', value=f'{predator_type}', inline=True)
    return_embed.add_field(name='PT Pool', value=f'{pt_pool}', inline=False)
    return_embed.add_field(name='PT Description', value=f'{pt_desc}', inline=False)
    return_embed.add_field(name='PT Discipline(s)', value=f'{pt_disciplines}', inline=True)
    return_embed.add_field(name='PT Specialty(ies)', value=f'{pt_spec}', inline=True)
    return_embed.add_field(name='PT Merit(s)', value=f'{pt_merit}', inline=True)
    return_embed.add_field(name='PT Flaw(s)', value=f'{pt_flaws}', inline=True)
    return_view = tV.KTV_HUNGER
    return return_embed, return_view


async def attributePageBuilder(return_embed, cursor):
    # ! Allow for Leveling
    # TODO: Make this also apply to skills (I want to die)
    attributes = ('Strength', 'Dexterity', 'Stamina',
                  'Charisma', 'Manipulation', 'Composure',
                  'Intelligence', 'Wits', 'Resolve')

    physical_impairment_flag: bool = False
    health_base: int = int(cursor.execute('SELECT healthBase from health').fetchone()[0])
    health_sup_damage: int = int(cursor.execute('SELECT healthSUP from health').fetchone()[0])
    if health_base <= health_sup_damage:
        return_embed.add_field(name='Physically Impaired.', value='-1 to Physical Dice Pools', inline=False)
        physical_impairment_flag = True

    mental_impairment_flag: bool = False
    willpower_base: int = int(cursor.execute('SELECT willpowerBase from willpower').fetchone()[0])
    willpower_sup_damage: int = int(cursor.execute('SELECT willpowerSUP from willpower').fetchone()[0])
    if willpower_base <= willpower_sup_damage:
        return_embed.add_field(name='Mentally Impaired', value='-1 to Social & Mental Dice Pools', inline=False)
        mental_impairment_flag = True

    for_var = 0
    for x in attributes:
        if for_var / 3 in (1, 2):
            return_embed.add_field(name='', value='', inline=False)
        count = int(cursor.execute(f'SELECT {attributes[for_var].lower()} from charAttributes').fetchone()[0])

        # don't like this, but will cope
        if physical_impairment_flag is True or mental_impairment_flag is True:
            if attributes[for_var].lower() in ('strength', 'dexterity', 'stamina'):
                count -= 1  # Removes one from PHYSICAL attributes since the character is PHYSICALLY impaired.

            if attributes[for_var].lower() in ('charisma', 'manipulation', 'composure', 'intelligence', 'wits', 'resolve'):
                count -= 1  # Removes one from MENTAL & SOCIAL attributes since the character is MENTALLY impaired.

        emojis = f'{count * mC.DOT_FULL_EMOJI} {abs(count - 5) * mC.DOT_EMPTY_EMOJI}'

        return_embed.add_field(name=f'{attributes[for_var]}', value=f'{emojis}', inline=True)
        for_var += 1

    return_view = tV.KTV_ATTRIBUTE
    return return_embed, return_view


async def skillsPageBuilder(return_embed, cursor):
    # ! Needs to allow for Leveling
    return_view = tV.KTV_SKILL
    return return_embed, return_view


async def physicalSkillsPageBuilder(return_embed, cursor):
    physical_skills = ('Athletics', 'Brawl', 'Craft', 'Drive', 'Firearms', 'Larceny', 'Melee', 'Stealth', 'Survival')
    for_var = 0
    for x in physical_skills:
        if for_var / 3 in (1, 2):
            return_embed.add_field(name='', value='', inline=False)
        count = int(
            cursor.execute(f'SELECT {physical_skills[for_var].lower()} from physicalSkills').fetchone()[0])
        emojis = f'{count * mC.DOT_FULL_EMOJI} {abs(count - 5) * mC.DOT_EMPTY_EMOJI}'

        return_embed.add_field(name=f'{physical_skills[for_var]}', value=f'{emojis}', inline=True)
        for_var += 1
    return_view = tV.KTV_SKILL
    return return_embed, return_view


async def socialSkillsPageBuilder(return_embed, cursor):
    social_skills = ('Animal_Ken', 'Etiquette', 'Insight', 'Intimidation', 'Leadership', 'Performance', 'Persuasion', 'Streetwise', 'Subterfuge')
    for_var = 0
    for x in social_skills:
        if for_var / 3 in (1, 2):
            return_embed.add_field(name='', value='', inline=False)
        count = int(
            cursor.execute(f'SELECT {social_skills[for_var].lower()} from socialSkills').fetchone()[0])
        emojis = f'{count * mC.DOT_FULL_EMOJI} {abs(count - 5) * mC.DOT_EMPTY_EMOJI}'

        return_embed.add_field(name=f'{social_skills[for_var]}', value=f'{emojis}', inline=True)
        for_var += 1
    return_view = tV.KTV_SKILL
    return return_embed, return_view


async def mentalSkillsPageBuilder(return_embed, cursor):
    mental_skills = ('Academics', 'Awareness', 'Finance', 'Investigation', 'Medicine', 'Occult', 'Politics', 'Science', 'Technology')
    for_var = 0
    for x in mental_skills:
        if for_var / 3 in (1, 2):
            return_embed.add_field(name='', value='', inline=False)
        count = int(
            cursor.execute(f'SELECT {mental_skills[for_var].lower()} from mentalSkills').fetchone()[0])
        emojis = f'{count * mC.DOT_FULL_EMOJI} {abs(count - 5) * mC.DOT_EMPTY_EMOJI}'

        return_embed.add_field(name=f'{mental_skills[for_var]}', value=f'{emojis}', inline=True)
        for_var += 1
    return_view = tV.KTV_SKILL
    return return_embed, return_view


async def disciplinePageBuilder(return_embed, cursor):
    disciplines = ('Obfuscate', 'Animalism', 'Potence', 'Dominate', 'Auspex', 'Protean', 'Presence', 'Fortitude', 'Thin_Blood_Alchemy',
                   'Blood_Sorc', 'Chemeristry', 'Seven', 'Myr', 'Selena', 'Nyct1', 'Nyct2', 'Iilta', 'Elijah')
    for_var = 0
    for x in disciplines:
        if for_var / 3 in (1, 2):
            return_embed.add_field(name='', value='', inline=False)
        count = int(cursor.execute(f'SELECT {disciplines[for_var].lower()} from disciplines').fetchone()[0])
        emojis = f'{count * mC.DOT_FULL_EMOJI} {abs(count - 5) * mC.DOT_EMPTY_EMOJI}'

        if count <= 0:
            pass
        else:
            return_embed.add_field(name=f'{disciplines[for_var]}', value=f'{emojis}', inline=True)
        for_var += 1

    return_view = tV.KTV_DISCIPLINE
    return return_embed, return_view


async def extrasPageBuilder(return_embed, cursor):
    # ! Needs Diablerie Button [Clan & Generation]
    # ! Needs Stain/Remorse Button [Humanity & Stains]
    # ! Needs PoE Rule Checker [Path of Enlightenment]
    clan: str = cursor.execute(f'SELECT clan from charInfo').fetchone()[0]
    gen: int = cursor.execute(f'SELECT generation from charInfo').fetchone()[0]
    bp: int = cursor.execute(f'SELECT blood_potency FROM charInfo').fetchone()[0]
    humanity: int = cursor.execute(f'SELECT humanity from charInfo').fetchone()[0]
    stains: int = cursor.execute(f'SELECT stains from charInfo').fetchone()[0]
    path_of_enlightenment = cursor.execute(f'SELECT path_of_enlightenment from charInfo').fetchone()[0]
    # THIS IS JUST FOR MY PERSONAL CHRONICLE
    if clan == 'SECRET_CLAN':
        return_embed.add_field(name='Clan', value=f'Beyond The Eye of Saulot', inline=True)
    else:
        return_embed.add_field(name='Clan', value=f'{clan}', inline=True)

    return_embed.add_field(name='', value=f'', inline=False)

    # THIS IS JUST FOR MY PERSONAL CHRONICLE
    if gen == 7:
        return_embed.add_field(name='Generation', value=f'Beyond The Eye of Saulot', inline=True)
    else:
        return_embed.add_field(name='Generation', value=f'{gen * mC.DOT_FULL_EMOJI}', inline=True)

    # THIS IS JUST FOR MY PERSONAL CHRONICLE
    if bp == 4:
        return_embed.add_field(name='Blood Potency', value=f'Beyond The Eye of Saulot', inline=True)
    else:
        return_embed.add_field(name='Blood Potency', value=f'{bp * mC.HUNGER_EMOJI}', inline=True)

    return_embed.add_field(name='', value=f'', inline=False)

    return_embed.add_field(name='Humanity', value=f'{humanity * mC.DOT_FULL_EMOJI} {stains * mC.DOT_EMPTY_EMOJI}', inline=True)
    # THIS IS JUST FOR MY PERSONAL CHRONICLE
    if path_of_enlightenment == 'SECRET_PATH':
        return_embed.add_field(name='Path of Enlightenment', value=f'Beyond The Eye of Saulot', inline=True)
    else:
        return_embed.add_field(name='Path of Enlightenment', value=f'{path_of_enlightenment}', inline=True)
    return_view = tV.KTV_EXTRA
    return return_embed, return_view


async def regainhealthPageBuilder(return_embed, cursor):
    # ? hc = health_count
    hc_base: int = int(cursor.execute('SELECT healthBase from health').fetchone()[0])
    hc_sup: int = int(cursor.execute('SELECT healthSUP from health').fetchone()[0])
    hc_agg: int = int(cursor.execute('SELECT healthAGG from health').fetchone()[0])

    actual_health = hc_base - hc_sup - hc_agg
    full_health = str(mC.HEALTH_FULL_EMOJI * actual_health)
    sup_health = str(mC.HEALTH_SUP_EMOJI * hc_sup)
    agg_health = str(mC.HEALTH_AGG_EMOJI * hc_agg)

    if hc_sup == hc_base and hc_agg > 1:
        sup_health = str(mC.HEALTH_SUP_EMOJI * int(hc_sup - hc_agg))

    return_embed.add_field(name='Health', value=f'{full_health}{sup_health}{agg_health}', inline=False)

    return_view = tV.KTV_HPREGAIN
    return return_embed, return_view


async def damagehealthPageBuilder(return_embed, cursor):
    # ? hc = health_count
    hc_base: int = int(cursor.execute('SELECT healthBase from health').fetchone()[0])
    hc_sup: int = int(cursor.execute('SELECT healthSUP from health').fetchone()[0])
    hc_agg: int = int(cursor.execute('SELECT healthAGG from health').fetchone()[0])

    actual_health = hc_base - hc_sup - hc_agg
    full_health = str(mC.HEALTH_FULL_EMOJI * actual_health)
    sup_health = str(mC.HEALTH_SUP_EMOJI * hc_sup)
    agg_health = str(mC.HEALTH_AGG_EMOJI * hc_agg)

    if hc_sup == hc_base and hc_agg > 1:
        sup_health = str(mC.HEALTH_SUP_EMOJI * int(hc_sup - hc_agg))

    return_embed.add_field(name='Health', value=f'{full_health}{sup_health}{agg_health}', inline=False)

    return_view = tV.KTV_HPDAMAGE
    return return_embed, return_view


async def damagewillpowerPageBuilder(return_embed, cursor):
    # ? wpc = willpower_count
    wpc_base: int = int(cursor.execute('SELECT willpowerBase from willpower').fetchone()[0])
    wpc_sup: int = int(cursor.execute('SELECT willpowerSUP from willpower').fetchone()[0])
    wpc_agg: int = int(cursor.execute('SELECT willpowerAGG from willpower').fetchone()[0])

    actual_willpower = wpc_base - wpc_sup - wpc_agg
    full_willpower = str(mC.WILLPOWER_FULL_EMOJI * actual_willpower)
    sup_willpower = str(mC.WILLPOWER_SUP_EMOJI * wpc_sup)
    agg_willpower = str(mC.WILLPOWER_AGG_EMOJI * wpc_agg)

    return_embed.add_field(name='Willpower', value=f'{full_willpower}{sup_willpower}{agg_willpower}', inline=False)
    return_view = tV.KTV_WPDAMAGE
    return return_embed, return_view


async def clanPageBuilder(return_embed, cursor):
    character_clan: str = str(cursor.execute('SELECT clan from charInfo').fetchone()[0])
    supported_clans = ('ExampleCase', 'True Brujah', 'Tremere', 'REMOVED_UNTIL_CLAN_REVEAL', 'Tzimisce', 'Nosferatu',
                       'Thin-Blood', 'Ravnos', 'Nagaraja')
    if character_clan not in supported_clans:
        log.error(f'**> character_clan provided is not supported.')
        return
    clan_bane_two = 'False'
    match character_clan:
        case 'ExampleCase':
            clan_description: str = ''  # "Internal" Desc
            clan_reputation: str = ''  # "Outside" Desc
            clan_status: str = ''  # High/Low Clan
            clan_compulsion: str = ''  # Mechanical Stuff
            clan_bane: str = ''  # Mechanical Stuff #2
            clan_bane_two: str = ''  # Mechanical Stuff #3
            clan_disciplines: str = ''  # What Players can expect those in the clan to have
        case 'True Brujah':
            clan_description: str = ''
            clan_reputation: str = ''
            clan_status: str = ''
            clan_compulsion: str = ''
            clan_bane: str = ''
            clan_bane_two: str = ''
            clan_disciplines: str = ''
        case 'Tremere':
            clan_description: str = ''
            clan_reputation: str = ''
            clan_status: str = ''
            clan_compulsion: str = ''
            clan_bane: str = ''
            clan_bane_two: str = ''
            clan_disciplines: str = ''
        case 'REMOVED_UNTIL_CLAN_REVEAL':
            clan_description: str = 'REMOVED_UNTIL_CLAN_REVEAL'
            clan_reputation: str = 'REMOVED_UNTIL_CLAN_REVEAL'
            clan_status: str = 'REMOVED_UNTIL_CLAN_REVEAL'
            clan_compulsion: str = ''
            clan_bane: str = 'REMOVED_UNTIL_CLAN_REVEAL'
            clan_bane_two: str = 'REMOVED_UNTIL_CLAN_REVEAL'
            clan_disciplines: str = ''
        case 'Tzimisce':
            clan_description: str = ''
            clan_reputation: str = ''
            clan_status: str = ''
            clan_compulsion: str = ''
            clan_bane: str = ''
            clan_bane_two: str = ''
            clan_disciplines: str = ''
        case 'Nosferatu':
            clan_description: str = ''
            clan_reputation: str = ''
            clan_status: str = ''
            clan_compulsion: str = ''
            clan_bane: str = ''
            clan_bane_two: str = ''
            clan_disciplines: str = ''
        case 'Thin-Blood':
            clan_description: str = ''
            clan_reputation: str = ''
            clan_status: str = ''
            clan_compulsion: str = ''
            clan_bane: str = ''
            clan_bane_two: str = ''
            clan_disciplines: str = ''
        case 'Ravnos':
            clan_description: str = ''
            clan_reputation: str = ''
            clan_status: str = 'Low Clan'
            clan_compulsion: str = ('Tempting Fate: The vampire is driven by their Blood to court danger. '
                                    'Haunted as they are by righteous fire burning its way up their lineage, why not? '
                                    'The next time the vampire is faced with a problem to solve, any attempt at a '
                                    'solution short of the most daring or dangerous incurs a two-dice penalty. '
                                    '(Suitably flashy and risky attempts can even merit bonus dice for this occasion.) '
                                    'The Daredevil is free to convince any fellows to do things their way, but is just '
                                    'as likely to go at it alone. The Compulsion persists until the problem is solved or'
                                    ' further attempts become impossible.')
            clan_bane: str = ('Doomed: The Ravnos are doomed. The sun’s fire that incinerated their founder rages through '
                              'the Blood of the clan, erupting from their very flesh if they ever settle down for long. '
                              'If they slumber in the same place more than once in four nights, roll a number of dice '
                              'equal to their Bane Severity. They receive aggravated damage equal to the number of 10’s '
                              '(critical results) rolled as they are scorched from within. This happens every time they '
                              'spend the day in a location they’ve already slumbered less than four days before. Two '
                              'resting places need to be at least a mile apart to avoid triggering the Bane. '
                              'Furthermore, a mobile haven, such as a movers’ truck, is safe so long as the place where '
                              'the truck is parked is at least a mile from the last location')
            clan_bane_two: str = ('Unbirth Name: If a Ravnos’ unbirth name is used against them, the name-wielding '
                                  'opponent receives a bonus equal to the Ravnos’ Bane Severity to resist their '
                                  'Discipline powers. Additionally, the Ravnos affected receives the same penalty to '
                                  'resist supernatural powers used by the opponent.[')
            clan_disciplines: str = 'Chemeristry + Charlatan (Auspex, Presence), Vulture (Obfuscate, Animalism), Trickster (Presence, Obfuscate), Nomad (Animalism, Fortitude))'
        case 'Nagaraja':
            clan_description: str = ('The Nagaraja, The Clan of Necromancers, are unlike other Kindred in that they must '
                                     'consume flesh, making them among the most reviled and "unnatural" of the bloodlines. '
                                     'They have pointed, irregular teeth, rather than the usual retractable fangs. '
                                     'This means that they seldom smile, and they tend to speak quietly around mortals – unless they plan to eat them. ')
            clan_reputation: str = ('Outliers & Death-Worshipers, most refuse to work with the Camarilla, '
                                    'some work with Anarchs closely, but more work outside of the two primary sects, '
                                    'their realm is that of the Autarkis, the Independent.')
            clan_status: str = 'Low Clan'
            clan_compulsion: str = 'Technically WIP'
            clan_bane: str = 'Technically WIP'
            clan_disciplines: str = 'Auspex, Dominate, Nihilistics'
        case _:
            log.error(f'**> Bad character_clan retrieved in clanPageBuilder(), {character_clan}')
            return
    return_embed.add_field(name='Clan', value=f'{character_clan}', inline=True)

    return_embed.add_field(name='', value='', inline=False)
    return_embed.add_field(name='Clan Description', value=f'{clan_description}', inline=True)

    return_embed.add_field(name='', value='', inline=False)
    return_embed.add_field(name='Clan Reputation', value=f'{clan_reputation}', inline=True)
    return_embed.add_field(name='Clan "Status"', value=f'{clan_status}', inline=True)

    return_embed.add_field(name='', value='', inline=False)
    return_embed.add_field(name='Clan Compulsion', value=f'{clan_compulsion}', inline=True)
    return_embed.add_field(name='Clan Bane', value=f'{clan_bane}', inline=True)
    if clan_bane_two != 'False':
        return_embed.add_field(name='Clan Bane #2', value=f'{clan_bane_two}', inline=True)
    return_embed.add_field(name='Clan Disciplines', value=f'{clan_disciplines}', inline=True)

    return_view = tV.KTV_CLAN
    return return_embed, return_view
