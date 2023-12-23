import discord
import sqlite3
from zenlog import log
from discord.ui import View

import cogs.vampire.vMisc.vampirePageSystem as vPS
import cogs.vampire.vMisc.vampireUtils as vU

import cogs.vampire.vRoller.rollerPageBuilders as rPB
import cogs.vampire.vRoller.rollerOptions as rO


# ? Until Functional, the button will be gray
# ? KRV = KINDRED_ROLLER_VIEW
class KRV_DIFFICULTY(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Attributes', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=1)
    async def attribute_button_callback(self, interaction, button):
        response_embed, response_view = await vPS.pageEVNav(interaction, 'roller.attribute')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))

    @discord.ui.button(label='Physical Skills', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.gray, row=2)
    async def physical_button_callback(self, interaction, button):
        response_embed, response_view = await vPS.pageEVNav(interaction, 'roller.physical')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))

    @discord.ui.button(label='Social Skills', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.gray, row=2)
    async def social_button_callback(self, interaction, button):
        response_embed, response_view = await vPS.pageEVNav(interaction, 'roller.social')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))

    @discord.ui.button(label='Mental Skills', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.gray, row=2)
    async def mental_button_callback(self, interaction, button):
        response_embed, response_view = await vPS.pageEVNav(interaction, 'roller.mental')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))

    @discord.ui.button(label='Discipline', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.gray, row=1)
    async def discipline_button_callback(self, interaction, button):
        response_embed, response_view = await vPS.pageEVNav(interaction, 'roller.discipline')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))

    @discord.ui.button(label='Extras', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.gray, row=1)
    async def extras_button_callback(self, interaction, button):
        response_embed, response_view = await vPS.pageEVNav(interaction, 'roller.discipline')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))

    @discord.ui.select(placeholder='Select Difficulty', options=rO.difficulty_options, max_values=1, min_values=1, row=0)
    async def difficulty_select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        response_embed, response_view = await vPS.pageEVNav(interaction, 'roller.difficulty')
        character_name = await vU.getCharacterName(interaction)

        # Actual Logic of the Selection
        with sqlite3.connect(f'cogs//vampire//characters//{str(interaction.user.id)}//{character_name}//{character_name}.sqlite') as db:
            db.cursor().execute('UPDATE commandvars SET difficulty=?', (select.values))  # ! Parentheses are NOT redundant
            db.commit()
        # Actual Logic of the Selection

        response_embed = await rPB.rollerBasicPageInformation(interaction, response_embed)
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))

    @discord.ui.button(label='Roll', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.gray, row=4)
    async def roll_button_callback(self, interaction, button):
        response_embed, response_view = await vPS.pageEVNav(interaction, 'roller.difficulty')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))

