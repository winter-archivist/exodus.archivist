import discord
from zenlog import log
import yaml
import sqlite3

embed_colors = {
    "white": 0xFFFFFF,
    "black": 0x000000,
    "purple": 0x800080,
    "red": 0xFF0000,
    "blue": 0x0000FF,
    "dark_yellow": 0x8B8000,
    "cyan": 0x00FFF
}


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
