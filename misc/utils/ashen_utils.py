import discord
from zenlog import log
import yaml
import sqlite3
import os
# ? Used Across Bot
DEVELOPER: str = '.ashywinter'  # ! if you need to contact who wrote this awful code
GITREPO: str = 'https://github.com/AshenEntropy/.ae_rewrite'  # ! if you need to contact who wrote this awful code
DEVLOG: str = 'https://ashenentropy.github.io/ashenDevlog/'  # ? To witness my horrid planning, BE WARNED: ITS PURE WEB1 BAD
RUNNER: str = f'{os.environ["RUNNER"]}'  # ? This should be your DISCORD userNAME (Not your DISCORD userID)
RUNNER_ID: str = f'{os.environ["RUNNER_ID"]}'  # ? This should be your DISCORD userID (Not your DISCORD userNAME)
ISSUE_CONTACT: str = (f'If you believe there is an issue, screenshot this and send it to `{RUNNER}`, the host of this bot. \n'
                      f'To contact the original bot writer: {DEVELOPER}` and/or visit `{GITREPO}`')
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
