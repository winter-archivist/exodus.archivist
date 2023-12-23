import discord
from discord.ui import View
import cogs.vampire.vMisc.vampirePageSystem as vPS


# ? Until Functional, the button will be gray
# ? KTV = KINDRED_TRACKER_VIEW
class KTV_HOME(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='HP/WP Page', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.green, row=1)
    async def hpwp_page_button_callback(self, interaction, button):
        response_embed, response_view = await vPS.pageEVNav(interaction, 'tracker.hp/wp')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))

    @discord.ui.button(label='Hunger Page', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.green, row=1)
    async def hunger_page_button_callback(self, interaction, button):
        response_embed, response_view = await vPS.pageEVNav(interaction, 'tracker.hunger')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))

    @discord.ui.button(label='Attributes Page', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.green, row=1)
    async def attributes_page_button_callback(self, interaction, button):
        response_embed, response_view = await vPS.pageEVNav(interaction, 'tracker.attributes')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))

    @discord.ui.button(label='Skills Page', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.green, row=2)
    async def skills_page_button_callback(self, interaction, button):
        response_embed, response_view = await vPS.pageEVNav(interaction, 'tracker.skills')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))

    @discord.ui.button(label='Disciplines Page', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.green, row=2)
    async def disciplines_page_button_callback(self, interaction, button):
        response_embed, response_view = await vPS.pageEVNav(interaction, 'tracker.discipline')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))

    @discord.ui.button(label='Extras Page', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.green, row=2)
    async def extras_page_button_callback(self, interaction, button):
        response_embed, response_view = await vPS.pageEVNav(interaction, 'tracker.extras')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))


class KTV_HPWP(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Home Page', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=0)
    async def home_button_callback(self, interaction, button):
        response_embed, response_view = await vPS.pageEVNav(interaction, 'tracker.home')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))

    @discord.ui.button(label='Damage Health', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.gray, row=1)
    async def health_damage_button_callback(self, interaction, button):
        response_embed, response_view = await vPS.pageEVNav(interaction, 'tracker.home')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))

    @discord.ui.button(label='Regain Health', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.gray, row=1)
    async def health_regain_button_callback(self, interaction, button):
        response_embed, response_view = await vPS.pageEVNav(interaction, 'tracker.home')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))

    @discord.ui.button(label='Damage Willpower', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.gray, row=1)
    async def willpower_damage_button_callback(self, interaction, button):
        response_embed, response_view = await vPS.pageEVNav(interaction, 'tracker.home')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))

    @discord.ui.button(label='Regain Willpower', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.gray, row=1)
    async def willpower_regain_button_callback(self, interaction, button):
        response_embed, response_view = await vPS.pageEVNav(interaction, 'tracker.home')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))


class KTV_HUNGER(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Home Page', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=0)
    async def home_button_callback(self, interaction, button):
        response_embed, response_view = await vPS.pageEVNav(interaction, 'tracker.home')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))

    @discord.ui.button(label='Hunt [Predator-Type]', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.gray, row=1)
    async def predhunt_button_callback(self, interaction, button):
        response_embed, response_view = await vPS.pageEVNav(interaction, 'tracker.home')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))

    @discord.ui.button(label='Hunt [Select]', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.gray, row=1)
    async def hunt_button_callback(self, interaction, button):
        response_embed, response_view = await vPS.pageEVNav(interaction, 'tracker.home')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))

    @discord.ui.button(label='Rouse', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.gray, row=1)
    async def rouse_button_callback(self, interaction, button):
        response_embed, response_view = await vPS.pageEVNav(interaction, 'tracker.home')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))


class KTV_ATTRIBUTE(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Home Page', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=0)
    async def home_button_callback(self, interaction, button):
        response_embed, response_view = await vPS.pageEVNav(interaction, 'tracker.home')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))

    @discord.ui.button(label='Roll', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.gray, row=1)
    async def roll_button_callback(self, interaction, button):
        # ! Send to Roller
        response_embed, response_view = await vPS.pageEVNav(interaction, 'tracker.home')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))


class KTV_SKILL(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Home Page', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=0)
    async def home_button_callback(self, interaction, button):
        response_embed, response_view = await vPS.pageEVNav(interaction, 'tracker.home')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))

    @discord.ui.button(label='Physical Skills Page', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.green, row=1)
    async def physical_skills_button_callback(self, interaction, button):
        response_embed, response_view = await vPS.pageEVNav(interaction, 'tracker.physical_skills')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))

    @discord.ui.button(label='Social Skills Page', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.green, row=1)
    async def social_skills_button_callback(self, interaction, button):
        response_embed, response_view = await vPS.pageEVNav(interaction, 'tracker.social_skills')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))

    @discord.ui.button(label='Mental Skills Page', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.green, row=2)
    async def mental_skills_button_callback(self, interaction, button):
        response_embed, response_view = await vPS.pageEVNav(interaction, 'tracker.mental_skills')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))

    @discord.ui.button(label='Roll', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.gray, row=2)
    async def roll_button_callback(self, interaction, button):
        # ! Send to Roller
        response_embed, response_view = await vPS.pageEVNav(interaction, 'tracker.home')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))


class KTV_DISCIPLINE(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Home Page', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=0)
    async def home_button_callback(self, interaction, button):
        response_embed, response_view = await vPS.pageEVNav(interaction, 'tracker.home')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))

    @discord.ui.button(label='Roll', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.gray, row=1)
    async def roll_button_callback(self, interaction, button):
        # ! Send to Roller
        response_embed, response_view = await vPS.pageEVNav(interaction, 'tracker.home')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))


class KTV_EXTRA(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Home Page', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=0)
    async def home_button_callback(self, interaction, button):
        response_embed, response_view = await vPS.pageEVNav(interaction, 'tracker.home')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))

    @discord.ui.button(label='Diablerie', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.gray, row=1)
    async def diablerie_button_callback(self, interaction, button):
        response_embed, response_view = await vPS.pageEVNav(interaction, 'tracker.home')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))

    @discord.ui.button(label='Remorse', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.gray, row=1)
    async def remorse_button_callback(self, interaction, button):
        response_embed, response_view = await vPS.pageEVNav(interaction, 'tracker.home')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))

    @discord.ui.button(label='Path Rules', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.gray, row=1)
    async def path_rules_button_callback(self, interaction, button):
        response_embed, response_view = await vPS.pageEVNav(interaction, 'tracker.home')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))
