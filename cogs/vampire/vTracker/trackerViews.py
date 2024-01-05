import discord
from discord.ui import View
import sqlite3
from zenlog import log

import cogs.vampire.vMisc.vampirePageSystem as vPS
import cogs.vampire.vMisc.vampireUtils as vU

from misc.config import mainConfig as mC

damage_options = [discord.SelectOption(label='One', value='1', emoji='<:snek:785811903938953227>'),
                  discord.SelectOption(label='Two', value='2', emoji='<:snek:785811903938953227>'),
                  discord.SelectOption(label='Three', value='3', emoji='<:snek:785811903938953227>'),
                  discord.SelectOption(label='Four', value='4', emoji='<:snek:785811903938953227>'),
                  discord.SelectOption(label='Five', value='5', emoji='<:snek:785811903938953227>'),
                  discord.SelectOption(label='Six', value='6', emoji='<:snek:785811903938953227>'),
                  discord.SelectOption(label='Seven', value='7', emoji='<:snek:785811903938953227>'),
                  discord.SelectOption(label='Eight', value='8', emoji='<:snek:785811903938953227>')]


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

    @discord.ui.button(label='Regain Health', emoji=f'{mC.health_full_emoji}', style=discord.ButtonStyle.green, row=1)
    async def health_regain_button_callback(self, interaction, button):
        response_embed, response_view = await vPS.pageEVNav(interaction, 'tracker.regain_health')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))

    @discord.ui.button(label='Damage Health', emoji=f'{mC.health_sup_emoji}', style=discord.ButtonStyle.red, row=1)
    async def health_damage_button_callback(self, interaction, button):
        response_embed, response_view = await vPS.pageEVNav(interaction, 'tracker.damage_health')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))

    @discord.ui.button(label='Regain Willpower', emoji=f'{mC.willpower_full_emoji}', style=discord.ButtonStyle.green, row=2)
    async def willpower_regain_button_callback(self, interaction, button):
        response_embed, response_view = await vPS.pageEVNav(interaction, 'tracker.regain_willpower')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))

    @discord.ui.button(label='Damage Willpower', emoji=f'{mC.willpower_sup_emoji}', style=discord.ButtonStyle.red, row=2)
    async def willpower_damage_button_callback(self, interaction, button):
        response_embed, response_view = await vPS.pageEVNav(interaction, 'tracker.damage_willpower')
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


class KTV_HPREGAIN(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Home Page', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=0)
    async def home_button_callback(self, interaction, button):
        response_embed, response_view = await vPS.pageEVNav(interaction, 'tracker.home')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))

    @discord.ui.button(label='Mend', emoji=f'{mC.hunger_emoji}', style=discord.ButtonStyle.red, row=1)
    async def mend_button_callback(self, interaction, button):

        character_name = await vU.getCharacterName(interaction)

        with sqlite3.connect(f'cogs//vampire//characters//{str(interaction.user.id)}//{character_name}//{character_name}.sqlite') as db:
            cursor = db.cursor()
            blood_potency = int(cursor.execute('SELECT blood_potency from charInfo').fetchone()[0])
            hc_sup: int = int(cursor.execute('SELECT healthSUP from health').fetchone()[0])

        # Prevents a Rouse from occurring if no health can be gained.
        if hc_sup == 0:
            response_embed, response_view = await vPS.pageEVNav(interaction, 'tracker.home')
            response_embed.add_field(name='No Superficial Health to Regain', value='')
            await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))
            return
        else:
            rouse_result = await vU.rouseCheck(interaction, character_name)

        if rouse_result == 'Frenzy':  # rouseCheck handles responding
            return

        if blood_potency <= 1: mend_amount = 1
        elif blood_potency <= 3: mend_amount = 2
        elif blood_potency <= 7: mend_amount = 3
        elif blood_potency <= 9: mend_amount = 4
        elif blood_potency == 10: mend_amount = 5
        else: return

        # Can't heal damage you don't have
        if mend_amount > hc_sup:
            mend_amount = hc_sup

        with sqlite3.connect(f'cogs//vampire//characters//{str(interaction.user.id)}//{character_name}//{character_name}.sqlite') as db:
            cursor = db.cursor()
            cursor.execute('UPDATE health SET healthSUP=?', (str(int(hc_sup) - mend_amount),))
            new_hunger = int(cursor.execute('SELECT hunger from charInfo').fetchone()[0])
            db.commit()

        response_embed, response_view = await vPS.pageEVNav(interaction, 'tracker.regain_health')
        response_embed.add_field(name=f'Rouse {rouse_result}', value=f'`{mend_amount}` Health Regained. Current Hunger: `{new_hunger}`')

        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))


class KTV_HPDAMAGE(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Home Page', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=0)
    async def home_button_callback(self, interaction, button):
        response_embed, response_view = await vPS.pageEVNav(interaction, 'tracker.home')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))

    @discord.ui.select(placeholder='Take Superficial Damage', options=damage_options, max_values=1, min_values=1, row=1)
    async def hp_sup_dmg_select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        character_name: str = await vU.getCharacterName(interaction)
        damage_amount: int = int(select.values[0])

        with sqlite3.connect(f'cogs//vampire//characters//{str(interaction.user.id)}//{character_name}//{character_name}.sqlite') as db:
            cursor = db.cursor()
            hc_base: int = int(cursor.execute('SELECT healthBase from health').fetchone()[0])

            while damage_amount > 0:
                hc_sup: int = int(cursor.execute('SELECT healthSUP from health').fetchone()[0])
                hc_agg: int = int(cursor.execute('SELECT healthAGG from health').fetchone()[0])

                if hc_base == hc_agg:
                    # Set up torpor logic later
                    # ! ENTER TORPOR
                    log.crit('Someone Torpor\'d')
                    quit()
                elif hc_sup == hc_base:
                    # Deals AGG Damage
                    cursor.execute('UPDATE health SET healthAGG=?', ((str(int(hc_agg + 1))),))  # ! Parentheses are NOT redundant
                else:
                    # Deals SUP Damage
                    cursor.execute('UPDATE health SET healthSUP=?', ((str(int(hc_sup + 1))),))  # ! Parentheses are NOT redundant

                damage_amount -= 1
                db.commit()

        response_page, response_view = await vPS.pageEVNav(interaction, 'tracker.hp/wp')
        await interaction.response.edit_message(embed=response_page, view=response_view(self.CLIENT))

    @discord.ui.select(placeholder='Take Aggravated Damage', options=damage_options, max_values=1, min_values=1, row=2)
    async def hp_agg_dmg_select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        character_name: str = await vU.getCharacterName(interaction)
        damage_amount: int = int(select.values[0])

        with sqlite3.connect(f'cogs//vampire//characters//{str(interaction.user.id)}//{character_name}//{character_name}.sqlite') as db:
            cursor = db.cursor()
            hc_base: int = int(cursor.execute('SELECT healthBase from health').fetchone()[0])

            while damage_amount > 0:
                hc_agg: int = int(cursor.execute('SELECT healthAGG from health').fetchone()[0])

                if hc_base == hc_agg:
                    # Set up torpor logic later
                    # ! ENTER TORPOR
                    log.crit('Someone Torpor\'d')
                    quit()

                # Deals AGG Damage
                cursor.execute('UPDATE health SET healthAGG=?', ((str(int(hc_agg + 1))),))  # ! Parentheses are NOT redundant

                damage_amount -= 1
                db.commit()

        response_page, response_view = await vPS.pageEVNav(interaction, 'tracker.hp/wp')
        await interaction.response.edit_message(embed=response_page, view=response_view(self.CLIENT))

