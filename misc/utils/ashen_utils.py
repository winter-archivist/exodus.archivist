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
