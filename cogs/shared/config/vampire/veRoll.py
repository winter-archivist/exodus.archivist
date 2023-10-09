import discord
from discord.ui import View

from misc import ashen_utils as au
from cogManager import non_admin_embed as cm

roll_embed = (
    discord.Embed(title='Roll', description='ROLL FUCKO', color=au.embed_colors["cyan"]))


class RollView(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    # Buttons
    @discord.ui.select(
        placeholder='Select physicalAttribute',
        options=[
            discord.SelectOption(
                label='Strength', value='str',
                emoji='<:color_01_blood_red:1136744533812596906>',
            ),
            discord.SelectOption(
                label='Dexterity', value='dex',
                emoji='<:color_04_orange:1136744764201512981> ',
            ),
            discord.SelectOption(
                label='Stamina', value='sta',
                emoji='<:color_08_dark_green:1136753193691381760>',
            )],
        row=0)
    async def physicalAttribute_select_callback(self, interaction, select: discord.ui.Select):
        if str(interaction.user) != '.ashywinter':
            await interaction.response.send_message(embed=cm.non_admin_embed, ephemeral=True)
            return

        # Read the value in database

        # Cache it

        await interaction.response.edit_message(embed=roll_embed)

    @discord.ui.button(label='Run', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.green)
    async def run_button_callback(self, interaction, button):
        if str(interaction.user) != '.ashywinter':
            await interaction.response.send_message(embed=cm.non_admin_embed, ephemeral=True)
            return

        # Read the value in database

        # Roll it

        roll_embed.set_field_at(index=2, name='Result:', value=f'RESULT#', inline=False)
