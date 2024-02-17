import discord
from discord import app_commands
from discord.ext import commands

from misc.config import main_config as mC


class CogManager(commands.Cog):
    def __init__(self, CLIENT):
        self.CLIENT = CLIENT

    @app_commands.command(name="cog", description="CogManager")
    @app_commands.choices(target=[
        app_commands.Choice(name="VTM Toolbox", value="vtm_toolbox.vampireToolboxCog")])
    @app_commands.choices(operation=[
        app_commands.Choice(name="Load", value="load"),
        app_commands.Choice(name="Unload", value="unload"),
        app_commands.Choice(name="Reload", value="reload")])
    async def cog(self, interaction: discord.Interaction, target: app_commands.Choice[str], operation: app_commands.Choice[str]):

        if str(interaction.user) != f'{mC.RUNNER}':
            # Prevents anyone, but the person running the bot, from interacting
            return

        # Makes the base embed
        base_page = discord.Embed(title='Cog Manager', description='', colour=mC.EMBED_COLORS[f'purple'])

        # Assigns basic user information
        user_info = {'user_name'  : interaction.user,
                     'user_id'    : interaction.user.id,
                     'user_avatar': interaction.user.display_avatar}

        # Adds the basic information to the page
        base_page.set_footer(text=f'{user_info["user_id"]}', icon_url=f'{user_info["user_avatar"]}')
        base_page.set_author(name=f'{user_info["user_name"]}', icon_url=f'{user_info["user_avatar"]}')

        base_page.add_field(name='Target:', value=f'{target.value}', inline=True)
        base_page.add_field(name='Operation:', value=f'{operation.value}', inline=True)
        base_page.add_field(name='Command:', value=f'{operation.value}({target.value})', inline=False)

        match operation.value:
            case 'load':
                await self.CLIENT.load_extension(f'cogs.{target.value}')

            case 'unload':
                await self.CLIENT.unload_extension(f'cogs.{target.value}')

            case 'unload':
                await self.CLIENT.reload_extension(f'cogs.{target.value}')

        await interaction.response.send_message(embed=base_page)


async def setup(CLIENT):
    await CLIENT.add_cog(CogManager(CLIENT))
