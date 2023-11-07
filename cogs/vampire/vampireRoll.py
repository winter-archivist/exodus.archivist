from discord.ext import commands
from discord import app_commands
import discord
from discord.ui import View

from zenlog import log
import sqlite3
from random import randint

from misc import ashen_utils as au
from cogs.vampire.selections import selections as s

selection_embed = (discord.Embed(title='',
                                 description=f'',
                                 color=au.embed_colors["purple"]))

roll_embed = (discord.Embed(title='Roll',
                            description=f'',
                            color=au.embed_colors["purple"]))

roll_details_embed = (discord.Embed(title='Extra Details:',
                                    description=f'{au.ISSUE_CONTACT}',
                                    color=au.embed_colors["black"]))

not_enough_wp_embed = (discord.Embed(title='Willpower Reroll',
                                     description=f'You don\'t have enough willpower. {au.ISSUE_CONTACT}',
                                     color=au.embed_colors["red"]))

character = f'[THIS IS AN ISSUE] Send `[cN] Error.001`:\n {au.ISSUE_CONTACT}'
user = f'[THIS IS AN ISSUE] Send `[uV] Error.001`:\n {au.ISSUE_CONTACT}'
roll_pool, difficulty, result = 0, 0, 0
pool_composition = []
reroll_dict = {'r_crit'    : 0,
               'rh_crit'   : 0,
               'r_success' : 0,
               'rh_success': 0,
               'r_fail'    : 0,
               'rh_fail'   : 0,
               'rh_skull'  : 0
               }


# ! Yes I know this sucks.
async def rollDecide(embed, rolls, diffi):
    embed.clear_fields()
    r_crit, rh_crit, r_success, rh_success, r_fail, rh_fail, rh_skull = rolls

    crits = 0
    whileTotal = r_crit + rh_crit
    flag = 0

    while whileTotal > 0:
        if r_crit + rh_crit > 2:
            if r_crit >= 2:
                crits += 4
                r_crit -= 2

            elif rh_crit >= 2:
                crits += 4
                flag += 1
                rh_crit -= 2

            elif r_crit + rh_crit >= 2:
                crits += 4
                flag += 1
                break
        else:
            break
        whileTotal -= 1

    if flag > 0:
        flag = 'Messy Crit'

    crits += rh_crit + r_crit

    totalSuccesses = int(r_success + rh_success + crits)
    if totalSuccesses < int(diffi) and int(rh_skull) > 0:
        flag = 'Bestial Failure'
    elif totalSuccesses < int(diffi):
        flag = 'Fail'
    elif totalSuccesses >= int(diffi) and flag != 'Messy Crit':
        flag = 'Success'

    # ! This sucks, but is just for the user to see all the roll details, really just for clarity
    if r_crit > 0:
        embed.add_field(name='Crits:', value=f'{r_crit}', inline=True)
    if rh_crit > 0:
        embed.add_field(name='Hunger Crits:', value=f'{rh_crit}', inline=True)
    embed.add_field(name='', value='', inline=False)

    if r_success > 0:
        embed.add_field(name='Successes:', value=f'{r_success}', inline=True)
    if rh_success > 0:
        embed.add_field(name='Hunger Successes:', value=f'{rh_success}', inline=True)
    embed.add_field(name='', value='', inline=False)

    if r_fail > 0:
        embed.add_field(name='Fails:', value=f'{r_fail}', inline=True)
    if rh_fail > 0:
        embed.add_field(name='Hunger Fails:', value=f'{rh_fail}', inline=True)
    embed.add_field(name='', value='', inline=False)

    if rh_skull > 0:
        embed.add_field(name='Skulls:', value=f'{rh_skull}', inline=False)
    embed.add_field(name='', value='', inline=False)

    return (totalSuccesses, flag), embed


async def hungerGrab(target_character: str) -> int:
    db = sqlite3.connect(f'cogs//vampire//characters//{target_character}.sqlite')
    cursor = db.cursor()
    hunger_result_grab = cursor.execute('SELECT hungerCount FROM hunger')
    hunger_result = hunger_result_grab.fetchone()[0]
    db.close()
    return hunger_result


class AttributeView(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Next Step', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=4)
    async def stepper_button_callback(self, interaction, button):
        if str(interaction.user) != f'{user}':
            return

        selection_embed.set_field_at(index=0, name='Select Your:', value='Skill')
        await interaction.response.edit_message(embed=selection_embed, view=SkillView(self.CLIENT))

    @discord.ui.select(
        placeholder='Select physicalAttribute',
        min_values=1,
        max_values=3,
        options=s.physicalAttributeOptions)
    async def physicalAttribute_select_callback(self, interaction, select: discord.ui.Select):
        if str(interaction.user) != f'{user}':
            return

        global roll_pool, character, pool_composition
        targetTable = 'physicalAttributes'
        roll_pool = await s.basicSelection(character, select.values, roll_pool, pool_composition, targetTable, interaction)

    @discord.ui.select(
        placeholder='Select socialAttributes',
        min_values=1,
        max_values=3,
        options=s.socialAttributeOptions)
    async def socialAttribute_select_callback(self, interaction, select: discord.ui.Select):
        if str(interaction.user) != f'{user}':
            return

        global roll_pool, character, pool_composition
        targetTable = 'socialAttributes'
        roll_pool = await s.basicSelection(character, select.values, roll_pool, pool_composition, targetTable, interaction)

    @discord.ui.select(
        placeholder='Select mentalAttribute',
        min_values=1,
        max_values=3,
        options=s.mentalAttributeOptions)
    async def mentalAttribute_select_callback(self, interaction, select: discord.ui.Select):
        if str(interaction.user) != f'{user}':
            return

        global roll_pool, character, pool_composition
        targetTable = 'mentalAttributes'
        roll_pool = await s.basicSelection(character, select.values, roll_pool, pool_composition, targetTable, interaction)


class SkillView(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Next Step', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=4)
    async def stepper_button_callback(self, interaction, button):
        if str(interaction.user) != f'{user}':
            return

        selection_embed.set_field_at(index=0, name='Select Your:', value='Discipline')
        await interaction.response.edit_message(embed=selection_embed, view=DisciplineView(self.CLIENT))

    @discord.ui.select(
        placeholder='Select physicalSkill',
        min_values=1,
        max_values=3,
        options=s.physicalSkillOptions)
    async def physicalSkill_select_callback(self, interaction, select: discord.ui.Select):
        if str(interaction.user) != f'{user}':
            return

        global roll_pool, character, pool_composition
        targetTable = 'physicalSkills'
        roll_pool = await s.basicSelection(character, select.values, roll_pool, pool_composition, targetTable, interaction)

    @discord.ui.select(
        placeholder='Select socialSkill',
        min_values=1,
        max_values=3,
        options=s.socialSkillOptions)
    async def socialSkill_select_callback(self, interaction, select: discord.ui.Select):
        if str(interaction.user) != f'{user}':
            return

        global roll_pool, character, pool_composition
        targetTable = 'socialSkills'
        roll_pool = await s.basicSelection(character, select.values, roll_pool, pool_composition, targetTable, interaction)

    @discord.ui.select(
        placeholder='Select mentalSkill',
        min_values=1,
        max_values=3,
        options=s.mentalSkillOptions)
    async def mentalSkill_select_callback(self, interaction, select: discord.ui.Select):
        if str(interaction.user) != f'{user}':
            return

        global roll_pool, character, pool_composition, pool_composition
        targetTable = 'mentalSkills'
        roll_pool = await s.basicSelection(character, select.values, roll_pool, pool_composition, targetTable, interaction)


class DisciplineView(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Next Step', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=4)
    async def stepper_button_callback(self, interaction, button):
        if str(interaction.user) != f'{user}':
            return

        selection_embed.set_field_at(index=0, name='Select Your:', value='Extra')
        await interaction.response.edit_message(embed=selection_embed, view=ExtraView(self.CLIENT))

    @discord.ui.select(
        placeholder='Select disciplines',
        options=s.disciplineOptions)
    async def discipline_select_callback(self, interaction, select: discord.ui.Select):
        if str(interaction.user) != f'{user}':
            return

        global roll_pool, character, pool_composition
        targetTable = 'disciplines'
        roll_pool = await s.basicSelection(character, select.values, roll_pool, pool_composition, targetTable, interaction)


class ExtraView(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.select(
        placeholder='Select Extras',
        options=s.extraOptions)
    async def extra_select_callback(self, interaction, select: discord.ui.Select):
        if str(interaction.user) != f'{user}':
            return

        global roll_pool
        forVar = 0

        for x in select.values:
            roll_pool += int(select.values[forVar])
            pool_composition.append(f'{int(select.values[forVar])}')
            forVar += 1

        await interaction.response.edit_message()

    @discord.ui.button(label='Roll', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.green, row=1)
    async def roll_button_callback(self, interaction, button):
        global user
        if str(interaction.user) != f'{user}':
            return

        global roll_pool, character, difficulty, result, pool_composition
        # r = roll
        # rh = roll hunger
        # TODO : kill me
        r_crit = 0; rh_crit = 0

        r_success = 0; rh_success = 0

        r_fail = 0; rh_fail = 0

        rh_skull = 0

        hunger_count = await hungerGrab(character)

        roll_embed.add_field(name='Pool:', value=f'{roll_pool} | {" + ".join(pool_composition)}', inline=True)

        whilePool = roll_pool
        while 0 < whilePool:
            die_result = randint(1, 10)

            match hunger_count:

                case 0:  # No Hunger
                    match die_result:
                        case 10:
                            r_crit += 1
                        case 9 | 8 | 7 | 6:
                            r_success += 1
                        case 5 | 4 | 3 | 2 | 1:
                            r_fail += 1
                        case _:
                            await interaction.response.send_message(
                                msg=f'[THIS IS AN ISSUE] Send `[!H] Error.001`:\n {au.ISSUE_CONTACT}')

                case 1 | 2 | 3 | 4 | 5:
                    hunger_count -= 1
                    match die_result:
                        case 10:
                            rh_crit += 1
                        case 9 | 8 | 7 | 6:
                            rh_success += 1
                        case 5 | 4 | 3 | 2:
                            rh_fail += 1
                        case 1:
                            rh_skull += 1
                        case _:
                            await interaction.response.send_message(
                                msg=f'[THIS IS AN ISSUE] Send `[regR.H] Error.001`:\n {au.ISSUE_CONTACT}')

                case _:
                    await interaction.response.send_message(f'[THIS IS AN ISSUE] Send `[regR] Error.003 {die_result} {hunger_count}`:\n {au.ISSUE_CONTACT}')

            whilePool -= 1

        reroll_dict['r_crit', 'rh_crit', 'r_success', 'rh_success', 'r_fail', 'rh_fail', 'rh_skull'] = (
            r_crit, rh_crit, r_success, rh_success, r_fail, rh_fail, rh_skull)

        die_results_packed = (r_crit, rh_crit, r_success, rh_success, r_fail, rh_fail, rh_skull)
        result, specEmbed = await rollDecide(roll_details_embed, die_results_packed, difficulty)

        roll_embed.add_field(name='Result:', value=f'{result[0]} | {result[1]}', inline=False)

        await interaction.response.edit_message(embed=roll_embed, view=RerollView(self.CLIENT))
        await interaction.followup.send(embed=specEmbed, ephemeral=True)


class RerollView(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Willpower Reroll', emoji='<:bloodT:555804549173084160>', style=discord.ButtonStyle.red, row=0)
    async def reroll_button_callback(self, interaction, button):
        if str(interaction.user) != f'{user}':
            return

        global result, reroll_dict, difficulty, character

        db = sqlite3.connect(f'cogs//vampire//characters//{character}.sqlite')
        cursor = db.cursor()
        wp_base = cursor.execute('SELECT willpowerBase FROM willpower').fetchone()[0]
        wp_SUP = cursor.execute('SELECT willpowerSUP FROM willpower').fetchone()[0]
        wp_AGG = cursor.execute('SELECT willpowerAGG FROM willpower').fetchone()[0]

        if wp_base <= wp_AGG:
            await interaction.response.edit_message(embed=not_enough_wp_embed, view=None)
            db.close()
            return
        elif wp_base <= wp_SUP:
            cursor.execute('UPDATE willpower SET willpowerAGG=?', (str(wp_AGG + 1),))
            db.commit()
            db.close()
        else:
            cursor.execute('UPDATE willpower SET willpowerSUP=?', (str(wp_SUP + 1),))
            db.commit()
            db.close()

        r_crit, rh_crit, r_success, rh_success, r_fail, rh_fail, rh_skull = reroll_dict[
            'r_crit', 'rh_crit', 'r_success', 'rh_success', 'r_fail', 'rh_fail', 'rh_skull']

        rerollCount = r_fail
        if rerollCount > 3:
            rerollCount = 3

        r_fail -= 3

        while 0 < rerollCount:
            die_result = randint(1, 10)

            match die_result:
                case 10:
                    r_crit += 1
                case 9 | 8 | 7 | 6:
                    r_success += 1
                case 5 | 4 | 3 | 2 | 1:
                    r_fail += 1
                case _:
                    await interaction.response.send_message(
                        masg=f'[THIS IS AN ISSUE] Send `[regR.!H] Error.002`:\n {au.ISSUE_CONTACT}')

            rerollCount -= 1

        die_results_packed = (r_crit, rh_crit, r_success, rh_success, r_fail, rh_fail, rh_skull)
        reroll_result, specEmbed = await rollDecide(roll_details_embed, die_results_packed, difficulty)

        roll_embed.add_field(name='New Result:', value=f'{reroll_result[0]} | {reroll_result[1]}', inline=True)

        await interaction.response.edit_message(embed=roll_embed, view=None)
        await interaction.followup.send(embed=specEmbed, ephemeral=True)


# * Commands are here
class VampireRoll(commands.Cog):
    def __init__(self, CLIENT):
        self.CLIENT = CLIENT

    @app_commands.command(name="vroll", description="Vampire: The Masquerade v5 Roller & Char Tracker")
    @app_commands.describe(charactername='Character Name')
    @app_commands.describe(rolldifficulty='Roll Difficulty')
    async def vroll(self, interaction: discord.Interaction, charactername: str, rolldifficulty: str):
        if not isinstance(interaction.channel, discord.channel.DMChannel):
            await interaction.channel.purge(limit=1)
        db = sqlite3.connect(f'cogs//vampire//characters//{charactername}.sqlite')
        cursor = db.cursor()
        charOwnerResultGrab = cursor.execute('SELECT userID FROM charOwner')
        charOwnerResult = charOwnerResultGrab.fetchone()[0]
        db.close()
        char_owner = charOwnerResult

        if char_owner != f'{interaction.user}':
            return

        roll_details_embed.clear_fields()
        selection_embed.clear_fields()
        roll_embed.clear_fields()

        selection_embed.add_field(name='Select Your:', value='Attribute')

        global roll_pool, result, reroll_dict, pool_composition  # Clears Prior Runs from Vars
        roll_pool, result, = 0, 0
        reroll_dict['r_crit', 'rh_crit', 'r_success', 'rh_success', 'r_fail', 'rh_fail', 'rh_skull'] = 0, 0, 0, 0, 0, 0, 0
        pool_composition = []

        global character, difficulty, user  # Converts prior runs into current
        character, difficulty, user = charactername, rolldifficulty, interaction.user

        await interaction.response.send_message(embed=selection_embed, view=AttributeView(self.CLIENT))

    @app_commands.command(name="blankmake", description="Makes a blank vampire DB")
    @app_commands.describe(targetcharacter='Character Name')
    async def blankmake(self, interaction: discord.Interaction, targetcharacter: str):
        if not isinstance(interaction.channel, discord.channel.DMChannel):
            await interaction.channel.purge(limit=1)
        if int(interaction.user.id) == int(au.RUNNER_ID):
            db = sqlite3.connect(f'cogs//vampire//characters//{targetcharacter}.sqlite')
            cursor = db.cursor()
            # Blank Vampire database Maker

            # Physical
            cursor.execute('CREATE TABLE IF NOT EXISTS physicalAttributes(strength INTEGER, dexterity INTEGER, stamina INTEGER)')
            cursor.execute(
                'CREATE TABLE IF NOT EXISTS physicalSkills(athletics INTEGER, brawl INTEGER, craft INTEGER, drive INTEGER, '
                'firearms INTEGER, larceny INTEGER, melee INTEGER, stealth INTEGER, survival INTEGER)')

            # Social
            cursor.execute(
                'CREATE TABLE IF NOT EXISTS socialAttributes(charisma INTEGER, manipulation INTEGER, composure INTEGER)')
            cursor.execute(
                'CREATE TABLE IF NOT EXISTS socialSkills(animal_ken INTEGER, etiquette INTEGER, insight INTEGER, intimidation INTEGER, '
                'leadership INTEGER, performance INTEGER, persuasion INTEGER, streetwise INTEGER, subterfuge INTEGER)')

            # Mental
            cursor.execute('CREATE TABLE IF NOT EXISTS mentalAttributes(intelligence INTEGER, wits INTEGER, resolve INTEGER)')
            cursor.execute(
                'CREATE TABLE IF NOT EXISTS mentalSkills(academics INTEGER, awareness INTEGER, finance INTEGER, investigation INTEGER, '
                'medicine INTEGER, occult INTEGER, politics INTEGER, science INTEGER, technology INTEGER)')

            # Disciplines
            cursor.execute('CREATE TABLE IF NOT EXISTS disciplines('
                           'obfuscate INTEGER, animalism INTEGER, potence INTEGER, dominate INTEGER, '
                           'auspex INTEGER, protean INTEGER, fortitude INTEGER, thin_blood_alchemy, '
                           'chemeristry INTEGER, seven INTEGER, myr INTEGER, selena INTEGER)')

            # Other
            cursor.execute(
                'CREATE TABLE IF NOT EXISTS willpower(willpowerBase INTEGER, willpowerSUP INTEGER, willpowerAGG INTEGER)')
            cursor.execute('CREATE TABLE IF NOT EXISTS health(healthBase INTEGER, healthSUP INTEGER, healthAGG INTEGER)')
            cursor.execute('CREATE TABLE IF NOT EXISTS hunger(hungerCount INTEGER)')
            cursor.execute('CREATE TABLE IF NOT EXISTS charOwner(userID TEXT)')

            # Basic Value Input into Blank Vampire DB

            # Physical
            cursor.execute('INSERT INTO physicalAttributes (strength, dexterity, stamina) VALUES(1,2,3)')
            cursor.execute(
                'INSERT INTO physicalSkills (athletics, brawl, craft, drive, firearms, larceny, melee, stealth, survival) '
                'VALUES(1,2,3,4,5,6,7,8,9)')

            # Social
            cursor.execute('INSERT INTO socialAttributes (charisma, manipulation, composure) VALUES(1,2,3)')
            cursor.execute('INSERT INTO socialSkills (animal_ken, etiquette, insight, intimidation, leadership, performance, '
                           'persuasion, streetwise, subterfuge)'
                           'VALUES(1,2,3,4,5,6,7,8,9)')

            # Mental
            cursor.execute('INSERT INTO mentalAttributes (intelligence, wits, resolve) VALUES(1,2,3)')
            cursor.execute('INSERT INTO mentalSkills (academics, awareness, finance, investigation, medicine, occult, '
                           'politics, science, technology)'
                           'VALUES(1,2,3,4,5,6,7,8,9)')

            # Disciplines
            # seven is Temporis
            # myr is Dementation
            # selena is Nihilistics
            cursor.execute('INSERT INTO disciplines('
                           'obfuscate, animalism, potence, dominate, '
                           'auspex, protean, fortitude, thin_blood_alchemy, '
                           'chemeristry, seven, myr, selena)'
                           'VALUES(1,1,1,1, 1,1,1,1, 1,1,1,1)')

            # Other
            cursor.execute('INSERT INTO willpower (willpowerBase, willpowerSUP, willpowerAGG) VALUES(5,0,0)')
            cursor.execute('INSERT INTO health (healthBase, healthSUP, healthAGG) VALUES(5,0,0)')
            cursor.execute('INSERT INTO hunger (hungerCount) VALUES(1)')
            cursor.execute('INSERT INTO charOwner (userID) VALUES("")')
            db.commit()
            db.close()


async def setup(CLIENT):
    await CLIENT.add_cog(VampireRoll(CLIENT))