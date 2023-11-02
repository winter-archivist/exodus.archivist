from discord.ext import commands
import discord
from discord.ui import View

from zenlog import log
import sqlite3

from misc import ashen_utils as au

# cache current user later instead, or just make it so the bot checks if someone is using the command already.
user = '.ashywinter'

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
        max_values=3,
        options=selectionOptions)
    async def decision_select_callback(self, interaction, select: discord.ui.Select):
        if str(interaction.user) != f'{user}':
            return

        db = sqlite3.connect(f'cogs//exonotes//notes//{user[2]}.sqlite')
        pass
        db.close()
        await interaction.response.edit_message()


class EXONOTES(commands.Cog):
    def __init__(self, CLIENT):
        self.CLIENT = CLIENT

    @commands.command()
    async def en(self, ctx):
        await ctx.send('EXONOTES')

    @commands.command()
    async def note(self, ctx, privateOnly=True):
        if isinstance(ctx.channel, discord.channel.DMChannel):
            # ? Intentionally doesn't delete what you've sent, this may be changed:
            # ! MESSAGE DELETION LINE: await ctx.channel.purge(limit=1
            pass
        elif privateOnly != 'f':
            await ctx.send('This command may __not__ be used in a server.\n'
                           'This is done to protect any information contained in your notes.\n'
                           '> __Please DM me instead!__')
            return

        db = sqlite3.connect(f'cogs//exonotes//notes//{user[2]}.sqlite')
        cursor = db.cursor()
        db.close()

        await ctx.send(embed=selection_embed, view=SelectionView(self.CLIENT))


async def setup(CLIENT):
    await CLIENT.add_cog(EXONOTES(CLIENT))
    log.info('> exoNotes Loaded')
