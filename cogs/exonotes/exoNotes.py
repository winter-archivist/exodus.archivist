from discord.ext import commands
import discord
from discord.ui import View

from zenlog import log
import sqlite3
import os

from misc import ashen_utils as au

selection_embed = (discord.Embed(title='Select',
                                 description='',
                                 color=au.embed_colors["purple"]))

selectionOptions = [
    discord.SelectOption(
        label='Make', value='make', emoji='<:snek:785811903938953227>'
    ),
    discord.SelectOption(
        label='Read', value='read', emoji='<:snek:785811903938953227>'
    ),
    discord.SelectOption(
        label='Edit', value='edit', emoji='<:snek:785811903938953227>'
    ),
    discord.SelectOption(
        label='Delete', value='delete', emoji='<:snek:785811903938953227>'
    )]


class SelectionView(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.select(
        placeholder='Select decision',
        min_values=1,
        max_values=1,
        options=selectionOptions)
    async def decision_select_callback(self, interaction, select: discord.ui.Select):
        match select.values[0]:
            case 'make':
                await interaction.response.edit_message(view=MakeView(self.CLIENT))

            case 'read':
                await interaction.response.edit_message(view=ReadView(self.CLIENT))

            case 'edit':
                await interaction.response.edit_message(view=EditView(self.CLIENT))

            case 'delete':
                await interaction.response.edit_message(view=DeleteView(self.CLIENT))

            case _:
                log.crit('Bad Value Passed in SelectionView')
                await interaction.response.edit_message(view=None)


class MakeView(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT
    # Title
    # Subtitle
    # Tags
    # Content

    @discord.ui.button(label='Finish', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.green, row=4)
    async def finish_button_callback(self, interaction, button):

        await interaction.response.edit_message(embed=None, view=None)


class ReadView(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.select(
        placeholder='Select read',
        min_values=1,
        max_values=1,
        options=selectionOptions)
    async def read_select_callback(self, interaction, select: discord.ui.Select):
        pass


class EditView(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.select(
        placeholder='Select edit',
        min_values=1,
        max_values=1,
        options=selectionOptions)
    async def edit_select_callback(self, interaction, select: discord.ui.Select):
        pass


class DeleteView(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.select(
        placeholder='Select delete',
        min_values=1,
        max_values=1,
        options=selectionOptions)
    async def delete_select_callback(self, interaction, select: discord.ui.Select):
        pass


class EXONOTES(commands.Cog):
    def __init__(self, CLIENT):
        self.CLIENT = CLIENT

    @commands.command()
    async def en(self, ctx):
        await ctx.send('EXONOTES')

    @commands.command()
    @commands.dm_only()
    async def note(self, ctx):
        userID = ctx.author.id

        path = f'./cogs/exonotes/notes/{userID}'
        if not os.path.exists(path):
            os.mkdir(path)
            log.warn(f'> User Note Folder _ {path} _ created!')
        else:
            log.warn(f'> User Note Folder _ {path} _ already exists')
        db = sqlite3.connect(f'cogs//exonotes//notes//{userID}//{userID}.sqlite')
        cursor = db.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS charOwner(userID TEXT)')
        cursor.execute('INSERT INTO charOwner (userID) VALUES("")')
        cursor.execute('UPDATE charOwner SET userID=?', (userID,))
        db.commit()
        db.close()

        await ctx.send(embed=selection_embed, view=SelectionView(self.CLIENT))


async def setup(CLIENT):
    await CLIENT.add_cog(EXONOTES(CLIENT))
    log.info('> exoNotes Loaded')
