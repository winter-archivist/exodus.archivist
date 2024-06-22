import discord
from discord import app_commands
from discord.ext import commands
from zenlog import log

import json
from random import SystemRandom
from string import ascii_uppercase, digits
from os import mkdir, path

from misc.config import main_config as mc


class OverseerCog(commands.Cog):
    def __init__(self, CLIENT):
        self.CLIENT = CLIENT

    # Needs Manage, View, Join, Leave

    # This is a very temp setup, please ignore
    @app_commands.command(name="create-game", description="Creates Overseer Game")
    @discord.app_commands.describe(name='Name of The Game [!Unmodifiable!]',
                                   system='System being used for The Game.',
                                   key='Used to join The Game.')
    async def overseer_create_game(self, interaction: discord.Interaction, name: str, system: str, key: str = None):

        GAME_DIRECTORY: str = f'cogs/overseer/games/{name}'

        try:
            mkdir(GAME_DIRECTORY)

            if key is None:
                key: str = ''.join(SystemRandom().choice(ascii_uppercase + digits) for _ in range(10))

            GAME_FILES: tuple = ('details', 'players', 'placeholder')
            FILE_CONTENTS: tuple = (
                {'Name' : f'{name}', 'System' : f'{system}', 'Key' : f'{key}'},

                {f'{interaction.user.id}' : {'Username' : f'{interaction.user.name}', 'Permissions' : f'Game Master'}},

                {'placeholder' : 'placeholder'})

            for_var: int = 0
            for x in GAME_FILES:
                with open(f'{GAME_DIRECTORY}/{GAME_FILES[for_var]}.json', 'w') as operate_file:
                    json.dump(FILE_CONTENTS[for_var], operate_file)
                for_var += 1

        except Exception as e:
            log.crit(f'*> {interaction.user.name} | {interaction.user.id} failed at making new game.')
            log.crit(f'*> Game Details: {name} {system} {key}')
            log.crit(f'*> Make Error: {e}')
            page: discord.Embed = discord.Embed(title='Overseer-Game-Create', description='Failed Creation', colour=mc.EMBED_COLORS[f"red"])
            page.add_field(name='Encountered Error', value=f'{e}', inline=False)
            return

        # Makes the base embed
        response_embed = discord.Embed(title='Create Game', description='', colour=mc.EMBED_COLORS[f'green'])

        # Adds the basic information to the page
        response_embed.set_footer(text=interaction.user.id, icon_url=interaction.user.display_avatar)
        response_embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar)

        response_embed.add_field(name=f'Created {name}', value=f'{system}', inline=False)
        response_embed.add_field(name='Game Key', value='[Check DMs]', inline=False)

        await interaction.response.send_message(embed=response_embed)


async def setup(CLIENT):
    await CLIENT.add_cog(OverseerCog(CLIENT))
