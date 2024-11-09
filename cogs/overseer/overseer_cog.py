import discord
from discord import app_commands
from discord.ext import commands
from zenlog import log

import json
import datetime
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

    return_var: dict = \
        {
            'details':
                {
                    'Name': f'{NAME}',
                    'System': f'{SYSTEM}',
                    'Key': f'{KEY}',
                    'Max Players': f'{MAX_PLAYERS}'},
            'players':
                PLAYERS
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

    for x in GAMES:
        game_path = f'cogs/overseer/games/{x}'

        with open(f'{game_path}/details.json', 'r') as operate_file:
            details: dict = json.load(operate_file)
        return_var.append(details['Key'])

    return tuple(return_var)


async def key_gen(LENGTH: int) -> str:
    # Returns random LENGTH character long string that contains ascii upper/lower case, digits, and punctuation.
    # If the generated key is found to be in use, it will repeatedly regenerate until the key is new.
    new_key = ''.join(SystemRandom().choice(ascii_uppercase + ascii_lowercase + digits) for _ in range(LENGTH))
    USED_KEYS: tuple = await get_all_keys()

    while new_key in USED_KEYS:
        new_key = ''.join(SystemRandom().choice(ascii_uppercase) for _ in range(LENGTH))

    log.debug(f'> Newly Generated Key: `{new_key}`')

    return new_key


async def generate_archive(interaction: discord.Interaction):
    archive_content: dict = {'ArchiveCreationDateTime': str(datetime.datetime.now()),
                             'ArchiveGenerator'       : f'{interaction.user.id}'}
    GAME_INFORMATION: tuple = await get_all_games_information()

    for_var: int = 0
    for x in GAME_INFORMATION:
        archive_content.update({GAME_INFORMATION[for_var]['details']['Name']: GAME_INFORMATION[for_var]['details']})
        archive_content.update({GAME_INFORMATION[for_var]['details']['Name']: GAME_INFORMATION[for_var]['players']})
        for_var += 1

    with open(f'cogs/overseer/archive/game_archive.json', 'w') as operate_file:
        json.dump(archive_content, operate_file)
    log.debug(f'> Generated Archive | {interaction.user.name} | {interaction.user.id}')


class OverseerCog(commands.Cog):
    def __init__(self, CLIENT):
        self.CLIENT = CLIENT

    # Needs Manage, View, Leave

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
        NOT_ALLOWED_CHARACTERS: tuple = ('<', '>', ':', '\\', '/', '|', '?', '*', '\'')
        for x in NOT_ALLOWED_CHARACTERS:

            if name.__contains__(str(x)):
                response_embed = discord.Embed(title='Create Game', description='', colour=mc.EMBED_COLORS[f'red'])
                response_embed.set_footer(text=interaction.user.id, icon_url=interaction.user.display_avatar)
                response_embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar)
                response_embed.add_field(name='Failed Creation', value=f'**Invalid Character:** `{NOT_ALLOWED_CHARACTERS[x]}` in **Name:** `{name}`', inline=False)
                response_embed.add_field(name='All Invalid Characters', value=f'{" ".join(NOT_ALLOWED_CHARACTERS)}', inline=False)
                await interaction.response.send_message(embed=response_embed)
                return

            if system.__contains__(str(x)):
                response_embed = discord.Embed(title='Create Game', description='', colour=mc.EMBED_COLORS[f'red'])
                response_embed.set_footer(text=interaction.user.id, icon_url=interaction.user.display_avatar)
                response_embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar)
                response_embed.add_field(name='Failed Creation', value=f'**Invalid Character:** `{NOT_ALLOWED_CHARACTERS[x]}` in **System:** `{system}`', inline=False)
                response_embed.add_field(name='All Invalid Characters', value=f'{" ".join(NOT_ALLOWED_CHARACTERS)}', inline=False)
                await interaction.response.send_message(embed=response_embed)
                return

        GAME_DIRECTORY: str = f'cogs/overseer/games/{name}'

        if max_players is None:
            max_players: int = 100
        if int(max_players) > 100:
            max_players = 100
        max_players: int = int(max_players)  # I just want to make absolutely certain it is an int

        key: str = await key_gen(10)

        try:
            # If something fails later, remove the directory that is made and any included files
            mkdir(GAME_DIRECTORY)
            log.debug(f'> Made dir {GAME_DIRECTORY} | {interaction.user.name} | {interaction.user.id}')

        except Exception as e:
            log.crit(f'*> {interaction.user.name} | {interaction.user.id} failed at making new game directory.')
            log.crit(f'*> Game Details: {name} {system}')
            log.crit(f'*> Make Error: {e}')
            page: discord.Embed = discord.Embed(title='Overseer-Game-Create', description='Failed Creation', colour=mc.EMBED_COLORS[f"red"])
            page.add_field(name='Encountered Error', value=f'{e}', inline=False)
            return

        try:
            GAME_FILES: tuple = ('details', 'players', 'placeholder')
            FILE_CONTENTS: tuple = (
                # Details File
                {'Name': f'{name}', 'System': f'{system}', 'Max Players': int(max_players), 'Key': f'{key}'},

                # Players File
                {f'{interaction.user.id}': {'Username'    : f'{interaction.user.name}',
                                            'Public Tags' : ('Creator', 'Game Master', 'Overseer'),
                                            'Private Tags': ('',)
                                            }
                 },

                # This placeholder is never read to, or written, feel free to delete it,
                # it's just here to make it clearer where to add additional files
                {'placeholder': 'placeholder'})

            for_var: int = 0
            for x in GAME_FILES:
                with open(f'{GAME_DIRECTORY}/{GAME_FILES[for_var]}.json', 'w') as operate_file:
                    json.dump(FILE_CONTENTS[for_var], operate_file)
                log.debug(f'> Made Game {GAME_FILES[for_var]} | {interaction.user.name} | {interaction.user.id}')
                for_var += 1

        except Exception as e:
            log.crit(f'*> {interaction.user.name} | {interaction.user.id} failed at making new game files.')
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

        await generate_archive(interaction)

        log.crit(f'> Errorless Game Creation by {interaction.user.name} | {interaction.user.id}')
        log.debug(f'> {await get_game_information(name)}')
        await interaction.response.send_message(embed=response_embed)
        return

    @app_commands.command(name="join-game", description="Joins Overseer Game by Key")
    @discord.app_commands.describe(key='Game Key')
    async def overseer_join_game(self, interaction: discord.Interaction, key: str):

        # ! TO BE REMOVED
        if str(interaction.user) != f'{mc.RUNNER}':
            # Prevents anyone, but the person running the bot, from interacting
            return
        # ! TO BE REMOVED

        KEYS: tuple = await get_all_keys()
        if key not in KEYS:  # If a key isn't in use, it can't be used to join a game, obviously.
            response_embed = discord.Embed(title='Invalid Key Provided', description='', colour=mc.EMBED_COLORS[f'red'])
            response_embed.set_footer(text=interaction.user.id, icon_url=interaction.user.display_avatar)
            response_embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar)
            await interaction.response.send_message(embed=response_embed)
            return

        GAMES: tuple = await get_games()
        for games in GAMES:
            # Checks all Games until it finds a matching key, once it does, it exits the for loop
            # This is used to find what game the player is wanting to join based on just the key
            game_path: str = f'cogs/overseer/games/{games}'

            with open(f'{game_path}/details.json', 'r') as operate_file:
                details: dict = json.load(operate_file)

            if details['Key'] == key:
                break

        with open(f'{game_path}/players.json', 'r') as operate_file:
            players: dict = json.load(operate_file)

        if str(interaction.user.id) in players:
            response_embed = discord.Embed(title='Already In Game', description='', colour=mc.EMBED_COLORS[f'red'])
            response_embed.set_footer(text=interaction.user.id, icon_url=interaction.user.display_avatar)
            response_embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar)
            await interaction.response.send_message(embed=response_embed)
            return

        try:
            PLAYER_FILE: dict = \
                {
                    f'{interaction.user.id}':
                        {
                            'Username'    : f'{interaction.user.name}',
                            'Public Tags' : ('Player',),
                            'Private Tags': ('Joined Via Key',)
                        }
                }

            players.update(PLAYER_FILE)
            with open(f'{game_path}/players.json', 'w') as operate_file:
                json.dump(players, operate_file)

            log.debug(f'> {interaction.user.name}/{interaction.user.id} Joined {games} with {key}')

        except Exception as e:
            log.crit(f'*> {interaction.user.name} | {interaction.user.id} failed at joining game with correct key.')
            page: discord.Embed = discord.Embed(title='Overseer-Game-Join', description='Failed Join', colour=mc.EMBED_COLORS[f"red"])
            page.add_field(name='Encountered Error', value=f'{e}', inline=False)
            return

        await generate_archive(interaction)

        response_embed = discord.Embed(title='Joined Game Successfully', description='', colour=mc.EMBED_COLORS[f'green'])
        response_embed.add_field(name=f'Joined {games} Via Key!', value='')
        response_embed.set_footer(text=interaction.user.id, icon_url=interaction.user.display_avatar)
        response_embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar)
        await interaction.response.send_message(embed=response_embed)
        return

    @app_commands.command(name="view-game", description="Views Overseer Game by Key or Game")
    @discord.app_commands.describe(key='Game Key')
    async def overseer_view_game(self, interaction: discord.Interaction, key: str):

        # ! TO BE REMOVED
        if str(interaction.user) != f'{mc.RUNNER}':
            # Prevents anyone, but the person running the bot, from interacting
            return
        # ! TO BE REMOVED

        # pa

    @app_commands.command(name="generate-game-archive", description="gga")
    async def generate_game_archive(self, interaction: discord.Interaction):

        if str(interaction.user.id) != f'{mc.RUNNER}':
            # Prevents anyone, but the person running the bot, from interacting
            return

        await generate_archive(interaction)
        

async def setup(CLIENT):
    await CLIENT.add_cog(OverseerCog(CLIENT))
