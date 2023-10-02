import discord
from discord.ui import View
from misc import ashen_utils as au


class RatView(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    """
    Should Access & Read `ae_rewrite\cogs\shared\database\rat.db`
    Should allow player to spend Willpower to try to gain
    Knowledge/Secrets from the DarkNet or fellow Rats
    Has a chance to affect other places/char sheet
    """

    # Buttons
    @discord.ui.button(label='Standard', emoji='<:bloodT:555804549173084160>', style=discord.ButtonStyle.gray, row=1)
    async def rat_standard_callback(self, interaction, button):
        pass


class RatAdminView(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    """ Should Access, Read, and Write to `ae_rewrite\cogs\shared\database\rat.db` """

    # Buttons
    @discord.ui.button(label='Admin', emoji='<:bloodT:555804549173084160>', style=discord.ButtonStyle.gray, row=1)
    async def rat_admin_callback(self, interaction, button):
        pass


# Embeds
rat_embed = discord.Embed(title='[The Rat Tunnels]', description='Hidden within Secrets', color=au.embed_colors["black"])
rat_admin_embed = discord.Embed(title='[[SysAd]]', description='The Unseen Eye', color=au.embed_colors["purple"])
rat_denied_embed = discord.Embed(title=']]Underfoot[[ ', description='Secrets Untouched', color=au.embed_colors["red"])


# Info for vtmMenuHandler
roleCheck = '.Rat'
packedViews = (RatAdminView, RatView)
packedEmbeds = (rat_admin_embed, rat_embed, rat_denied_embed)

ratInfo = (roleCheck, packedEmbeds, packedViews)
