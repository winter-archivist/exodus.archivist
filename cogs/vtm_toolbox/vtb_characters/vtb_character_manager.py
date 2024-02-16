import os
import json
import discord
import functools
from zenlog import log
from discord.ui import View

from misc.config import mainConfig as mC


async def make_character_file(interaction: discord.Interaction, character_name):
    CHARACTER_FILE: str = f'cogs/vtm_toolbox/vtb_characters/{interaction.user.id}/{character_name}/{character_name}.json'
    CHARACTER_DICT: dict = {'character_name': character_name, 'owner_id': interaction.user.id}

    with open(CHARACTER_FILE, "w") as operate_file:
        json.dump(CHARACTER_DICT, operate_file)


class vtb_DEV_TEST_VIEW(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='TESTING', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.green, row=1)
    async def dev_test_button_one_button_callback(self, interaction, button):

        character_class = vtb_CharacterManager(interaction)

        dev_test_embed = discord.Embed(title='`!__DEV__DEBUG__TESTS__!`',
                                       description='`!__ONLY__PRESS__THINGS__IF__INSTRUCTED__!`',
                                       color=mC.EMBED_COLORS['red'])
        dev_test_embed.add_field(name='Char Name', value=f'{character_class.CHARACTER_NAME}', inline=True)
        dev_test_embed.add_field(name='Char Owner ID', value=f'{character_class.OWNER_ID}', inline=True)
        dev_test_embed.add_field(name='Interactor ID', value=f'{interaction.user.id}', inline=True)

        await interaction.response.send_message(embed=dev_test_embed, view=vtb_DEV_TEST_VIEW(self.CLIENT))


class vtb_CharacterManager:
    def __init__(self, interaction: discord.Interaction):
        CHARACTER_NAME_FILE: str = f'cogs/vtm_toolbox/vtb_characters/{interaction.user.id}/target_character.json'
        with open(CHARACTER_NAME_FILE, 'r') as operate_file:
            CHARACTER_NAME = json.load(operate_file)['character_name']

        self.CHARACTER_NAME: str = CHARACTER_NAME

        CHARACTER_FILE_PATH: str = f'cogs/vtm_toolbox/vtb_characters/{interaction.user.id}/{self.CHARACTER_NAME}/{self.CHARACTER_NAME}.json'

        if not os.path.isfile(CHARACTER_FILE_PATH):
            # This just means the interactor doesn't have any character with the given name.
            raise FileNotFoundError

        with open(CHARACTER_FILE_PATH, 'r') as operate_file:
            CHARACTER_INFO = json.load(operate_file)

        if int(CHARACTER_INFO['owner_id']) == interaction.user.id:
            self.OWNER_ID = interaction.user.id
        else:
            log.error('*> Bad Character Owner')
            raise Exception('*> Bad Character Owner')
