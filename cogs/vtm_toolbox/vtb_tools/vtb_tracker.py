import discord
import discord.ui
from zenlog import log

import misc.config.main_config as mc

import cogs.vtm_toolbox.vtb_misc.vtb_utils as vu
import cogs.vtm_toolbox.vtb_misc.vtb_pages as vp
import cogs.vtm_toolbox.vtb_tools.vtb_roller as vr
import cogs.vtm_toolbox.vtb_characters.vtb_character_manager as cm

health_or_willpower_options = [discord.SelectOption(label='One', value='1', emoji='<:snek:785811903938953227>'),
                               discord.SelectOption(label='Two', value='2', emoji='<:snek:785811903938953227>'),
                               discord.SelectOption(label='Three', value='3', emoji='<:snek:785811903938953227>'),
                               discord.SelectOption(label='Four', value='4', emoji='<:snek:785811903938953227>'),
                               discord.SelectOption(label='Five', value='5', emoji='<:snek:785811903938953227>'),
                               discord.SelectOption(label='Six', value='6', emoji='<:snek:785811903938953227>'),
                               discord.SelectOption(label='Seven', value='7', emoji='<:snek:785811903938953227>'),
                               discord.SelectOption(label='Eight', value='8', emoji='<:snek:785811903938953227>')]


async def return_to_home(self, interaction: discord.Interaction) -> None:
    CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)  # This is kept so the __init__ can run the owner checker
    page: discord.Embed = await vp.basic_page_builder(interaction, 'Home', '', 'mint')
    await interaction.response.edit_message(embed=page, view=Home(self.CLIENT))
    return None


async def go_to_roller(self, interaction: discord.Interaction) -> None:
    CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
    page: discord.Embed = await vp.basic_page_builder(interaction, 'Home', '', 'purple')
    page: discord.Embed = await vp.standard_roller_page_modifications(page, CHARACTER)
    await interaction.response.edit_message(embed=page, view=vr.Home(self.CLIENT))
    return None


class Home(discord.ui.View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Attributes', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=1)
    async def attributes_button_callback(self, interaction, button):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.basic_page_builder(interaction, 'Attributes Page', '', 'mint')

        attributes: tuple = \
            ('strength', 'dexterity', 'stamina', 'charisma', 'manipulation', 'composure', 'intelligence', 'wits', 'resolve')
        character_data: dict = await CHARACTER.__get_values__(attributes, 'attributes')

        emoji_result = f'{character_data["strength"] * mc.DOT_FULL_EMOJI} {abs(character_data["strength"] - 5) * mc.DOT_EMPTY_EMOJI}'
        page.add_field(name='Strength', value=emoji_result, inline=True)

        emoji_result = f'{character_data["dexterity"] * mc.DOT_FULL_EMOJI} {abs(character_data["dexterity"] - 5) * mc.DOT_EMPTY_EMOJI}'
        page.add_field(name='Dexterity', value=emoji_result, inline=True)

        emoji_result = f'{character_data["stamina"] * mc.DOT_FULL_EMOJI} {abs(character_data["stamina"] - 5) * mc.DOT_EMPTY_EMOJI}'
        page.add_field(name='Stamina', value=emoji_result, inline=True)

        page.add_field(name='', value='', inline=False)

        emoji_result = f'{character_data["charisma"] * mc.DOT_FULL_EMOJI} {abs(character_data["charisma"] - 5) * mc.DOT_EMPTY_EMOJI}'
        page.add_field(name='Charisma', value=emoji_result, inline=True)

        emoji_result = f'{character_data["manipulation"] * mc.DOT_FULL_EMOJI} {abs(character_data["manipulation"] - 5) * mc.DOT_EMPTY_EMOJI}'
        page.add_field(name='Manipulation', value=emoji_result, inline=True)

        emoji_result = f'{character_data["composure"] * mc.DOT_FULL_EMOJI} {abs(character_data["composure"] - 5) * mc.DOT_EMPTY_EMOJI}'
        page.add_field(name='Composure', value=emoji_result, inline=True)

        page.add_field(name='', value='', inline=False)

        emoji_result = f'{character_data["intelligence"] * mc.DOT_FULL_EMOJI} {abs(character_data["intelligence"] - 5) * mc.DOT_EMPTY_EMOJI}'
        page.add_field(name='Intelligence', value=emoji_result, inline=True)

        emoji_result = f'{character_data["wits"] * mc.DOT_FULL_EMOJI} {abs(character_data["wits"] - 5) * mc.DOT_EMPTY_EMOJI}'
        page.add_field(name='Wits', value=emoji_result, inline=True)

        emoji_result = f'{character_data["resolve"] * mc.DOT_FULL_EMOJI} {abs(character_data["resolve"] - 5) * mc.DOT_EMPTY_EMOJI}'
        page.add_field(name='Resolve', value=emoji_result, inline=True)
        await interaction.response.edit_message(embed=page, view=Home_n_Roll(self.CLIENT))
        return

    @discord.ui.button(label='Health & Willpower', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=1)
    async def hpwp_button_callback(self, interaction, button):
        page: discord.Embed = await vp.hp_wp_page_builder(interaction)
        await interaction.response.edit_message(embed=page, view=HP_n_WP(self.CLIENT))
        return

    @discord.ui.button(label='Physical Skills', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=0)
    async def physical_skills_button_callback(self, interaction, button):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.basic_page_builder(interaction, 'Physical Skills Page', '', 'mint')

        PHYSICAL_SKILLS: tuple = ('athletics', 'brawl', 'craft', 'drive', 'firearms', 'larceny', 'melee', 'stealth', 'survival')
        PHYSICAL_SKILLS_DICT: dict = await CHARACTER.__get_values__(PHYSICAL_SKILLS, 'skills/physical')

        while_var: int = 0
        while while_var != 9:  # 9 = Skill Count
            count: int = PHYSICAL_SKILLS_DICT[PHYSICAL_SKILLS[while_var]]
            emoji: str = f'{count * mc.DOT_FULL_EMOJI} {abs(count - 5) * mc.DOT_EMPTY_EMOJI}'
            page.add_field(name=f'{str.capitalize(PHYSICAL_SKILLS[while_var])}', value=f'{emoji}', inline=True)
            while_var += 1

        await interaction.response.edit_message(embed=page, view=Home_n_Roll(self.CLIENT))
        return

    @discord.ui.button(label='Social Skills', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=0)
    async def social_skills_button_callback(self, interaction, button):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.basic_page_builder(interaction, 'Social Skills Page', '', 'mint')

        SOCIAL_SKILLS: tuple = ('animal_ken', 'etiquette', 'insight', 'intimidation', 'leadership', 'performance', 'persuasion', 'streetwise', 'subterfuge')
        SOCIAL_SKILLS_DICT: dict = await CHARACTER.__get_values__(SOCIAL_SKILLS, 'skills/social')

        while_var: int = 0
        while while_var != 9:  # 9 = Skill Count
            count: int = SOCIAL_SKILLS_DICT[SOCIAL_SKILLS[while_var]]
            emoji: str = f'{count * mc.DOT_FULL_EMOJI} {abs(count - 5) * mc.DOT_EMPTY_EMOJI}'

            # This is a special case, because just str.capitalize() will result in the string being 'Animal_ken'
            # I'll sacrifice a little bit of performance, Python isn't supposed to be fast anyway
            if SOCIAL_SKILLS[while_var] == 'animal_ken':
                page.add_field(name=f'Animal Ken', value=f'{emoji}', inline=True)
            else:
                page.add_field(name=f'{str.capitalize(SOCIAL_SKILLS[while_var])}', value=f'{emoji}', inline=True)
            while_var += 1

        await interaction.response.edit_message(embed=page, view=Home_n_Roll(self.CLIENT))
        return

    @discord.ui.button(label='Mental Skills', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=0)
    async def mental_skills_button_callback(self, interaction, button):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.basic_page_builder(interaction, 'Mental Skills Page', '', 'mint')

        MENTAL_SKILLS: tuple = ('academics', 'awareness', 'finance', 'investigation', 'medicine', 'occult', 'politics', 'science', 'technology')
        MENTAL_SKILLS_DICT: dict = await CHARACTER.__get_values__(MENTAL_SKILLS, 'skills/mental')

        while_var: int = 0
        while while_var != 9:  # 9 = Skill Count
            count: int = MENTAL_SKILLS_DICT[MENTAL_SKILLS[while_var]]
            emoji: str = f'{count * mc.DOT_FULL_EMOJI} {abs(count - 5) * mc.DOT_EMPTY_EMOJI}'
            page.add_field(name=f'{str.capitalize(MENTAL_SKILLS[while_var])}', value=f'{emoji}', inline=True)
            while_var += 1

        await interaction.response.edit_message(embed=page, view=Home_n_Roll(self.CLIENT))
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
        page: discord.Embed = await vp.basic_page_builder(interaction, 'Home', '', 'purple')
        SUPERFICIAL_HEALTH_DAMAGE: int = await CHARACTER.__get_value__('superficial_health_damage', 'health')
        BLOOD_POTENCY: int = await CHARACTER.__get_value__('blood_potency', 'misc')

        # Prevents a Rouse from occurring if no health can be gained.
        if SUPERFICIAL_HEALTH_DAMAGE == 0:
            page.add_field(name='No Superficial Health to Regain', value='')
            await interaction.response.edit_message(embed=page, view=HP_n_WP(self.CLIENT))
            return

        ROUSE_RESULT: tuple = await CHARACTER.__rouse_check__()
        if ROUSE_RESULT[0] == 'Frenzy' == 'Frenzy':  # .__rouse_check__ handles Frenzy
            return
        NEW_HUNGER: int = ROUSE_RESULT[1]

        if BLOOD_POTENCY <= 1: mend_amount = 1
        elif BLOOD_POTENCY <= 3: mend_amount = 2
        elif BLOOD_POTENCY <= 7: mend_amount = 3
        elif BLOOD_POTENCY <= 9: mend_amount = 4
        elif BLOOD_POTENCY == 10: mend_amount = 5
        else: return

        # Can't heal damage you don't have
        if mend_amount > SUPERFICIAL_HEALTH_DAMAGE:
            mend_amount = SUPERFICIAL_HEALTH_DAMAGE

        page.add_field(name=f'Rouse {ROUSE_RESULT[0]}', value=f'`{mend_amount}` Health Regained. Current Hunger: `{ROUSE_RESULT[0]}`')

        await interaction.response.edit_message(embed=page, view=HP_n_WP(self.CLIENT))
        return

    @discord.ui.button(label='Take HP/WP Damage', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.red, row=2)
    async def to_damage_button_callback(self, interaction, button):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)  # This is kept so the __init__ can run the owner checker
        page: discord.Embed = await vp.basic_page_builder(interaction, 'Take HP/WP Damage', '', 'mint')
        await interaction.response.edit_message(embed=page, view=HP_n_WP_Damage(self.CLIENT))
        return None


class HP_n_WP_Damage(discord.ui.View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Return', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=1)
    async def return_to_hpwp_button_callback(self, interaction, button):
        page: discord.Embed = await vp.hp_wp_page_builder(interaction)
        await interaction.response.edit_message(embed=page, view=HP_n_WP(self.CLIENT))
        return
