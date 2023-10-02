import discord
from discord.ui import View
from misc import ashen_utils as au


class CobwebView(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    """
    Should Access & Read `ae_rewrite\cogs\shared\database\cobweb.db`
    Should allow player to spend Willpower to try to extract
    Dreams/Prophecies from the Cobweb
    Has a chance to affect other places/char sheet
    """

    # Buttons
    @discord.ui.button(label='Standard', emoji='<:bloodT:555804549173084160>', style=discord.ButtonStyle.gray, row=1)
    async def cobweb_standard_callback(self, interaction, button):
        pass


class CobwebAdminView(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    """ Should Access, Read, and Write to `ae_rewrite\cogs\shared\database\cobweb.db` """

    # Buttons
    @discord.ui.button(label='Admin', emoji='<:bloodT:555804549173084160>', style=discord.ButtonStyle.blurple, row=1)
    async def cobweb_admin_callback(self, interaction, button):
        pass


# Embeds
cobweb_embed = (
    discord.Embed(title='>- The Cobweb -<', description='Of Shattered Minds.', color=au.embed_colors["white"]))

cobweb_admin_embed = (
    discord.Embed(title='>- The Spider -<', description='Of Shattered Minds.', color=au.embed_colors["purple"]))

cobweb_denied_embed = (
    discord.Embed(title='>- The Cobweb -<', description='Unaware.',color=au.embed_colors["red"]))


# Info for vtmMenuHandler
roleCheck = '.Cobweb'
packedViews = (CobwebAdminView, CobwebView)
packedEmbeds = (cobweb_admin_embed, cobweb_embed, cobweb_denied_embed)

cobwebInfo = (roleCheck, packedEmbeds, packedViews)
