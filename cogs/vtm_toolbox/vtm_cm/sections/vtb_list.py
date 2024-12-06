import os
import json
import discord
import discord.ext

from zenlog import log

import misc.config.main_config as mc

import cogs.vtm_toolbox.vtm_cm.vtb_character_manager as cm

import cogs.vtm_toolbox.vtm_cm.vtb_pages as vp
import cogs.vtm_toolbox.vtm_cm.sections.vtb_roller as vr
import cogs.vtm_toolbox.vtm_cm.sections.vtb_tracker as vt


class vtb_Book:
    def __init__(self, interaction: discord.Interaction, EXODUS_CLIENT):
        self.HOME_VIEW: discord.ui.View = HOME_PAGE_VIEW(EXODUS_CLIENT, self)
        self.PAGE_VIEW: discord.ui.View = PAGES_VIEW(EXODUS_CLIENT, self)

        self.BOOK_OWNER_ID: int = interaction.user.id

        self.current_pages_character_name: str = ''
        self.current_page_number: int = 0

        TARGET_PATH: str = f'cogs/vtm_toolbox/vtb_characters/{self.BOOK_OWNER_ID}/'
        self.OWNED_CHARACTERS: tuple = tuple([i for i in os.listdir(TARGET_PATH) if os.path.isdir(os.path.join(TARGET_PATH, i))])

    async def __write_pages__(self, interaction: discord.Interaction):
        home_page: discord.Embed = discord.Embed(title='Character List Home Page', description='Found Characters:', colour=mc.EMBED_COLORS['mint'])
        home_page.set_footer(text=interaction.user.id, icon_url=interaction.user.display_avatar)
        home_page.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar)
        for i in self.OWNED_CHARACTERS:
            home_page.add_field(name=f'__{i}__', value='', inline=False)

        constructed_pages: list = [home_page]

        while_var: int = 0
        while while_var < len(self.OWNED_CHARACTERS):
            FILE_PATH = f'cogs/vtm_toolbox/vtb_characters/{interaction.user.id}/{self.OWNED_CHARACTERS[while_var]}'
            with open(f'{FILE_PATH}/misc.json', 'r') as operate_file:
                CHARACTER_INFO: dict = json.load(operate_file)

            new_page: discord.Embed = discord.Embed(title='Character Page',
                                                    description=CHARACTER_INFO['Character Name'],
                                                    colour=mc.EMBED_COLORS['mint'])
            new_page.set_thumbnail(url=CHARACTER_INFO['Character Avatar URL'])
            new_page.set_footer(text=interaction.user.id, icon_url=interaction.user.display_avatar)
            new_page.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar)

            constructed_pages.append(new_page)
            while_var += 1

        self.PAGES: tuple = tuple(constructed_pages)

    async def __next_page__(self) -> discord.Embed:
        self.current_page_number += 1

        try:
            self.current_pages_character_name: str = self.PAGES[self.current_page_number].description

        except IndexError:
            self.current_page_number = 1
            self.current_pages_character_name: str = self.PAGES[self.current_page_number].description

        return self.PAGES[self.current_page_number]

    async def __home_page__(self) -> discord.Embed:
        self.current_page_number = 0
        return self.PAGES[self.current_page_number]

    async def __previous_page__(self) -> discord.Embed:
        self.current_page_number -= 1

        try:
            self.current_pages_character_name: str = self.PAGES[self.current_page_number].description

            if self.current_page_number <= 0:
                raise IndexError

        except IndexError:
            self.current_page_number: int = len(self.PAGES)-1
            self.current_pages_character_name: str = self.PAGES[self.current_page_number].description

        return self.PAGES[self.current_page_number]


class HOME_PAGE_VIEW(discord.ui.View):
    def __init__(self, CLIENT, BOOK):
        super().__init__()
        self.CLIENT = CLIENT
        self.BOOK: vtb_Book = BOOK

    # noinspection PyUnresolvedReferences
    @discord.ui.button(label='Next', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=0)
    async def next_page(self, interaction: discord.Interaction, button: discord.ui.Select):
        if interaction.user.id != self.BOOK.BOOK_OWNER_ID:
            ownership_failure_page: discord.Embed = discord.Embed(title='You Do Not Own This Book!', description='', colour=mc.EMBED_COLORS['red'])
            await interaction.response.edit_message(embed=ownership_failure_page, ephemeral=True)

        await interaction.response.edit_message(embed=await self.BOOK.__next_page__(), view=self.BOOK.PAGE_VIEW)
        return

    # noinspection PyUnresolvedReferences
    @discord.ui.button(label='Home', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=0)
    async def home_page(self, interaction: discord.Interaction, button: discord.ui.Select):
        if interaction.user.id != self.BOOK.BOOK_OWNER_ID:
            ownership_failure_page: discord.Embed = discord.Embed(title='You Do Not Own This Book!', description='', colour=mc.EMBED_COLORS['red'])
            await interaction.response.edit_message(embed=ownership_failure_page, ephemeral=True)

        await interaction.response.edit_message(embed=await self.BOOK.__home_page__(), view=self.BOOK.HOME_VIEW)
        return

    # noinspection PyUnresolvedReferences
    @discord.ui.button(label='Previous', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=0)
    async def previous_page(self, interaction: discord.Interaction, button: discord.ui.Select):
        if interaction.user.id != self.BOOK.BOOK_OWNER_ID:
            ownership_failure_page: discord.Embed = discord.Embed(title='You Do Not Own This Book!', description='', colour=mc.EMBED_COLORS['red'])
            await interaction.response.edit_message(embed=ownership_failure_page, ephemeral=True)

        await interaction.response.edit_message(embed=await self.BOOK.__previous_page__(), view=self.BOOK.PAGE_VIEW)
        return


class PAGES_VIEW(discord.ui.View):
    def __init__(self, CLIENT, BOOK):
        super().__init__()
        self.CLIENT = CLIENT
        self.BOOK: vtb_Book = BOOK

    @discord.ui.button(label='Next', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=0)
    async def next_page(self, interaction: discord.Interaction, button: discord.ui.Select):
        if interaction.user.id != self.BOOK.BOOK_OWNER_ID:
            ownership_failure_page: discord.Embed = discord.Embed(title='You Do Not Own This Book!', description='', colour=mc.EMBED_COLORS['red'])
            await interaction.response.edit_message(embed=ownership_failure_page, ephemeral=True)

        await interaction.response.edit_message(embed=await self.BOOK.__next_page__(), view=self.BOOK.PAGE_VIEW)
        return

    @discord.ui.button(label='Home', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=0)
    async def home_page(self, interaction: discord.Interaction, button: discord.ui.Select):
        if interaction.user.id != self.BOOK.BOOK_OWNER_ID:
            ownership_failure_page: discord.Embed = discord.Embed(title='You Do Not Own This Book!', description='', colour=mc.EMBED_COLORS['red'])
            await interaction.response.edit_message(embed=ownership_failure_page, ephemeral=True)

        await interaction.response.edit_message(embed=await self.BOOK.__home_page__(), view=self.BOOK.HOME_VIEW)
        return

    @discord.ui.button(label='Previous', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=0)
    async def previous_page(self, interaction: discord.Interaction, button: discord.ui.Select):
        if interaction.user.id != self.BOOK.BOOK_OWNER_ID:
            ownership_failure_page: discord.Embed = discord.Embed(title='You Do Not Own This Book!', description='', colour=mc.EMBED_COLORS['red'])
            await interaction.response.edit_message(embed=ownership_failure_page, ephemeral=True)

        await interaction.response.edit_message(embed=await self.BOOK.__previous_page__(), view=self.BOOK.PAGE_VIEW)
        return

    @discord.ui.button(label='Open In Tracker', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.red, row=1)
    async def open_in_tracker(self, interaction: discord.Interaction, button: discord.ui.Select):
        if interaction.user.id != self.BOOK.BOOK_OWNER_ID:
            ownership_failure_page: discord.Embed = discord.Embed(title='You Do Not Own This Book!', description='', colour=mc.EMBED_COLORS['red'])
            await interaction.response.edit_message(embed=ownership_failure_page, ephemeral=True)

        if self.BOOK.current_page_number == 0:
            return

        # Updates target_character.json (stored in the uid folder)
        try:
            CHARACTER_NAME_FILE: str = f'cogs/vtm_toolbox/vtb_characters/{interaction.user.id}/target_character.json'
            CHARACTER_NAME_DICT: dict = {'character_name': self.BOOK.current_pages_character_name}
            with open(CHARACTER_NAME_FILE, "w") as operate_file:
                json.dump(CHARACTER_NAME_DICT, operate_file)
        except FileNotFoundError:
            page: discord.Embed = discord.Embed(title='Target Character File Not Found.', description='', colour=mc.EMBED_COLORS['red'])
            page.set_footer(text=f'{interaction.user.id}', icon_url=f'{interaction.user.display_avatar}')
            page.set_author(name=f'{interaction.user.name}', icon_url=f'{interaction.user.display_avatar}')
            await interaction.response.edit_message(embed=page)
            return

        page: discord.Embed = await vp.basic_page_builder(cm.vtb_Character(interaction), 'Home', '', 'mint')
        await interaction.response.edit_message(embed=page, view=vt.Home(self.CLIENT))
        return

    @discord.ui.button(label=f'Open In Roller', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.red, row=1)
    async def open_in_roller(self, interaction: discord.Interaction, button: discord.ui.Select):
        if interaction.user.id != self.BOOK.BOOK_OWNER_ID:
            ownership_failure_page: discord.Embed = discord.Embed(title='You Do Not Own This Book!', description='', colour=mc.EMBED_COLORS['red'])
            await interaction.response.edit_message(embed=ownership_failure_page, ephemeral=True)

        if self.BOOK.current_page_number == 0:
            return

        # Updates target_character.json (stored in the uid folder)
        try:
            CHARACTER_NAME_FILE: str = f'cogs/vtm_toolbox/vtb_characters/{interaction.user.id}/target_character.json'
            CHARACTER_NAME_DICT: dict = {'character_name': self.BOOK.current_pages_character_name}
            with open(CHARACTER_NAME_FILE, "w") as operate_file:
                json.dump(CHARACTER_NAME_DICT, operate_file)
        except FileNotFoundError:
            page: discord.Embed = discord.Embed(title='Target Character File Not Found.', description='', colour=mc.EMBED_COLORS['red'])
            page.set_footer(text=f'{interaction.user.id}', icon_url=f'{interaction.user.display_avatar}')
            page.set_author(name=f'{interaction.user.name}', icon_url=f'{interaction.user.display_avatar}')
            await interaction.response.edit_message(embed=page)
            return

        # Resets the currently stored Roll information for given character.
        try:
            ROLL_DICT: dict = {'Difficulty'           : 0,
                               'Pool'                 : 0,
                               'Result'               : '',
                               'Composition'          : 'Base[0]',

                               # These are NOT a dict as to make it friendlier
                               # with vtb_Character.__update_information__()
                               'Regular Success Count': 0,
                               'Regular Fail Count'   : 0,
                               'Hunger Crit Count'    : 0,
                               'Hunger Success Count' : 0,
                               'Hunger Fail Count'    : 0,
                               'Skull Count'          : 0}
            ROLL_FILE_DIRECTORY: str = f'cogs/vtm_toolbox/vtb_characters/{interaction.user.id}/{self.BOOK.current_pages_character_name}/roll/info.json'
            with open(ROLL_FILE_DIRECTORY, "w") as operate_file:
                json.dump(ROLL_DICT, operate_file)
        except FileNotFoundError:
            page: discord.Embed = discord.Embed(title='Character File Not Found.', description='',
                                                colour=mc.EMBED_COLORS['red'])
            page.set_footer(text=f'{interaction.user.id}', icon_url=f'{interaction.user.display_avatar}')
            page.set_author(name=f'{interaction.user.name}', icon_url=f'{interaction.user.display_avatar}')
            await interaction.response.edit_message(embed=page)
            return
        
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.basic_page_builder(CHARACTER, 'Home', '', 'mint')
        page: discord.Embed = await vp.standard_roller_page_modifications(page, CHARACTER)
        await interaction.response.edit_message(embed=page, view=vr.Home(self.CLIENT))
        return
