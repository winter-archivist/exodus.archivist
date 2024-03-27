import discord
import discord.ui
from zenlog import log

import misc.config.main_config as mc

import cogs.vtm_toolbox.vtm_cm.vtb_pages as vp
import cogs.vtm_toolbox.vtm_cm.sections.vtb_roller as vr
import cogs.vtm_toolbox.vtm_cm.vtb_character_manager as cm

number_options = [discord.SelectOption(label='One', value='1', emoji='<:snek:785811903938953227>'),
                        discord.SelectOption(label='Two', value='2', emoji='<:snek:785811903938953227>'),
                        discord.SelectOption(label='Three', value='3', emoji='<:snek:785811903938953227>'),
                        discord.SelectOption(label='Four', value='4', emoji='<:snek:785811903938953227>'),
                        discord.SelectOption(label='Five', value='5', emoji='<:snek:785811903938953227>'),
                        discord.SelectOption(label='Six', value='6', emoji='<:snek:785811903938953227>'),
                        discord.SelectOption(label='Seven', value='7', emoji='<:snek:785811903938953227>'),
                        discord.SelectOption(label='Eight', value='8', emoji='<:snek:785811903938953227>'),
                        discord.SelectOption(label='Nine', value='9', emoji='<:snek:785811903938953227>'),
                        discord.SelectOption(label='Ten', value='10', emoji='<:snek:785811903938953227>'),
                        discord.SelectOption(label='Eleven', value='11', emoji='<:snek:785811903938953227>'),
                        discord.SelectOption(label='Twelve', value='12', emoji='<:snek:785811903938953227>'),
                        discord.SelectOption(label='Thirteen', value='13', emoji='<:snek:785811903938953227>'),
                        discord.SelectOption(label='Fourteen', value='14', emoji='<:snek:785811903938953227>'),
                        discord.SelectOption(label='Fifteen', value='15', emoji='<:snek:785811903938953227>'),
                        discord.SelectOption(label='Sixteen', value='16', emoji='<:snek:785811903938953227>'),
                        discord.SelectOption(label='Seventeen', value='17', emoji='<:snek:785811903938953227>'),]


async def return_to_home(self, interaction: discord.Interaction) -> None:
    CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)  # This is kept so the __init__ can run the owner checker
    page: discord.Embed = await vp.basic_page_builder(CHARACTER, 'Home', '', 'mint')
    await interaction.response.edit_message(embed=page, view=Home(self.CLIENT))
    return None


async def go_to_roller(self, interaction: discord.Interaction) -> None:
    CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
    page: discord.Embed = await vp.basic_page_builder(CHARACTER, 'Home', '', 'purple')
    page: discord.Embed = await vp.standard_roller_page_modifications(page, CHARACTER)
    await interaction.response.edit_message(embed=page, view=vr.Home(self.CLIENT))
    return None


class Home(discord.ui.View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Attributes', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=0)
    async def attributes_button_callback(self, interaction, button):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.basic_page_builder(CHARACTER, 'Attributes Page', '', 'mint')

        ATTRIBUTES: tuple = \
            ('Strength', 'Dexterity', 'Stamina', 'Charisma', 'Manipulation', 'Composure', 'Intelligence', 'Wits', 'Resolve')
        CHARACTER_DATA: dict = await CHARACTER.__get_values__(ATTRIBUTES, 'attributes')

        physical_impairment_flag: bool = False
        HEALTH_BASE: int = await CHARACTER.__get_value__('Base Health', 'health')
        HEALTH_SUPERFICIAL_DAMAGE: int = await CHARACTER.__get_value__('Superficial Health Damage', 'health')
        if HEALTH_BASE <= HEALTH_SUPERFICIAL_DAMAGE:
            page.add_field(name='Physically Impaired.', value='-1 to Physical Dice Pools', inline=False)
            physical_impairment_flag = True

        mental_impairment_flag: bool = False
        WILLPOWER_BASE: int = await CHARACTER.__get_value__('Base Willpower', 'willpower')
        WILLPOWER_SUPERFICIAL_DAMAGE: int = await CHARACTER.__get_value__('Superficial Willpower Damage', 'willpower')
        if WILLPOWER_BASE <= WILLPOWER_SUPERFICIAL_DAMAGE:
            page.add_field(name='Mentally Impaired', value='-1 to Social & Mental Dice Pools', inline=False)
            mental_impairment_flag = True

        for_var = 0
        for x in ATTRIBUTES:
            if for_var % 3 == 0:
                page.add_field(name='', value='', inline=False)
            count = CHARACTER_DATA[ATTRIBUTES[for_var]]

            # don't like this, but will cope
            if physical_impairment_flag is True or mental_impairment_flag is True:
                if ATTRIBUTES[for_var].lower() in ('Strength', 'Dexterity', 'Stamina'):
                    count -= 1  # Removes one from PHYSICAL attributes since the character is PHYSICALLY impaired.

                if ATTRIBUTES[for_var].lower() in ('Charisma', 'Manipulation', 'Composure', 'Intelligence', 'Wits', 'Resolve'):
                    count -= 1  # Removes one from MENTAL & SOCIAL attributes since the character is MENTALLY impaired.

            emojis = f'{count * mc.DOT_FULL_EMOJI} {abs(count - 5) * mc.DOT_EMPTY_EMOJI}'

            page.add_field(name=f'{ATTRIBUTES[for_var]}', value=f'{emojis}', inline=True)
            for_var += 1

        await interaction.response.edit_message(embed=page, view=Home_n_Roll(self.CLIENT))
        return

    @discord.ui.button(label='Disciplines', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=0)
    async def disciplines_button_callback(self, interaction, button):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.basic_page_builder(CHARACTER, 'Disciplines', '', 'mint')

        if CHARACTER.CHARACTER_NAME != 'Nyctea':
            DISCIPLINES: tuple = ('Obfuscate', 'Animalism', 'Potence', 'Dominate', 'Auspex', 'Protean', 'Presence', 'Fortitude',
                                  'Thin Blood Alchemy', 'Blood Sorcery', 'Chemeristry', 'Seven Specific', 'Myr Specific',
                                  'Selena Specific', 'Nyctea Specific One', 'Nyctea Specific Two', 'Elijah Specific')

            for_var = 0
            for x in DISCIPLINES:
                count: int = await CHARACTER.__get_value__(DISCIPLINES[for_var], 'disciplines')
                emojis = f'{count * mc.DOT_FULL_EMOJI} {abs(count - 5) * mc.DOT_EMPTY_EMOJI}'

                if count <= 0:
                    pass
                else:
                    page.add_field(name=f'{DISCIPLINES[for_var]}', value=f'{emojis}', inline=True)
                for_var += 1
        elif CHARACTER.CHARACTER_NAME == 'Nyctea':
            # Remove the code within this else and take out the if statement, if you intend on using this in your chronicle
            # these limits have been set up due to a specific character in my Chronicle
            page.add_field(name='Potential', value=f'Beyond the Eye of Saulot', inline=True)

        await interaction.response.edit_message(embed=page, view=Home_n_Roll(self.CLIENT))
        return

    @discord.ui.button(label='Hunger', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=0)
    async def hunger_button_callback(self, interaction, button):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)  # This is kept so the __init__ can run the owner checker
        page: discord.Embed = await vp.hunger_page_builder(CHARACTER)
        await interaction.response.edit_message(embed=page, view=Hunger(self.CLIENT))
        return

    @discord.ui.button(label='Physical Skills', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=1)
    async def physical_skills_button_callback(self, interaction, button):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.basic_page_builder(CHARACTER, 'Physical Skills Page', '', 'mint')

        PHYSICAL_SKILLS: tuple = ('Athletics', 'Brawl', 'Craft', 'Drive', 'Firearms', 'Larceny', 'Melee', 'Stealth', 'Survival')
        PHYSICAL_SKILLS_DICT: dict = await CHARACTER.__get_values__(PHYSICAL_SKILLS, 'skills/physical')

        while_var: int = 0
        while while_var != 9:  # 9 = Skill Count
            count: int = PHYSICAL_SKILLS_DICT[PHYSICAL_SKILLS[while_var]]
            emoji: str = f'{count * mc.DOT_FULL_EMOJI} {abs(count - 5) * mc.DOT_EMPTY_EMOJI}'
            page.add_field(name=f'{str.capitalize(PHYSICAL_SKILLS[while_var])}', value=f'{emoji}', inline=True)
            while_var += 1

        await interaction.response.edit_message(embed=page, view=Home_n_Roll(self.CLIENT))
        return

    @discord.ui.button(label='Social Skills', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=1)
    async def social_skills_button_callback(self, interaction, button):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.basic_page_builder(CHARACTER, 'Social Skills Page', '', 'mint')

        SOCIAL_SKILLS: tuple = ('Animal Ken', 'Etiquette', 'Insight', 'Intimidation', 'Leadership', 'Performance', 'Persuasion', 'Streetwise', 'Subterfuge')
        SOCIAL_SKILLS_DICT: dict = await CHARACTER.__get_values__(SOCIAL_SKILLS, 'skills/social')

        while_var: int = 0
        while while_var != 9:  # 9 = Skill Count
            count: int = SOCIAL_SKILLS_DICT[SOCIAL_SKILLS[while_var]]
            emoji: str = f'{count * mc.DOT_FULL_EMOJI} {abs(count - 5) * mc.DOT_EMPTY_EMOJI}'
            page.add_field(name=f'{str.capitalize(SOCIAL_SKILLS[while_var])}', value=f'{emoji}', inline=True)
            while_var += 1

        await interaction.response.edit_message(embed=page, view=Home_n_Roll(self.CLIENT))
        return

    @discord.ui.button(label='Mental Skills', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=1)
    async def mental_skills_button_callback(self, interaction, button):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.basic_page_builder(CHARACTER, 'Mental Skills Page', '', 'mint')

        MENTAL_SKILLS: tuple = ('Academics', 'Awareness', 'Finance', 'Investigation', 'Medicine', 'Occult', 'Politics', 'Science', 'Technology')
        MENTAL_SKILLS_DICT: dict = await CHARACTER.__get_values__(MENTAL_SKILLS, 'skills/mental')

        while_var: int = 0
        while while_var != 9:  # 9 = Skill Count
            count: int = MENTAL_SKILLS_DICT[MENTAL_SKILLS[while_var]]
            emoji: str = f'{count * mc.DOT_FULL_EMOJI} {abs(count - 5) * mc.DOT_EMPTY_EMOJI}'
            page.add_field(name=f'{str.capitalize(MENTAL_SKILLS[while_var])}', value=f'{emoji}', inline=True)
            while_var += 1

        await interaction.response.edit_message(embed=page, view=Home_n_Roll(self.CLIENT))
        return

    @discord.ui.button(label='Health & Willpower', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=2)
    async def hpwp_button_callback(self, interaction, button):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.hp_wp_page_builder(CHARACTER)
        await interaction.response.edit_message(embed=page, view=HP_n_WP(self.CLIENT))
        return

    @discord.ui.button(label='Extras', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=2)
    async def extras_button_callback(self, interaction, button):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)  # This is kept so the __init__ can run the owner checker
        page: discord.Embed = await vp.basic_page_builder(CHARACTER, 'Extras', '', 'mint')

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

        page.add_field(name='Humanity', value=f'{HUMANITY_DICT["Humanity"] * mc.DOT_FULL_EMOJI} {HUMANITY_DICT["Stains"] * mc.DOT_EMPTY_EMOJI}', inline=True)

        await interaction.response.edit_message(embed=page, view=Extras(self.CLIENT))
        return


class Home_n_Roll(discord.ui.View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Home', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=1)
    async def home_button_callback(self, interaction, button):
        await return_to_home(self, interaction)
        return

    @discord.ui.button(label='Roll', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.red, row=1)
    async def roll_button_callback(self, interaction, button):
        await go_to_roller(self, interaction)
        return


class HP_n_WP(discord.ui.View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Home', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=1)
    async def home_button_callback(self, interaction, button):
        await return_to_home(self, interaction)
        return

    @discord.ui.button(label='Roll', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.red, row=1)
    async def roll_button_callback(self, interaction, button):
        await go_to_roller(self, interaction)
        return

    @discord.ui.button(label='Mend', emoji=f'{mc.HUNGER_EMOJI}', style=discord.ButtonStyle.red, row=2)
    async def mend_button_callback(self, interaction, button):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)

        BLOOD_POTENCY: int = await CHARACTER.__get_value__('Blood Potency', 'misc')
        if BLOOD_POTENCY <= 1: MEND_AMOUNT = 1
        elif BLOOD_POTENCY <= 3: MEND_AMOUNT = 2
        elif BLOOD_POTENCY <= 7: MEND_AMOUNT = 3
        elif BLOOD_POTENCY <= 9: MEND_AMOUNT = 4
        elif BLOOD_POTENCY == 10: MEND_AMOUNT = 5
        else: raise ValueError

        SUPERFICIAL_HEALTH_DAMAGE: int = await CHARACTER.__get_value__('Superficial Health Damage', 'health')

        # Prevents a Rouse from occurring if no health can be gained.
        if SUPERFICIAL_HEALTH_DAMAGE == 0:
            page: discord.Embed = await vp.hp_wp_page_builder(interaction)
            page.add_field(name='No Superficial Health to Regain', value='')
            await interaction.response.edit_message(embed=page, view=HP_n_WP(self.CLIENT))
            return

        ROUSE_RESULT: tuple = await CHARACTER.__rouse_check__()
        if ROUSE_RESULT[0] == 'Frenzy' == 'Frenzy':  # .__rouse_check__ handles Frenzy
            return

        # Can't heal damage you don't have
        if MEND_AMOUNT > SUPERFICIAL_HEALTH_DAMAGE:
            MEND_AMOUNT = SUPERFICIAL_HEALTH_DAMAGE

        await CHARACTER.__update_value__('Superficial Health Damage', int(SUPERFICIAL_HEALTH_DAMAGE - MEND_AMOUNT), 'health')

        page: discord.Embed = await vp.hp_wp_page_builder(interaction)

        page.add_field(name=f'Rouse {ROUSE_RESULT[0]}', value=f'`{MEND_AMOUNT}` Health Regained. New Hunger: {ROUSE_RESULT[1] * mc.HUNGER_EMOJI}')
        await interaction.response.edit_message(embed=page, view=HP_n_WP(self.CLIENT))
        return

    @discord.ui.button(label='Take HP/WP Damage', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.red, row=2)
    async def to_damage_button_callback(self, interaction, button):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.hp_wp_page_builder(CHARACTER)
        await interaction.response.edit_message(embed=page, view=HP_n_WP_Damage(self.CLIENT))
        return None


class HP_n_WP_Damage(discord.ui.View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Return', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=4)
    async def return_to_hpwp_button_callback(self, interaction, button):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.hp_wp_page_builder(CHARACTER)
        await interaction.response.edit_message(embed=page, view=HP_n_WP(self.CLIENT))
        return

    @discord.ui.select(placeholder='Take Superficial HP Damage', options=number_options, max_values=1, min_values=1, row=0)
    async def hp_sup_dmg_select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)

        damage_amount: int = int(select.values[0])

        BASE_HEALTH: int = await CHARACTER.__get_value__('Base Health', 'health')

        while damage_amount > 0:
            HEALTH_DAMAGE: dict = await CHARACTER.__get_values__(('Superficial Health Damage', 'Aggravated Health Damage'), 'health')
            AGG_DMG = HEALTH_DAMAGE['Aggravated Health Damage']
            SUP_DMG = HEALTH_DAMAGE['Superficial Health Damage']

            if BASE_HEALTH == AGG_DMG:
                # Set up torpor logic later
                # ENTER TORPOR HERE
                log.crit('Someone Torpor\'d')
            elif BASE_HEALTH == SUP_DMG:  # Deals AGG Damage
                await CHARACTER.__update_value__('Aggravated Health Damage', int(AGG_DMG + 1), 'health')
            else:  # Deals SUP Damage
                await CHARACTER.__update_value__('Superficial Health Damage', int(SUP_DMG + 1), 'health')
            damage_amount -= 1

        page: discord.Embed = await vp.hp_wp_page_builder(CHARACTER)
        await interaction.response.edit_message(embed=page, view=HP_n_WP_Damage(self.CLIENT))
        return

    @discord.ui.select(placeholder='Take Aggravated HP Damage', options=number_options, max_values=1, min_values=1, row=1)
    async def hp_agg_dmg_select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)

        damage_amount: int = int(select.values[0])

        BASE_HEALTH: int = await CHARACTER.__get_value__('Base Health', 'health')

        while damage_amount > 0:
            AGG_DMG: int = await CHARACTER.__get_value__('Aggravated Health Damage', 'health')

            if BASE_HEALTH == AGG_DMG:
                # Set up torpor logic later
                # ENTER TORPOR HERE
                log.crit('Someone Torpor\'d')
                return

            await CHARACTER.__update_value__('Aggravated Health Damage', int(AGG_DMG + 1), 'health')
            damage_amount -= 1

        page: discord.Embed = await vp.hp_wp_page_builder(CHARACTER)
        await interaction.response.edit_message(embed=page, view=HP_n_WP_Damage(self.CLIENT))
        return

    @discord.ui.select(placeholder='Take Superficial WP Damage', options=number_options, max_values=1, min_values=1, row=2)
    async def wp_sup_dmg_select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)

        damage_amount: int = int(select.values[0])

        BASE_WILLPOWER: int = await CHARACTER.__get_value__('Base Willpower', 'willpower')

        while damage_amount > 0:
            WILLPOWER_DAMAGE: dict = await CHARACTER.__get_values__(('Superficial Willpower Damage', 'Aggravated Willpower Damage'), 'willpower')
            AGG_DMG = WILLPOWER_DAMAGE['Aggravated Willpower Damage']
            SUP_DMG = WILLPOWER_DAMAGE['Superficial Willpower Damage']

            if BASE_WILLPOWER == SUP_DMG:  # Deals AGG Damage
                await CHARACTER.__update_value__('Aggravated Willpower Damage', int(AGG_DMG + 1), 'willpower')
            else:  # Deals SUP Damage
                await CHARACTER.__update_value__('Superficial Willpower Damage', int(SUP_DMG + 1), 'willpower')
            damage_amount -= 1

        page: discord.Embed = await vp.hp_wp_page_builder(CHARACTER)
        await interaction.response.edit_message(embed=page, view=HP_n_WP_Damage(self.CLIENT))
        return

    @discord.ui.select(placeholder='Take Aggravated WP Damage', options=number_options, max_values=1, min_values=1, row=3)
    async def wp_agg_dmg_select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)

        damage_amount: int = int(select.values[0])

        BASE_WILLPOWER: int = await CHARACTER.__get_value__('Base Willpower', 'willpower')

        while damage_amount > 0:
            AGG_DMG: int = await CHARACTER.__get_value__('Aggravated Willpower Damage', 'willpower')
            await CHARACTER.__update_value__('Aggravated Willpower Damage', int(AGG_DMG + 1), 'willpower')
            damage_amount -= 1

        page: discord.Embed = await vp.hp_wp_page_builder(CHARACTER)
        await interaction.response.edit_message(embed=page, view=HP_n_WP_Damage(self.CLIENT))
        return


class Hunger(discord.ui.View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Home', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=1)
    async def home_button_callback(self, interaction, button):
        await return_to_home(self, interaction)
        return

    @discord.ui.button(label='Predator Type', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.red, row=2)
    async def predator_type_button_callback(self, interaction, button):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.basic_page_builder(CHARACTER, 'Predator Type Information', '', 'mint')

        PREDATOR_TYPE: str = await CHARACTER.__get_value__('Predator Type', 'misc')
        SUPPORTED_PREDATOR_TYPES: tuple = ('SECRET_PREDATOR_TYPE', 'Grim Reaper', 'Sandman',
                                           'Cryptid', 'Alleycat', 'Grave Robber', 'Trapdoor')

        if PREDATOR_TYPE not in SUPPORTED_PREDATOR_TYPES:
            log.error('**> Bad PREDATOR_TYPE given to predator_type_button_callback()')
            return

        match PREDATOR_TYPE:
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
                log.crit('**> How did we get here? (vtb_pages "case _:")')
                return

        page.add_field(name='Predator Type', value=f'{PREDATOR_TYPE}', inline=True)
        page.add_field(name='PT Pool', value=f'{pt_pool}', inline=False)
        page.add_field(name='PT Description', value=f'{pt_desc}', inline=False)
        page.add_field(name='PT Discipline(s)', value=f'{pt_disciplines}', inline=True)
        page.add_field(name='PT Specialty(ies)', value=f'{pt_spec}', inline=True)
        page.add_field(name='PT Merit(s)', value=f'{pt_merit}', inline=True)
        page.add_field(name='PT Flaw(s)', value=f'{pt_flaws}', inline=True)

        await interaction.response.edit_message(embed=page, view=Predator_Type(self.CLIENT))
        return None


class Predator_Type(discord.ui.View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Return', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=1)
    async def return_to_hunger_button_callback(self, interaction, button):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.hunger_page_builder(CHARACTER)
        await interaction.response.edit_message(embed=page, view=Hunger(self.CLIENT))
        return

    @discord.ui.button(label='Roll', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.red, row=1)
    async def roll_button_callback(self, interaction, button):
        await go_to_roller(self, interaction)
        return


class Extras(discord.ui.View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Home', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=0)
    async def home_button_callback(self, interaction, button):
        await return_to_home(self, interaction)
        return

    @discord.ui.button(label='Roll', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.red, row=0)
    async def roll_button_callback(self, interaction, button):
        await go_to_roller(self, interaction)
        return

    @discord.ui.button(label='Clan Information', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.red, row=1)
    async def clan_button_callback(self, interaction, button):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)

        MISC_DICT: dict = await CHARACTER.__get_values__(('Clan', 'Bloodline'), 'misc')
        CLAN = MISC_DICT['Clan']
        BLOODLINE = MISC_DICT['Bloodline']

        if CLAN not in ('SECRET_CLAN', 'Tzimisce', 'Tremere', 'Thinblood'):
            fail_page: discord.Embed = await vp.basic_page_builder(CHARACTER, 'Clan Information', 'Failed to Retrieve', 'red')
            log.error(f'*> Bad CLAN ({CLAN}) given to clan_button_callback() | {CHARACTER.OWNER_NAME} | {CHARACTER.OWNER_ID} |')
            await interaction.response.edit_message(embed=fail_page, view=Home_n_Roll(self.CLIENT))
            return

        page: discord.Embed = await vp.basic_page_builder(CHARACTER, 'Clan Information', '', 'mint')
        # This is specific to my chronicle, for your use, remove this
        if CHARACTER.CHARACTER_NAME == 'Nyctea':
            CLAN_BANE_TITLE: str = ''
            CLAN_BANE_DESCRIPTION: str = 'Beyond'
            CLAN_COMPULSION_TITLE: str = ''
            CLAN_COMPULSION_DESCRIPTION: str = 'The Sight'
            CLAN_DISCIPLINES: str = 'Of Saulot'
            # This is specific to my chronicle, for your use, remove this

        # All the information below should be looked at and edited per your chronicle since mine uses homebrew.
        variant_bane: bool = False
        if CLAN == 'Tzimisce':
            if BLOODLINE == 'New Clan':
                CLAN_BANE_TITLE: str = 'Grounded'
                CLAN_BANE_DESCRIPTION: str = ('Each Tzimisce must choose a specific charge — a physical domain, a group of people'
                                              ', an organization, or even something more esoteric — but clearly defined and limit'
                                              'ed. The Kindred must spend their day sleep surrounded by their chosen charge. Hist'
                                              'orically this has often meant slumbering in the soil of their land, but it can als'
                                              'o mean being surrounded by that which they tonight rule: a certain kind of people,'
                                              ' a building deeply tied to their obsession, a local counterculture faction, or oth'
                                              'er, more outlandish elements. If they do not, they sustain aggravated Willpower da'
                                              'mage equal to their Bane Severity upon waking the following night.')

                CLAN_COMPULSION_TITLE: str = 'Refinement'
                CLAN_COMPULSION_DESCRIPTION: str = ('The Tzimisce’s blood pushes them to improve or transform things, from their o'
                                                    'wn flesh to their domains and hospitality. Everything can be honed or improv'
                                                    'ed upon. The Tzimisce must score a critical at a roll in order to improve so'
                                                    'mething, either giving a bonus to an item or action, or improving a dice poo'
                                                    'l on themselves, someone or something else. Until they successfully improve '
                                                    'something, they take a -2 penalty to all actions unrelated to making somethi'
                                                    'ng better than its current state.')

                CLAN_DISCIPLINES: str = 'Vicissitude, Animalism, Auspex'
        elif CLAN == 'Tremere':
            CLAN_BANE_TITLE: str = 'Deficient Blood'
            CLAN_BANE_DESCRIPTION: str = ('The Tremere are no longer able to create Blood Bonds with other Kindr'
                                          'ed through normal means. A Tremere can still bind mortals and ghouls, though the corru'
                                          'pted vitae must be drunk an additional number of times equal to the vampire’s Bane Sev'
                                          'erity for the bond to form. ')

            variant_bane: bool = True
            VARIANT_CLAN_BANE_TITLE: str = 'Stolen Blood'
            VARIANT_CLAN_BANE_DESCRIPTION: str = ('When performing a Blood Surge they need to make Rouse Checks equal to their Ba'
                                                  'ne Severity. If these Rouse Checks increase their Hunger to 5 or higher, they '
                                                  'can choose whether to back off their Blood Surge or perform it to then hit Hun'
                                                  'ger 5 afterward immediately')

            CLAN_COMPULSION_TITLE: str = 'Refinement'
            CLAN_COMPULSION_DESCRIPTION: str = ('nothing but the best satisfies the vampire. Anything less than exceptional perfo'
                                                'rmance instils a profound sense of failure, and they often repeat tasks obsessiv'
                                                'ely to get them "just right". Until the vampire scores a critical win on a Skill'
                                                ' roll or the scene ends, the vampire labours under a two-dice penalty to all dic'
                                                'e pools. The penalty is reduced to one die for a repeated action and removed ent'
                                                'irely on a second repeat.')

            CLAN_DISCIPLINES: str = 'Blood Sorcery, Dominate, Auspex'
        elif CLAN == 'Thinblood':
            CLAN_BANE_TITLE: str = 'Thinblooded'
            CLAN_BANE_DESCRIPTION: str = ('Your blood is too thin, too far from Caine; Your blood potency can not be raised above'
                                          ' 0. Additionally, you begin with the Suspect flaw.')

            CLAN_COMPULSION_TITLE: str = 'N/A'
            CLAN_COMPULSION_DESCRIPTION: str = ''

            CLAN_DISCIPLINES: str = 'N/A'

        page.add_field(name=f'Clan Bane: {CLAN_BANE_TITLE}', value=f'{CLAN_BANE_DESCRIPTION}', inline=False)
        if variant_bane:
            page.add_field(name=f'Clan Bane: {VARIANT_CLAN_BANE_TITLE}', value=f'{VARIANT_CLAN_BANE_DESCRIPTION}', inline=False)
        page.add_field(name=f'Clan Compulsion: {CLAN_COMPULSION_TITLE}', value=f'{CLAN_COMPULSION_DESCRIPTION}', inline=False)
        page.add_field(name=f'Clan Disciplines', value=f'{CLAN_DISCIPLINES}', inline=False)

        await interaction.response.edit_message(embed=page, view=Extras(self.CLIENT))
        return

    @discord.ui.button(label='Remorse', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.gray, row=1)
    async def remorse_button_callback(self, interaction, button):
        raise NotImplementedError
        return
