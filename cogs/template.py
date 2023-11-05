from discord.ext import commands
from discord import app_commands
import discord

from zenlog import log


class TEMPLATE(commands.Cog):
    def __init__(self, CLIENT):
        self.CLIENT = CLIENT

    @app_commands.command(name="TEMPLATE", description="TEMPLATE COMMAND")
    @app_commands.describe(templateinput='TEMPLATE Display Text')
    async def TEMPLATE(self, interaction: discord.Interaction, templateinput: str):
        await interaction.response.send_message(f'TEMPLATE; {templateinput}')


async def setup(CLIENT):
    await CLIENT.add_cog(TEMPLATE(CLIENT))
    log.info('> Template Loaded')
