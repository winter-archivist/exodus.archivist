import discord
from discord.ui import View
from misc import ashen_utils as au


class NomadView(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    """
    Should Access & Read `ae_rewrite\cogs\shared\database\nomad.db`
    Chance for events to occur when the Nomad
        Hunts
        Enters/Exits Daysleep
        Downtime
    """

    # Buttons
    @discord.ui.button(label='Standard', emoji='<:bloodT:555804549173084160>', style=discord.ButtonStyle.gray, row=1)
    async def nomad_standard_callback(self, interaction, button):
        pass


class NomadAdminView(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    """ Should Access, Read, and Write to `ae_rewrite\cogs\shared\database\nomad.db` """

    # Buttons
    @discord.ui.button(label='Admin', emoji='<:bloodT:555804549173084160>', style=discord.ButtonStyle.gray, row=1)
    async def nomad_admin_callback(self, interaction, button):
        pass


# Embeds
nomad_embed = (
    discord.Embed(title='|The ¦ Road|', description='Scorched Rubber & Burnt Time ', color=au.embed_colors["dark_yellow"]))

nomad_admin_embed = (
    discord.Embed(title='| ¦ |', description='Tread On', color=au.embed_colors["purple"]))

nomad_denied_embed = (
    discord.Embed(title='Dead End.', description='Pavement Untouched', color=au.embed_colors["red"]))


# Info for vtmMenuHandler
roleCheck = '.Nomad'
packedViews = (NomadAdminView, NomadView)
packedEmbeds = (nomad_admin_embed, nomad_embed, nomad_denied_embed)

nomadInfo = (roleCheck, packedEmbeds, packedViews)

