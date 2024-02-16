import discord
from discord import Embed, app_commands
from discord.ext import commands

import sqlite3
import os as os
from zenlog import log

from misc.config import mainConfig as mC

import cogs.vtm_toolbox.vtb_misc.vtbUtils as vU
import cogs.vtm_toolbox.vtb_misc.vtbPageSystem as vPS


class VampireRoll(commands.Cog):
    def __init__(self, CLIENT):
        self.CLIENT = CLIENT

    @app_commands.command(name='vampire-roll', description='VTM v5 Dice Roller!')
    @app_commands.describe(charactername='Character Name')
    async def VampireRoll(self, interaction: discord.Interaction, charactername: str):
        await vU.rollPrep(interaction, charactername)
        await vPS.vampirePageCommand(self, interaction, charactername, 'roller.difficulty', False)

    @app_commands.command(name='vampire-tracker', description='VTM v5 Character Tracker!')
    @app_commands.describe(character_name='Character Name')
    async def VampireTracker(self, interaction: discord.Interaction, character_name: str):
        await vPS.vampirePageCommand(self, interaction, character_name, 'tracker.home', True)

    @app_commands.command(name='dev-test', description='---DO NOT TOUCH---')
    @app_commands.describe(character_name='Character Name')
    async def DevTest(self, interaction: discord.Interaction, character_name: str):
        import cogs.vtm_toolbox.vtb_characters.vtb_character_manager as vtb_cm
        import json

        CHARACTER_NAME_FILE: str = f'cogs/vtm_toolbox/vtb_characters/{interaction.user.id}/target_character.json'
        CHARACTER_NAME_DICT: dict = {'character_name': character_name}

        with open(CHARACTER_NAME_FILE, "w") as operate_file:
            json.dump(CHARACTER_NAME_DICT, operate_file)

        await vtb_cm.make_character_file(interaction, character_name)

        try:
            character_class = vtb_cm.vtb_CharacterManager(interaction)
        except Exception == '':
            dev_test_embed = discord.Embed(title='`!__DEV__DEBUG__TESTS__!`',
                                           description='`!__ONLY__PRESS__THINGS__IF__INSTRUCTED__!`',
                                           color=mC.EMBED_COLORS['red'])
            dev_test_embed.add_field(name='Char Name', value=f'{character_name}', inline=True)
            dev_test_embed.add_field(name='Interactor ID', value=f'{interaction.user.id}', inline=True)
            dev_test_embed.add_field(name='YOU DO NOT OWN', value=f'{character_name}', inline=True)
            await interaction.response.send_message(embed=dev_test_embed, view=vtb_cm.vtb_DEV_TEST_VIEW(self.CLIENT))
        else:
            dev_test_embed = discord.Embed(title='`!__DEV__DEBUG__TESTS__!`', description='`!__ONLY__PRESS__THINGS__IF__INSTRUCTED__!`', color=mC.EMBED_COLORS['red'])
            dev_test_embed.add_field(name='Char Name', value=f'{character_class.CHARACTER_NAME}', inline=True)
            dev_test_embed.add_field(name='Char Owner ID', value=f'{character_class.OWNER_ID}', inline=True)
            dev_test_embed.add_field(name='Interactor ID', value=f'{interaction.user.id}', inline=True)

            await interaction.response.send_message(embed=dev_test_embed, view=vtb_cm.vtb_DEV_TEST_VIEW(self.CLIENT))

    @app_commands.command(name='vampire-img', description='Sets the character img for `vampire`')
    @app_commands.describe(charactername='Character Name')
    @app_commands.describe(characterimgurl='Character Image URL')
    async def VampireImgSet(self, interaction: discord.Interaction, charactername: str, characterimgurl: str):
        url_set_embed = Embed(title='URL Set', description='', color=mC.EMBED_COLORS["green"])
        url_set_embed.add_field(name='Success', value='', inline=False)
        targetDB = f'cogs//vampire//characters//{str(interaction.user.id)}//{charactername}//{charactername}.sqlite'
        log.debug(f'> Checking if [ {targetDB} ] exist')
        if not os.path.exists(targetDB):
            log.warn(f'*> Database [ {targetDB} ] does not exist')

            await interaction.response.send_message(embed=discord.Embed(
                title='Database Error', color=mC.EMBED_COLORS["red"],
                description=f'[ {charactername} ] Does Not Exist, Can\'t Set URL.'), ephemeral=True)

            return False
        else:
            log.debug(f'> Successful Connection to [ {targetDB} ] Setting URL')

        with sqlite3.connect(f'cogs//vampire//characters//{str(interaction.user.id)}//{charactername}//{charactername}.sqlite') as db:
            db.cursor().execute('UPDATE charInfo SET imgURL=?', (f'{characterimgurl}',))
            db.commit()
        log.debug(f'> [ {targetDB} ] URL Set to [ {characterimgurl} ]')

        with sqlite3.connect(f'cogs//vampire//characters//{str(interaction.user.id)}//{charactername}//{charactername}.sqlite') as db:
            found_url = db.cursor().execute('SELECT imgURL from charInfo').fetchone()[0]
            url_set_embed.set_thumbnail(url=f'{found_url}')
        log.debug(f'> Sending [ {characterimgurl} ] back to user')

        await interaction.response.send_message(embed=url_set_embed)

    @commands.command(hidden=True)
    async def new(self, ctx, targetcharacter: str):
        # ! I swear this command will be cleaned eventually
        if ctx.author.id == mC.RUNNER_ID:
            try:
                createdDirectory = f'{os.getcwd()}//cogs//vampire//characters//{str(ctx.author.id)}//{targetcharacter}'
                log.debug(f'Creating Directory [ {createdDirectory} ] if not created')
                os.makedirs(createdDirectory, exist_ok=True)
                log.debug(f'Directory [ {createdDirectory} ] Created')

                with sqlite3.connect(f'cogs//vampire//characters//{str(ctx.author.id)}//{targetcharacter}//{targetcharacter}.sqlite') as db:
                    cursor = db.cursor()
                    log.debug(f'Creation of [ {targetcharacter} ] Begun')
                    # ? These were sorted by the listing order in DB Browser

                    log.debug('Setting charAttributes')
                    cursor.execute('CREATE TABLE IF NOT EXISTS charAttributes(strength INTEGER, dexterity INTEGER, stamina INTEGER, charisma INTEGER, manipulation INTEGER, composure INTEGER, intelligence INTEGER, wits INTEGER, resolve INTEGER)')
                    cursor.execute('INSERT INTO charAttributes(strength, dexterity, stamina, charisma, manipulation, composure, intelligence, wits, resolve) VALUES(1,2,3, 1,2,3, 1,2,3)')

                    log.debug('Setting charInfo')
                    cursor.execute('CREATE TABLE IF NOT EXISTS charInfo(blood_potency INTEGER, clan TEXT, generation INTEGER, humanity INTEGER, bane_severity INTEGER, hunger INTEGER, predator_type TEXT, imgURL TEXT)')
                    cursor.execute('INSERT INTO charInfo (blood_potency, clan, generation, humanity, bane_severity, hunger, predator_type, imgURL) VALUES(1, "ExampleClan", 10, 7, 2, 1, "nom", "https://cdn.discordapp.com/attachments/1145636416584429609/1181774388522143824/remix-be94809d-97fd-4654-9a6a-57b02abefb01.png?ex=658b82aa&is=65790daa&hm=39a5c62fdf1e8e0c43f8928b655fdb917fec7cb7807f702f4c257ab078ccd624&")')

                    log.debug('Setting commandVars')
                    cursor.execute('CREATE TABLE IF NOT EXISTS commandVars(difficulty INTEGER, rollPool INTEGER, result INTEGER, poolComp TEXT)')
                    cursor.execute('INSERT INTO commandVars (difficulty, rollPool, result, poolComp) VALUES(0, 0, 0, "Stuff, And, Things")')

                    log.debug('Setting disciplines')
                    cursor.execute('CREATE TABLE IF NOT EXISTS disciplines('
                                   'obfuscate INTEGER, animalism INTEGER, potence INTEGER, dominate INTEGER, auspex INTEGER, protean INTEGER, presence INTEGER, fortitude INTEGER, '
                                   'thin_blood_alchemy INTEGER, blood_sorc INTEGER, chemeristry INTEGER, '
                                   'seven INTEGER, myr INTEGER, selena INTEGER, nyct1 INTEGER, nyct2 INTEGER, iilta INTEGER, elijah INTEGER)')
                    cursor.execute('INSERT INTO disciplines('
                                   'obfuscate, animalism, potence, dominate, auspex, protean, presence, fortitude, '
                                   'thin_blood_alchemy, blood_sorc, chemeristry, '
                                   'seven, myr, selena, nyct1, nyct2, iilta, elijah)'
                                   'VALUES(1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1)')

                    log.debug('Setting health')
                    cursor.execute('CREATE TABLE IF NOT EXISTS health(healthBase INTEGER, healthSUP INTEGER, healthAGG INTEGER)')
                    cursor.execute('INSERT INTO health (healthBase, healthSUP, healthAGG) VALUES(5,0,0)')

                    log.debug('Setting mentalSkills')
                    cursor.execute('CREATE TABLE IF NOT EXISTS mentalSkills(academics INTEGER, awareness INTEGER, finance INTEGER, investigation INTEGER, medicine INTEGER, occult INTEGER, politics INTEGER, science INTEGER, technology INTEGER)')
                    cursor.execute('INSERT INTO mentalSkills (academics, awareness, finance, investigation, medicine, occult, politics, science, technology) VALUES(1,2,3,4,5,6,7,8,9)')

                    log.debug('Setting ownerInfo')
                    cursor.execute('CREATE TABLE IF NOT EXISTS ownerInfo(userID INTEGER, userNAME TEXT)')
                    cursor.execute('INSERT INTO ownerInfo (userID, userNAME) VALUES(0, "nada")')
                    cursor.execute('UPDATE ownerInfo SET userID=?, userNAME=?', (int(ctx.author.id), f"{ctx.author}"))

                    log.debug('Setting physicalSkills')
                    cursor.execute('CREATE TABLE IF NOT EXISTS physicalSkills(athletics INTEGER, brawl INTEGER, craft INTEGER, drive INTEGER, firearms INTEGER, larceny INTEGER, melee INTEGER, stealth INTEGER, survival INTEGER)')
                    cursor.execute('INSERT INTO physicalSkills (athletics, brawl, craft, drive, firearms, larceny, melee, stealth, survival) VALUES(1,2,3,4,5,6,7,8,9)')

                    log.debug('Setting rerollInfo')
                    cursor.execute('CREATE TABLE IF NOT EXISTS rerollInfo(regularCritDie INTEGER, hungerCritDie INTEGER, regularSuccess INTEGER, hungerSuccess INTEGER, regularFail INTEGER, hungerFail INTEGER, hungerSkull INTEGER)')
                    cursor.execute('INSERT INTO rerollInfo (regularCritDie, hungerCritDie, regularSuccess, hungerSuccess, regularFail, hungerFail, hungerSkull) VALUES(0,0, 0,0, 0,0, 0)')

                    log.debug('Setting socialSkills')
                    cursor.execute('CREATE TABLE IF NOT EXISTS socialSkills(animal_ken INTEGER, etiquette INTEGER, insight INTEGER, intimidation INTEGER, leadership INTEGER, performance INTEGER, persuasion INTEGER, streetwise INTEGER, subterfuge INTEGER)')
                    cursor.execute('INSERT INTO socialSkills (animal_ken, etiquette, insight, intimidation, leadership, performance, persuasion, streetwise, subterfuge) VALUES(1,2,3,4,5,6,7,8,9)')

                    log.debug('Setting willpower')
                    cursor.execute('CREATE TABLE IF NOT EXISTS willpower(willpowerBase INTEGER, willpowerSUP INTEGER, willpowerAGG INTEGER)')
                    cursor.execute('INSERT INTO willpower (willpowerBase, willpowerSUP, willpowerAGG) VALUES(5,0,0)')

                    db.commit()
                    db.close()

                    log.debug(f'Creation of [ {targetcharacter} ] Successful')
                    await ctx.send('Make Complete')
            except sqlite3.Error as e:
                log.error(f'vampMaker | SQLITE3 ERROR | {e}')


async def setup(CLIENT):
    await CLIENT.add_cog(VampireRoll(CLIENT))
