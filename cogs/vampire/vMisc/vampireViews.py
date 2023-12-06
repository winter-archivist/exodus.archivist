import discord
import sqlite3
from zenlog import log
from discord.ui import View

import cogs.vampire.vMisc.vampireFunctions as vF
import cogs.vampire.vMisc.vampireEmbeds as vE
import cogs.vampire.vMisc.vampireOptions as vO


class StandardStartSelectionView(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Next Step', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=1)
    async def stepper_button_callback(self, interaction, button):
        targetcharacter = await vF.ownerChecker(interaction)
        if targetcharacter is str:
            pass
        elif targetcharacter is False:
            return

        await vF.selectionEmbedSetter(interaction, targetcharacter)

        await interaction.response.edit_message(embed=vE.selection_embed, view=StandardSelectionView(self.CLIENT))

    @discord.ui.button(label='Blood Surge', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.red, row=1)
    async def blood_surge_button_callback(self, interaction, button):
        targetcharacter = await vF.ownerChecker(interaction)
        if targetcharacter is str:
            pass
        elif targetcharacter is False:
            return

        rouse_result = await vF.rouseCheck(interaction, targetcharacter)
        if rouse_result in ('Frenzy', 'Hungry'):
            button.disabled = True
            button.style = discord.ButtonStyle.gray

            if rouse_result == 'Frenzy':
                button.label = 'Broken Chains.'
                # ! DO FRENZY STUFF HERE

            elif rouse_result == 'Hungry':
                button.label = 'Too Hungry, Feast.'

            await interaction.response.edit_message(view=self)
            return
        elif rouse_result == 'Pass':
            button.label = 'The Beast\'s Lock Rattles, Hunger Avoided.'
        elif rouse_result == 'Fail':
            button.label = 'Blood Boils Within, Hunger Gained.'

        try:
            with sqlite3.connect(f'cogs//vampire//characters//{str(interaction.user.id)}//{targetcharacter}.sqlite') as db:
                cursor = db.cursor()

                bp = int(cursor.execute('SELECT blood_potency FROM charInfo').fetchone()[0])
                bp_mapping = {1: 2, 2: 2, 3: 3, 4: 3, 5: 4, 6: 5}
                bp_add = bp_mapping[bp]

                new_roll_pool = int(cursor.execute('SELECT rollPool FROM commandvars').fetchone()[0] + bp_add)
                cursor.execute('UPDATE commandvars SET rollPool=?', (new_roll_pool,))
                cursor.execute('UPDATE commandvars SET poolComp=?', (f"Blood Surge[{bp_add}]",))
                db.commit()

                await vF.selectionEmbedSetter(interaction, targetcharacter)

                button.disabled = True
                button.style = discord.ButtonStyle.gray
                await interaction.response.edit_message(embed=vE.selection_embed, view=self)
        except sqlite3.Error as e:
            log.error(f'blood_surge_button_callback | SQLITE3 ERROR | {e}')

    @discord.ui.select(placeholder='Select Difficulty', options=vO.difficulty_options, max_values=1, min_values=1, row=0)
    async def difficulty_select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        targetcharacter = await vF.ownerChecker(interaction)
        if targetcharacter is str:
            pass
        elif targetcharacter is False:
            return
        try:
            with sqlite3.connect(f'cogs//vampire//characters//{str(interaction.user.id)}//{targetcharacter}.sqlite') as db:
                db.cursor().execute('UPDATE commandvars SET difficulty=?', (select.values))  # ! Parentheses are NOT redundant
                db.commit()

                await vF.selectionEmbedSetter(interaction, targetcharacter)

                await interaction.response.edit_message(embed=vE.selection_embed, view=self)
        except sqlite3.Error as e:
            log.error(f'difficulty_select_callback | SQLITE3 ERROR | {e}')


class StandardSelectionView(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Next Step', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=4)
    async def stepper_button_callback(self, interaction, button):
        targetcharacter = await vF.ownerChecker(interaction)
        if targetcharacter is str:
            pass
        elif targetcharacter is False:
            return

        await vF.selectionEmbedSetter(interaction, targetcharacter)

        await interaction.response.edit_message(embed=vE.selection_embed, view=StandardDisciplineSelectionView(self.CLIENT))

    @discord.ui.select(placeholder='Select Attributes', min_values=1, max_values=3, options=vO.attribute_options, row=0)
    async def attribute_select_callback(self, interaction, select: discord.ui.Select):
        await vF.simpleSelection(interaction, select, self, 'charAttributes', 'attribute_select_callback')

    @discord.ui.select(placeholder='Select Physical Skills', min_values=1, max_values=3, options=vO.physical_skill_options, row=1)
    async def physical_skill_select_callback(self, interaction, select: discord.ui.Select):
        await vF.simpleSelection(interaction, select, self, 'physicalSkills', 'physical_skill_select_callback')

    @discord.ui.select(placeholder='Select Social Skills', min_values=1, max_values=3, options=vO.social_skill_options, row=2)
    async def social_skill_select_callback(self, interaction, select: discord.ui.Select):
        await vF.simpleSelection(interaction, select, self, 'socialSkills', 'social_skill_select_callback')

    @discord.ui.select(placeholder='Select Mental Skills', min_values=1, max_values=3, options=vO.mental_skill_options, row=3)
    async def mental_skill_select_callback(self, interaction, select: discord.ui.Select):
        await vF.simpleSelection(interaction, select, self, 'mentalSkills', 'mental_skill_select_callback')


class StandardDisciplineSelectionView(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Next Step', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=4)
    async def stepper_button_callback(self, interaction, button):
        targetcharacter = await vF.ownerChecker(interaction)
        if targetcharacter is str:
            pass
        elif targetcharacter is False:
            return

        await vF.selectionEmbedSetter(interaction, targetcharacter)

        await interaction.response.edit_message(embed=vE.selection_embed, view=StandardExtraSelectionView(self.CLIENT))
        
    @discord.ui.button(label='Roll', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.green, row=4)
    async def roll_button_callback(self, interaction, button):
        targetcharacter = await vF.ownerChecker(interaction)
        if targetcharacter is str:
            pass
        elif targetcharacter is False:
            return

        await vF.normalRoller(interaction, self, targetcharacter)

    @discord.ui.select(placeholder='Select Discipline', min_values=1, options=vO.discipline_options)
    async def discipline_select_callback(self, interaction, select: discord.ui.Select):
        await vF.simpleSelection(interaction, select, self, 'disciplines', 'discipline_select_callback')


class StandardExtraSelectionView(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Next Step', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=4)
    async def stepper_button_callback(self, interaction, button):
        targetcharacter = await vF.ownerChecker(interaction)
        if targetcharacter is str:
            pass
        elif targetcharacter is False:
            return

        await vF.selectionEmbedSetter(interaction, targetcharacter)

        await interaction.response.edit_message(embed=vE.selection_embed, view=StandardRollView(self.CLIENT))

    @discord.ui.button(label='Roll', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.green, row=4)
    async def roll_button_callback(self, interaction, button):
        targetcharacter = await vF.ownerChecker(interaction)
        if targetcharacter is str:
            pass
        elif targetcharacter is False:
            return

        await vF.normalRoller(interaction, self, targetcharacter)

    @discord.ui.select(placeholder='Select Extra', min_values=1, options=vO.extra_options)
    async def extra_select_callback(self, interaction, select: discord.ui.Select):
        targetcharacter = await vF.ownerChecker(interaction)
        if targetcharacter is str:
            pass
        elif targetcharacter is False:
            return

        try:
            with sqlite3.connect(f'cogs//vampire//characters//{str(interaction.user.id)}//{targetcharacter}.sqlite') as db:
                cursor = db.cursor()

                roll_pool = int(cursor.execute('SELECT rollPool FROM commandvars').fetchone()[0])
                roll_comp = cursor.execute('SELECT poolComp from commandVars').fetchone()[0]

                extra_value = select.values[0]
                roll_pool += int(extra_value)
                roll_comp = f'{roll_comp} + Extra[{extra_value}]'

                cursor.execute('UPDATE commandvars SET poolComp=?', (roll_comp,))
                cursor.execute('UPDATE commandvars SET rollPool=?', (roll_pool,))
                db.commit()

                await vF.selectionEmbedSetter(interaction, targetcharacter)

                select.disabled = True
                await interaction.response.edit_message(embed=vE.selection_embed, view=self)
        except sqlite3.Error as e:
            log.error(f'extra_select_callback | SQLITE3 ERROR | {e}')


class StandardRollView(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Roll', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.green, row=0)
    async def roll_button_callback(self, interaction, button):
        targetcharacter = await vF.ownerChecker(interaction)
        if targetcharacter is str:
            pass
        elif targetcharacter is False:
            return

        await vF.normalRoller(interaction, self, targetcharacter)


class StandardRerollView(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Reroll', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.red, row=1)
    async def roll_button_callback(self, interaction, button):
        targetcharacter = await vF.ownerChecker(interaction)
        if targetcharacter is str:
            pass
        elif targetcharacter is False:
            return

        await vF.reRoller(interaction, self, targetcharacter, button)
