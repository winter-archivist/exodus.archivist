import discord
import json

from zenlog import log


class vtb_CharacterManager:
    def __init__(self, interaction: discord.Interaction):
        CHARACTER_NAME_FILE = f'cogs/vtm_toolbox/vtb_characters/{interaction.user.id}/target_character_name.json'

        with open(CHARACTER_NAME_FILE, 'r') as operate_file:
            CHARACTER_NAME_DICT = json.load(operate_file)
        self.OWNER_ID: int = interaction.user.id
        self.CHARACTER_NAME: str = CHARACTER_NAME_DICT['character_name']

    async def __get_owner_id__(self) -> int:
        return self.OWNER_ID
