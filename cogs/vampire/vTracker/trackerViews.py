import discord
from discord.ui import View


class StandardTrackerView(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Home', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=1)
    async def stepper_button_callback(self, interaction, button):
        home_embed = 1
        await func()
        view_embed = 1
        await interaction.response.edit_message(embed=home_embed, view=StandardSelectionView(self.CLIENT))



