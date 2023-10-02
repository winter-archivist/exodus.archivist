import discord
from discord.ui import View
from misc import ashen_utils as au


class MarkView(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    """
    Should Access & Read `ae_rewrite\cogs\shared\database\mark.db`
    Should allow player to spend Willpower/HP to try to extract
    Prophecies/Knowledge/Power from the Mark of Caine
    Has a chance to affect other places/char sheet
    """

    # Buttons
    @discord.ui.button(label='Standard', emoji='<:bloodT:555804549173084160>', style=discord.ButtonStyle.gray, row=1)
    async def mark_standard_callback(self, interaction, button):
        pass


class MarkAdminView(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    """ Should Access, Read, and Write to `ae_rewrite\cogs\shared\database\mark.db` """

    # Buttons
    @discord.ui.button(label='Admin', emoji='<:bloodT:555804549173084160>', style=discord.ButtonStyle.gray, row=1)
    async def mark_admin_callback(self, interaction, button):
        pass


# Embeds
mark_embed = (
    discord.Embed(title='>-| The Mark |-<', description='A Curse.', color=au.embed_colors["red"]))

mark_admin_embed = (
    discord.Embed(title='>- Caine -<', description='Lazarus', color=au.embed_colors["purple"]))

mark_denied_embed = (
    discord.Embed(title='>-| The Mark |-<', description='Unblessed.', color=au.embed_colors["blue"]))


# Info for vtmMenuHandler
roleCheck = '.Marked'
packedViews = (MarkAdminView, MarkView)
packedEmbeds = (mark_admin_embed, mark_embed, mark_denied_embed)

markInfo = (roleCheck, packedEmbeds, packedViews)

