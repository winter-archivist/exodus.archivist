import discord
from discord.ui import View
from misc import ashen_utils as au

chargen_embed = (
    discord.Embed(title='Character Creation:',
                  description='Insert the values of your character sheet on r20 here! '
                              'If you mess up at any point, please contact Winter.',
                  color=au.embed_colors["purple"]))


# chargen_embed.add_field(name='Attribute:', value=f'N/A', inline=False)
# chargen_embed.set_field_at(index=0, name='Skill:', value=f'N/A', inline=False)
# chargen_embed.set_field_at(index=0, name='Discipline:', value=f'N/A', inline=False)


class CharGenView(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    """ PLAYERS SHOULD BE ABLE TO HAVE MULTIPLE CHARACTERS """

    """ TO BE DELETED/TODO START

    THE VAGUE WAY THIS SYSTEM SHOULD WORK IS IN A SET "STEP" WITH A BUTTON THAT'LL WIPE ALL PROGRESS 
    NO RESTART, JUST WIPE/CMD END
    HAVING A "GO BACK" BUTTON SOUNDS LIKE FUCKING HELL, ABSOLUTELY NOT
    THIS WILL PROBABLY NEED LOTS OF EXTRA LOGIC AND LIKE 7 FUCKING VIEWS
    FOR THE DIFFERENT INPUTS

        FUCK ME

    EACH "STEP" SHOULD WRITE FOR A SPECIFIC ATTRIBUTE/SKILL

    HOMEBREW DISCIPLINES WILL NEED TO BE MANUALLY SET BY ME
    CAN'T BE FUCKED TO ASK THE PLAYER FOR THE PROPER INPUT
    AND WON'T BE REVEALING WHAT HB DISCIPLINES ARE BEING USED

    KEYWORDS FOR THE DISCIPLINES WILL ALSO BE A FUCKING CUNT

    TO BE DELETED/TODO END"""

    # Buttons
    @discord.ui.button(label='1', emoji='<:bloodT:555804549173084160>', style=discord.ButtonStyle.red, row=1)
    async def one_button_callback(self, interaction, button):
        pass

    @discord.ui.button(label='2', emoji='<:bloodT:555804549173084160>', style=discord.ButtonStyle.gray, row=1)
    async def two_button_callback(self, interaction, button):
        pass

    @discord.ui.button(label='3', emoji='<:bloodT:555804549173084160>', style=discord.ButtonStyle.gray, row=1)
    async def three_button_callback(self, interaction, button):
        pass

    @discord.ui.button(label='4', emoji='<:bloodT:555804549173084160>', style=discord.ButtonStyle.gray, row=1)
    async def four_button_callback(self, interaction, button):
        pass

    @discord.ui.button(label='5', emoji='<:bloodT:555804549173084160>', style=discord.ButtonStyle.green, row=1)
    async def five_button_callback(self, interaction, button):
        pass
