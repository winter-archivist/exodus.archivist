import discord
from discord.ui import View
from misc import ashen_utils as au

homebrew_embed = (
    discord.Embed(title='Homebrew', description='Homebrew', color=au.embed_colors["white"]))


class HomebrewView(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    # Buttons
    @discord.ui.button(label='Homebrew', emoji='<:bloodT:555804549173084160>', style=discord.ButtonStyle.gray, row=1)
    async def nomad_standard_callback(self, interaction, button):
        pass
