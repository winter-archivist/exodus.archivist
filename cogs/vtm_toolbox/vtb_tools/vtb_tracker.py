import discord
import discord.ui
from zenlog import log

import misc.config.main_config as mc

import cogs.vtm_toolbox.vtb_misc.vtb_utils as vu
import cogs.vtm_toolbox.vtb_misc.vtb_pages as vp
import cogs.vtm_toolbox.vtb_tools.vtb_roller as vr
import cogs.vtm_toolbox.vtb_characters.vtb_character_manager as cm


async def return_to_home(self, interaction: discord.Interaction) -> None:
    CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
    page: discord.Embed = await vp.basic_page_builder(interaction, 'Home', '', 'dark_yellow')
    await interaction.response.send_message(embed=page, view=Home(self.CLIENT))
    return None


async def go_to_roller(self, interaction) -> None:
    CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
    page: discord.Embed = await vp.basic_page_builder(interaction, 'Home', '', 'dark_yellow')
    page: discord.Embed = await vp.standard_roller_page_modifications(page, CHARACTER)
    await interaction.response.edit_message(embed=page, view=vr.Home(self.CLIENT))
    return None


class Home(discord.ui.View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Attributes', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.gray, row=1)
    async def attributes_button_callback(self, interaction, button):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.basic_page_builder(interaction, 'Attributes Page', '', 'dark_yellow')

        attributes: tuple = \
            ('strength', 'dexterity', 'stamina', 'charisma', 'manipulation', 'composure', 'intelligence', 'wits', 'resolve')
        character_data: dict = await CHARACTER.__get_information__(attributes, 'attributes')

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
        await interaction.response.send_message(embed=page, view=Home_n_Roll(self.CLIENT))
        return

    @discord.ui.button(label='EXAMPLE', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.gray, row=1)
    async def example_button_callback(self, interaction, button):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.basic_page_builder(interaction, 'Example', '', 'dark_yellow')

        # stuff

        await interaction.response.send_message(embed=page, view=Home_n_Roll(self.CLIENT))
        return

    @discord.ui.button(label='Physical Skills', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.gray, row=0)
    async def physical_skills_button_callback(self, interaction, button):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.basic_page_builder(interaction, 'Physical Skills Page', '', 'dark_yellow')

        PHYSICAL_SKILLS: tuple = ('athletics', 'brawl', 'craft', 'drive', 'firearms', 'larceny', 'melee', 'stealth', 'survival')
        PHYSICAL_SKILLS_DICT: dict = await CHARACTER.__get_information__(PHYSICAL_SKILLS, 'skills/physical')

        # Will eventually turn this into some kind of loop

        count: int = PHYSICAL_SKILLS_DICT['athletics']
        emoji: str = f'{count * mc.DOT_FULL_EMOJI} {abs(count - 5) * mc.DOT_EMPTY_EMOJI}'
        page.add_field(name=f'{str.capitalize(PHYSICAL_SKILLS[0])}', value=f'{emoji}', inline=True)

        count: int = PHYSICAL_SKILLS_DICT['brawl']
        emoji: str = f'{count * mc.DOT_FULL_EMOJI} {abs(count - 5) * mc.DOT_EMPTY_EMOJI}'
        page.add_field(name=f'{str.capitalize(PHYSICAL_SKILLS[1])}', value=f'{emoji}', inline=True)

        count: int = PHYSICAL_SKILLS_DICT['craft']
        emoji: str = f'{count * mc.DOT_FULL_EMOJI} {abs(count - 5) * mc.DOT_EMPTY_EMOJI}'
        page.add_field(name=f'{str.capitalize(PHYSICAL_SKILLS[2])}', value=f'{emoji}', inline=True)

        #
        page.add_field(name='', value='', inline=False)

        count: int = PHYSICAL_SKILLS_DICT['drive']
        emoji: str = f'{count * mc.DOT_FULL_EMOJI} {abs(count - 5) * mc.DOT_EMPTY_EMOJI}'
        page.add_field(name=f'{str.capitalize(PHYSICAL_SKILLS[3])}', value=f'{emoji}', inline=True)

        count: int = PHYSICAL_SKILLS_DICT['firearms']
        emoji: str = f'{count * mc.DOT_FULL_EMOJI} {abs(count - 5) * mc.DOT_EMPTY_EMOJI}'
        page.add_field(name=f'{str.capitalize(PHYSICAL_SKILLS[4])}', value=f'{emoji}', inline=True)

        count: int = PHYSICAL_SKILLS_DICT['larceny']
        emoji: str = f'{count * mc.DOT_FULL_EMOJI} {abs(count - 5) * mc.DOT_EMPTY_EMOJI}'
        page.add_field(name=f'{str.capitalize(PHYSICAL_SKILLS[5])}', value=f'{emoji}', inline=True)

        #
        page.add_field(name='', value='', inline=False)

        count: int = PHYSICAL_SKILLS_DICT['melee']
        emoji: str = f'{count * mc.DOT_FULL_EMOJI} {abs(count - 5) * mc.DOT_EMPTY_EMOJI}'
        page.add_field(name=f'{str.capitalize(PHYSICAL_SKILLS[6])}', value=f'{emoji}', inline=True)

        count: int = PHYSICAL_SKILLS_DICT['stealth']
        emoji: str = f'{count * mc.DOT_FULL_EMOJI} {abs(count - 5) * mc.DOT_EMPTY_EMOJI}'
        page.add_field(name=f'{str.capitalize(PHYSICAL_SKILLS[7])}', value=f'{emoji}', inline=True)

        count: int = PHYSICAL_SKILLS_DICT['survival']
        emoji: str = f'{count * mc.DOT_FULL_EMOJI} {abs(count - 5) * mc.DOT_EMPTY_EMOJI}'
        page.add_field(name=f'{str.capitalize(PHYSICAL_SKILLS[8])}', value=f'{emoji}', inline=True)

        await interaction.response.send_message(embed=page, view=Home_n_Roll(self.CLIENT))
        return

    @discord.ui.button(label='Social Skills', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.gray, row=0)
    async def social_skills_button_callback(self, interaction, button):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.basic_page_builder(interaction, 'Social Skills Page', '', 'dark_yellow')

        SOCIAL_SKILLS: tuple = ('animal_ken', 'etiquette', 'insight', 'intimidation', 'leadership', 'performance', 'persuasion', 'streetwise', 'subterfuge')
        SOCIAL_SKILLS_DICT: dict = await CHARACTER.__get_information__(SOCIAL_SKILLS, 'skills/social')

        # Will eventually turn this into some kind of loop

        count: int = SOCIAL_SKILLS_DICT['animal_ken']
        emoji: str = f'{count * mc.DOT_FULL_EMOJI} {abs(count - 5) * mc.DOT_EMPTY_EMOJI}'
        page.add_field(name=f'{str.capitalize(SOCIAL_SKILLS[0])}', value=f'{emoji}', inline=True)

        count: int = SOCIAL_SKILLS_DICT['etiquette']
        emoji: str = f'{count * mc.DOT_FULL_EMOJI} {abs(count - 5) * mc.DOT_EMPTY_EMOJI}'
        page.add_field(name=f'{str.capitalize(SOCIAL_SKILLS[1])}', value=f'{emoji}', inline=True)

        count: int = SOCIAL_SKILLS_DICT['insight']
        emoji: str = f'{count * mc.DOT_FULL_EMOJI} {abs(count - 5) * mc.DOT_EMPTY_EMOJI}'
        page.add_field(name=f'{str.capitalize(SOCIAL_SKILLS[2])}', value=f'{emoji}', inline=True)

        #
        page.add_field(name='', value='', inline=False)

        count: int = SOCIAL_SKILLS_DICT['intimidation']
        emoji: str = f'{count * mc.DOT_FULL_EMOJI} {abs(count - 5) * mc.DOT_EMPTY_EMOJI}'
        page.add_field(name=f'{str.capitalize(SOCIAL_SKILLS[3])}', value=f'{emoji}', inline=True)

        count: int = SOCIAL_SKILLS_DICT['leadership']
        emoji: str = f'{count * mc.DOT_FULL_EMOJI} {abs(count - 5) * mc.DOT_EMPTY_EMOJI}'
        page.add_field(name=f'{str.capitalize(SOCIAL_SKILLS[4])}', value=f'{emoji}', inline=True)

        count: int = SOCIAL_SKILLS_DICT['performance']
        emoji: str = f'{count * mc.DOT_FULL_EMOJI} {abs(count - 5) * mc.DOT_EMPTY_EMOJI}'
        page.add_field(name=f'{str.capitalize(SOCIAL_SKILLS[5])}', value=f'{emoji}', inline=True)

        #
        page.add_field(name='', value='', inline=False)

        count: int = SOCIAL_SKILLS_DICT['persuasion']
        emoji: str = f'{count * mc.DOT_FULL_EMOJI} {abs(count - 5) * mc.DOT_EMPTY_EMOJI}'
        page.add_field(name=f'{str.capitalize(SOCIAL_SKILLS[6])}', value=f'{emoji}', inline=True)

        count: int = SOCIAL_SKILLS_DICT['streetwise']
        emoji: str = f'{count * mc.DOT_FULL_EMOJI} {abs(count - 5) * mc.DOT_EMPTY_EMOJI}'
        page.add_field(name=f'{str.capitalize(SOCIAL_SKILLS[7])}', value=f'{emoji}', inline=True)

        count: int = SOCIAL_SKILLS_DICT['subterfuge']
        emoji: str = f'{count * mc.DOT_FULL_EMOJI} {abs(count - 5) * mc.DOT_EMPTY_EMOJI}'
        page.add_field(name=f'{str.capitalize(SOCIAL_SKILLS[8])}', value=f'{emoji}', inline=True)

        await interaction.response.send_message(embed=page, view=Home_n_Roll(self.CLIENT))
        return

    @discord.ui.button(label='Mental Skills', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.gray, row=0)
    async def mental_skills_button_callback(self, interaction, button):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.basic_page_builder(interaction, 'Physical Skills Page', '', 'dark_yellow')

        MENTAL_SKILLS: tuple = ('academics', 'awareness', 'finance', 'investigation', 'medicine', 'occult', 'politics', 'science', 'technology')
        MENTAL_SKILLS_DICT: dict = await CHARACTER.__get_information__(MENTAL_SKILLS, 'skills/mental')

        # Will eventually turn this into some kind of loop

        count: int = MENTAL_SKILLS_DICT['academics']
        emoji: str = f'{count * mc.DOT_FULL_EMOJI} {abs(count - 5) * mc.DOT_EMPTY_EMOJI}'
        page.add_field(name=f'{str.capitalize(MENTAL_SKILLS[0])}', value=f'{emoji}', inline=True)

        count: int = MENTAL_SKILLS_DICT['awareness']
        emoji: str = f'{count * mc.DOT_FULL_EMOJI} {abs(count - 5) * mc.DOT_EMPTY_EMOJI}'
        page.add_field(name=f'{str.capitalize(MENTAL_SKILLS[1])}', value=f'{emoji}', inline=True)

        count: int = MENTAL_SKILLS_DICT['finance']
        emoji: str = f'{count * mc.DOT_FULL_EMOJI} {abs(count - 5) * mc.DOT_EMPTY_EMOJI}'
        page.add_field(name=f'{str.capitalize(MENTAL_SKILLS[2])}', value=f'{emoji}', inline=True)

        #
        page.add_field(name='', value='', inline=False)

        count: int = MENTAL_SKILLS_DICT['investigation']
        emoji: str = f'{count * mc.DOT_FULL_EMOJI} {abs(count - 5) * mc.DOT_EMPTY_EMOJI}'
        page.add_field(name=f'{str.capitalize(MENTAL_SKILLS[3])}', value=f'{emoji}', inline=True)

        count: int = MENTAL_SKILLS_DICT['medicine']
        emoji: str = f'{count * mc.DOT_FULL_EMOJI} {abs(count - 5) * mc.DOT_EMPTY_EMOJI}'
        page.add_field(name=f'{str.capitalize(MENTAL_SKILLS[4])}', value=f'{emoji}', inline=True)

        count: int = MENTAL_SKILLS_DICT['occult']
        emoji: str = f'{count * mc.DOT_FULL_EMOJI} {abs(count - 5) * mc.DOT_EMPTY_EMOJI}'
        page.add_field(name=f'{str.capitalize(MENTAL_SKILLS[5])}', value=f'{emoji}', inline=True)

        #
        page.add_field(name='', value='', inline=False)

        count: int = MENTAL_SKILLS_DICT['politics']
        emoji: str = f'{count * mc.DOT_FULL_EMOJI} {abs(count - 5) * mc.DOT_EMPTY_EMOJI}'
        page.add_field(name=f'{str.capitalize(MENTAL_SKILLS[6])}', value=f'{emoji}', inline=True)

        count: int = MENTAL_SKILLS_DICT['science']
        emoji: str = f'{count * mc.DOT_FULL_EMOJI} {abs(count - 5) * mc.DOT_EMPTY_EMOJI}'
        page.add_field(name=f'{str.capitalize(MENTAL_SKILLS[7])}', value=f'{emoji}', inline=True)

        count: int = MENTAL_SKILLS_DICT['technology']
        emoji: str = f'{count * mc.DOT_FULL_EMOJI} {abs(count - 5) * mc.DOT_EMPTY_EMOJI}'
        page.add_field(name=f'{str.capitalize(MENTAL_SKILLS[8])}', value=f'{emoji}', inline=True)

        await interaction.response.send_message(embed=page, view=Home_n_Roll(self.CLIENT))
        return


class Home_n_Roll(discord.ui.View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Home', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.gray, row=1)
    async def home_button_callback(self, interaction, button):
        await return_to_home(self, interaction)
        return

    @discord.ui.button(label='Roll', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.red, row=1)
    async def roll_button_callback(self, interaction, button):
        await go_to_roller(self, interaction)
        return
