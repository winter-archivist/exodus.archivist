import discord
from zenlog import log
import yaml
import sqlite3

vePCDBLocation = 'cogs\\shared\\database\\vampire\\'

embed_colors = {
    "white": 0xFFFFFF,
    "black": 0x000000,
    "purple": 0x800080,
    "red": 0xFF0000,
    "blue": 0x0000FF,
    "dark_yellow": 0x8B8000,
    "cyan": 0x00FFF
}


async def roleCheck(targetUser, ctx, roleName):
    checkRole = discord.utils.find(lambda ringo: ringo.name == f'{roleName}', ctx.message.guild.roles)
    if checkRole in targetUser.roles:
        return True
    else:
        return False


async def cacheHandler(*, primaryRunType=None, secondaryRunType=None, targetCache=None, dataInput=None, searchFor=None):

    if primaryRunType == '-r':  # Read data from cache

        if targetCache is None:
            log.critical('*> No `targetCache` passed into `cacheHandler` for `-r` runType')
            return

        with open(f'{targetCache}', 'r') as file:
            data = yaml.safe_load(file)
        return data

    elif primaryRunType == '-w' and isinstance(dataInput, dict):
        if targetCache is None:
            log.critical('*> No `targetCache` passed into `cacheHandler` for `-w` runType')
            return
        if dataInput is None:
            log.critical('*> No `dataInput` passed into `cacheHandler` for `-w` runType')
            return

        with open(f'{targetCache}', 'a' if dataInput else 'w') as file:
            yaml.dump(dataInput, file)

    elif primaryRunType == '-e':  # simple exist check
        if targetCache is None:
            log.critical('*> No `targetCache` passed into `cacheHandler` for `-e` runType')
            return

        with open(f'{targetCache}', 'r') as file:
            data = yaml.safe_load(file)
        if data is None:  # Checks if Data even Exists, this prevents error caused by checking for something in nothing
            return None
        elif searchFor in data:
            return True
        else:
            return False

    if secondaryRunType == '--c':  # Clears the target YAML file
        if targetCache is None:
            log.critical('*> No `fileName` passed into `cacheHandler` for `-c` runType')
            return
        with open(f'{targetCache}', 'w') as file:
            pass


async def cacheRead(targetCache):
    with open(f'{targetCache}', 'r') as file:
        data = yaml.safe_load(file)
    return data


async def cacheWrite(targetCache, dataInput):
    with open(f'{targetCache}', 'a' if dataInput else 'w') as file:
        yaml.dump(dataInput, file)


async def cacheClear(targetCache):
    with open(f'{targetCache}', 'w') as file:
        pass


async def cacheDataExist(targetCache, searchFor):
    with open(f'{targetCache}', 'r') as file:
        data = yaml.safe_load(file)
    if data is None:  # Checks if Data even Exists, this prevents error caused by checking for something in nothing
        return None
    elif searchFor in data:
        return True
    else:
        return False


async def dbRead(*, targetDB, targetTable, readFor, condOne, condTwo):
    db = sqlite3.connect(f'{targetDB}.sqlite')
    cursor = db.cursor()
    cursor.execute(f'SELECT {readFor} FROM {targetTable} WHERE {condOne}="{condTwo}"')
    return cursor.fetchall()


async def dbWrite(*, targetDB, dbColumn, writeInfo, condOne, condTwo):
    db = sqlite3.connect(f'{targetDB}.sqlite')
    cursor = db.cursor()
    cursor.execute(f'UPDATE {targetDB} SET {dbColumn}="{writeInfo}" WHERE {condOne}="{condTwo}"')
    db.commit()
    return True


async def dbDelete(*, targetDB, removeThis):
    db = sqlite3.connect(f'{targetDB}.sqlite')
    cursor = db.cursor()
    print(f'DELETE {removeThis} FROM {targetDB}')
    cursor.execute(f'DELETE {removeThis} FROM {targetDB}')
    db.commit()
    return True


async def dbDataExistCheck(targetDB, checkFor, condOne, condTwo):
    db = sqlite3.connect(f'{targetDB}.sqlite')
    cursor = db.cursor()
    for row in cursor.execute(f'SELECT {checkFor} FROM {targetDB} WHERE {condOne}="{condTwo}"'):
        return True
    else:
        return False


async def dbMake(*, primaryRunType=None, secondaryRunType=None, targetDB=None, dataInput=None, searchFor=None):
    pass


async def embedHandler(*, primaryRunType, secondaryRunType=None, interaction=None, handled_embeds):

    if primaryRunType == '-$':  # Embed Initial Set

        if secondaryRunType == '--cm':  # Cog Manager
            cog_manager_embed = handled_embeds[0]
            yaml_error_embed = handled_embeds[1]
            cog_manager_embed.add_field(name='targetCog:', value=f'N/A', inline=False)
            cog_manager_embed.add_field(name='operationType:', value=f'N/A', inline=False)
            cog_manager_embed.add_field(name='Run: ', value=f'N/A', inline=False)
            yaml_error_embed.add_field(name='Issue:',
                                       value=f'OH SHIT STUFF FUCKED UP; PLEASE CONTACT `.ashywinter` ON DISCORD',
                                       inline=False)
            yaml_error_embed.add_field(name='Solution:', value=f'Cache Cleared', inline=False)
            log.info('> Embeds Set for CogManager...')

        if secondaryRunType == '--vr':  # veRoll
            pass

    elif primaryRunType == '-r':  # Resets an embed

        if interaction is None:  # Logs Error & returns
            log.critical('*> No `interaction` passed into `embedHandler` for `-r` primaryRunType')
            return

        if handled_embeds is None:
            log.critical('*> No `handled_embeds` passed into `embedHandler` for `-r` primaryRunType')
            return

        if secondaryRunType == '--cm':  # Cog Manager
            cog_manager_embed = handled_embeds

            cog_manager_embed.set_field_at(index=0, name='targetCog:', value=f'N/A', inline=False)
            cog_manager_embed.set_field_at(index=1, name='operationType:', value=f'N/A', inline=False)
            await interaction.response.edit_message(embed=cog_manager_embed)

    elif primaryRunType == '-u':  # updates selection with specification

        if interaction is None:  # Logs Error & returns
            log.critical('*> No `interaction` passed into `embedHandler` for `-u` runType')
            return

        # do real shit
        pass
