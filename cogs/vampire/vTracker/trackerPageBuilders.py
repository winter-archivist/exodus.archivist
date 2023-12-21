import cogs.vampire.vTracker.trackerViews as tV
import misc.config.mainConfig as mC


async def homePageBuilder(return_embed):
    return_embed.add_field(name='Select Page', value='', inline=False)
    return_view = tV.KTV_HOME
    return return_embed, return_view


async def hpwpPageBuilder(return_embed, cursor):
    # ! Needs a hp/wp add/remove
    # ? hc = health_count | wpc = willpower_count
    hc_full: str = str(mC.health_full_emoji * int(cursor.execute('SELECT healthBase from health').fetchone()[0]))
    hc_sup: str = str(mC.health_sup_emoji * int(cursor.execute('SELECT healthSUP from health').fetchone()[0]))
    hc_agg: str = str(mC.health_agg_emoji * int(cursor.execute('SELECT healthAGG from health').fetchone()[0]))
    wpc_full: str = str(mC.willpower_full_emoji * int(cursor.execute('SELECT willpowerBase from willpower').fetchone()[0]))
    wpc_sup: str = str(mC.willpower_sup_emoji * int(cursor.execute('SELECT willpowerSUP from willpower').fetchone()[0]))
    wpc_agg: str = str(mC.willpower_agg_emoji * int(cursor.execute('SELECT willpowerAGG from willpower').fetchone()[0]))

    return_embed.add_field(name='Health', value=f'{hc_full}{hc_sup}{hc_agg}', inline=False)
    return_embed.add_field(name='Willpower', value=f'{wpc_full}{wpc_sup}{wpc_agg}', inline=False)
    return_view = tV.KTV_HPWP
    return return_embed, return_view


async def hungerPageBuilder(return_embed, cursor):
    # ! Needs a Hunt Button (Lets use Selected Pool or Pred Pool)
    hunger: int = int(cursor.execute('SELECT hunger from charInfo').fetchone()[0])
    pred_type: str = str(cursor.execute('SELECT predator_type from charInfo').fetchone()[0])
    return_embed.add_field(name='Hunger', value=f'{hunger * mC.dot_full_emoji} {abs(hunger - 5) * mC.dot_empty_emoji}', inline=False)
    return_embed.add_field(name='Predator Type', value=f'{pred_type}', inline=False)
    return_view = tV.KTV_HUNGER
    return return_embed, return_view


async def attributePageBuilder(return_embed, cursor):
    # ! Needs to be affected by Impairment & Allow for Leveling
    attributes = ('Strength', 'Dexterity', 'Stamina',
                  'Charisma', 'Manipulation', 'Composure',
                  'Intelligence', 'Wits', 'Resolve')

    for_var = 0
    for x in attributes:
        if for_var / 3 in (1, 2):
            return_embed.add_field(name='', value='', inline=False)
        count = int(cursor.execute(f'SELECT {attributes[for_var].lower()} from charAttributes').fetchone()[0])
        emojis = f'{count * mC.dot_full_emoji} {abs(count - 5) * mC.dot_empty_emoji}'

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
        emojis = f'{count * mC.dot_full_emoji} {abs(count - 5) * mC.dot_empty_emoji}'

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
        emojis = f'{count * mC.dot_full_emoji} {abs(count - 5) * mC.dot_empty_emoji}'

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
        emojis = f'{count * mC.dot_full_emoji} {abs(count - 5) * mC.dot_empty_emoji}'

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
        emojis = f'{count * mC.dot_full_emoji} {abs(count - 5) * mC.dot_empty_emoji}'

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
    return_embed.add_field(name='Clan', value=f'{clan}', inline=True)

    return_embed.add_field(name='', value=f'', inline=False)

    return_embed.add_field(name='Generation', value=f'{gen * mC.dot_full_emoji}', inline=True)
    return_embed.add_field(name='Blood Potency', value=f'{bp * mC.dot_full_emoji}', inline=True)

    return_embed.add_field(name='', value=f'', inline=False)

    return_embed.add_field(name='Humanity', value=f'{humanity * mC.dot_full_emoji} {stains * mC.dot_empty_emoji}', inline=True)
    return_embed.add_field(name='Path of Enlightenment', value=f'{path_of_enlightenment}', inline=True)
    return_view = tV.KTV_EXTRA
    return return_embed, return_view

