import discord
from discord import app_commands
from discord.ext import commands
from zenlog import log

import json
from random import SystemRandom
from string import ascii_uppercase, ascii_lowercase, digits
from os import mkdir, listdir

from misc.config import main_config as mc


async def get_games() -> tuple:
    return tuple(listdir('cogs/overseer/games'))


async def get_game_information(game: str) -> dict:
    GAME_PATH = f'cogs/overseer/games/{game}'

    with open(f'{GAME_PATH}/details.json', 'r') as operate_file:
        DETAILS: dict = json.load(operate_file)

    NAME: str = DETAILS['Name']
    SYSTEM: str = DETAILS['System']
    KEY: str = DETAILS['Key']
    MAX_PLAYERS: int = DETAILS['Max Players']

    with open(f'{GAME_PATH}/players.json', 'r') as operate_file:
        PLAYERS: dict = json.load(operate_file)

    return_var: dict = {'details':
                            {'Name': f'{NAME}', 'System': f'{SYSTEM}', 'Key': f'{KEY}', 'Max Players': f'{MAX_PLAYERS}'},
                        'players': PLAYERS
                        }
    return return_var


async def get_all_games_information() -> tuple:
    GAMES: tuple = await get_games()
    return_var: list = []
    for x in GAMES:
        return_var.append(await get_game_information(x))
    return tuple(return_var)


async def get_all_keys() -> tuple:
    GAMES: tuple = await get_games()
    return_var: list = []
    for_var: int = 0
    for x in GAMES:
        game_path = f'cogs/overseer/games/{GAMES[for_var]}'

        with open(f'{game_path}/details.json', 'r') as operate_file:
            details: dict = json.load(operate_file)
        return_var.append(details['Key'])
        for_var += 1
    return tuple(return_var)


async def key_gen(LENGTH: int) -> str:
    # Returns random LENGTH character long string that contains ascii upper/lower case, digits, and punctuation.
    # It does not check if the same key has been made before, its just so unlikely I don't feel like programming it in.
    key = ''.join(SystemRandom().choice(ascii_uppercase + ascii_lowercase + digits) for _ in range(LENGTH))
    log.debug(f'> Newly Generated Key: `{key}`')

    return key


class OverseerCog(commands.Cog):
    def __init__(self, CLIENT):
        self.CLIENT = CLIENT

    # Needs Manage, View, Join, Leave

    # This is a very temp setup, please ignore
    @app_commands.command(name="create-game", description="Creates Overseer Game")
    @discord.app_commands.describe(name='Name of The Game [!Unmodifiable!]',
                                   system='System being used for The Game. (ex: D&D)',
                                   max_players='Max Amount of Players (ex: 10, max/default:100)',)
    async def overseer_create_game(self, interaction: discord.Interaction, name: str, system: str, max_players: str = None):

        # ! TO BE REMOVED
        if str(interaction.user) != f'{mc.RUNNER}':
            # Prevents anyone, but the person running the bot, from interacting
            return
        # ! TO BE REMOVED

        # Checks for not permitted Characters in the name or system
        NOT_ALLOWED_CHARACTERS: tuple = ('<', '>', ':', '\\', '/', '|', '?', '*')
        for_var: int = 0
        for x in NOT_ALLOWED_CHARACTERS:

            if name.__contains__(NOT_ALLOWED_CHARACTERS[for_var]):
                response_embed = discord.Embed(title='Create Game', description='', colour=mc.EMBED_COLORS[f'red'])
                response_embed.set_footer(text=interaction.user.id, icon_url=interaction.user.display_avatar)
                response_embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar)
                response_embed.add_field(name='Failed Creation', value=f'**Invalid Character:** `{NOT_ALLOWED_CHARACTERS[for_var]}` in **Name:** `{name}`', inline=False)
                response_embed.add_field(name='All Invalid Characters', value=f'{" ".join(NOT_ALLOWED_CHARACTERS)}', inline=False)
                await interaction.response.send_message(embed=response_embed)
                return

            if system.__contains__(NOT_ALLOWED_CHARACTERS[for_var]):
                response_embed = discord.Embed(title='Create Game', description='', colour=mc.EMBED_COLORS[f'red'])
                response_embed.set_footer(text=interaction.user.id, icon_url=interaction.user.display_avatar)
                response_embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar)
                response_embed.add_field(name='Failed Creation', value=f'**Invalid Character:** `{NOT_ALLOWED_CHARACTERS[for_var]}` in **System:** `{system}`', inline=False)
                response_embed.add_field(name='All Invalid Characters', value=f'{" ".join(NOT_ALLOWED_CHARACTERS)}', inline=False)
                await interaction.response.send_message(embed=response_embed)
                return

            for_var += 1

        GAME_DIRECTORY: str = f'cogs/overseer/games/{name}'

        try:
            if max_players is None:
                max_players: int = 100
            if max_players > 100:
                max_players = 100
            max_players: int = int(max_players)  # I just want to make absolutely certain it is an int

            key: str = await key_gen(10)

            mkdir(GAME_DIRECTORY)
            log.debug(f'> Made dir {GAME_DIRECTORY} | {interaction.user.name} | {interaction.user.id}')

            GAME_FILES: tuple = ('details', 'players', 'placeholder')
            FILE_CONTENTS: tuple = (
                # Details File
                {'Name' : f'{name}', 'System' : f'{system}', 'Max Players': int(max_players), 'Key' : f'{key}'},

                # Players File
                {f'{interaction.user.id}' : {'Username' : f'{interaction.user.name}',
                                             'Public Tags' : ('Creator', 'Game Master', 'Overseer'),
                                             'Private Tags' : ('',)
                                             }
                 },

                # This placeholder is never read to, or written, feel free to delete it,
                # it's just here to make it clearer where to add additional files
                {'placeholder' : 'placeholder'})

            for_var: int = 0
            for x in GAME_FILES:
                with open(f'{GAME_DIRECTORY}/{GAME_FILES[for_var]}.json', 'w') as operate_file:
                    json.dump(FILE_CONTENTS[for_var], operate_file)
                log.debug(f'> Made Game {GAME_FILES[for_var]} | {interaction.user.name} | {interaction.user.id}')
                for_var += 1

        except Exception as e:
            log.crit(f'*> {interaction.user.name} | {interaction.user.id} failed at making new game.')
            log.crit(f'*> Game Details: {name} {system}')
            log.crit(f'*> Make Error: {e}')
            page: discord.Embed = discord.Embed(title='Overseer-Game-Create', description='Failed Creation', colour=mc.EMBED_COLORS[f"red"])
            page.add_field(name='Encountered Error', value=f'{e}', inline=False)
            return

        response_embed = discord.Embed(title='Create Game', description='', colour=mc.EMBED_COLORS[f'green'])
        response_embed.set_footer(text=interaction.user.id, icon_url=interaction.user.display_avatar)
        response_embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar)

        response_embed.add_field(name=f'Created {name}', value=f'{system}', inline=False)
        response_embed.add_field(name='Game Key', value=f'{key}', inline=False)

        log.crit(f'> Errorless Game Creation by {interaction.user.name} | {interaction.user.id}')
        log.debug(f'> {await get_game_information(name)}')
        await interaction.response.send_message(embed=response_embed)
        return

    @app_commands.command(name="test-key", description="Tests Overseer Game Key")
    @discord.app_commands.describe(key='Tested Key')
    async def overseer_key_test(self, interaction: discord.Interaction, key: str):
        # This is purely a test of the get_all_keys() function for the moment
        KEYS: tuple = await get_all_keys()

        if key in KEYS:
            log.debug(f'> Tested Key: {key} is in use')
            response_embed = discord.Embed(title='Key Use', description='', colour=mc.EMBED_COLORS[f'red'])
            response_embed.add_field(name=f'`{key}` In Use', value='Sadge')
        else:
            log.debug(f'> Tested Key: {key} is not in use')
            response_embed = discord.Embed(title='Key Use?', description='', colour=mc.EMBED_COLORS[f'green'])
            response_embed.add_field(name=f'`{key}` Not In Use', value='Hapy')


        response_embed.set_footer(text=interaction.user.id, icon_url=interaction.user.display_avatar)
        response_embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar)
        await interaction.response.send_message(embed=response_embed)
        return


async def setup(CLIENT):
    await CLIENT.add_cog(OverseerCog(CLIENT))
