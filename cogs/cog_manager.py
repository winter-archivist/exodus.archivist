import discord
from discord import app_commands
from discord.ext import commands

from misc.config import main_config as mc


class CogManager(commands.Cog):
    def __init__(self, CLIENT):
        self.CLIENT = CLIENT

    @app_commands.command(name="cog", description="Bot Runner Only")
    @app_commands.choices(target=[
        app_commands.Choice(name="VTM Toolbox", value="vtm_toolbox.vampire_toolbox_cog"),
        app_commands.Choice(name="Overseer", value="overseer.overseer_cog"),
        app_commands.Choice(name="ARCHON", value="archon.archon_cog"),
        app_commands.Choice(name="EA Roller", value="rolletron.rolletron")
    ])
    @app_commands.choices(operation=[
        app_commands.Choice(name="Load", value="load"),
        app_commands.Choice(name="Unload", value="unload"),
        app_commands.Choice(name="Reload", value="reload")
    ])
    async def cog(self, interaction: discord.Interaction, target: app_commands.Choice[str], operation: app_commands.Choice[str]):

        if str(interaction.user) != f'{mc.RUNNER}':
            # Prevents anyone, but the person running the bot, from interacting
            return

        # Makes the base embed
        response_embed = discord.Embed(title='Cog Manager', description='', colour=mc.EMBED_COLORS[f'green'])

        # Adds the basic information to the page
        response_embed.set_footer(text=interaction.user.id, icon_url=interaction.user.display_avatar)
        response_embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar)

        response_embed.add_field(name='', value=f'{operation.value.capitalize()}ed `{target.value}`', inline=True)

        match operation.value:
            case 'load':
                await self.CLIENT.load_extension(f'cogs.{target.value}')

            case 'unload':
                await self.CLIENT.unload_extension(f'cogs.{target.value}')

            case 'reload':
                await self.CLIENT.reload_extension(f'cogs.{target.value}')

        await interaction.response.send_message(embed=response_embed)


async def setup(CLIENT):
    await CLIENT.add_cog(CogManager(CLIENT))
