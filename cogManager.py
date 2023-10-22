import discord
from discord.ext import commands
from discord.ui import View
from zenlog import log

cog_manager_embed = discord.Embed(title='Cog Manager', color=0x8A2BE2)
cog_manager_embed.add_field(name='targetCog:', value=f'N/A', inline=True)
cog_manager_embed.add_field(name='operationType:', value=f'N/A', inline=True)
cog_manager_embed.add_field(name='CMD:', value=f'N/A', inline=False)

run_command = \
    {"operation": 'tc.Ungiven1',
     "target": 'Ungiven2'}


class ExodusView(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.select(
        placeholder='Select targetCog',
        options=[
            discord.SelectOption(
                label='Template', value='template',
                emoji='<a:pydis_pridespin:1113716405192376351>',
            ),
            discord.SelectOption(
                label='Vampire', value='cogs.vampire.vampireRoll',
                emoji='<:bloodT:555804549173084160>',
            )],
        row=0)
    async def targetCog_select_callback(self, interaction, select: discord.ui.Select):
        if str(interaction.user) != '.ashywinter':
            return

        global run_command
        run_command["target"] = f'{select.values[0]}'

        cog_manager_embed.set_field_at(index=0, name='targetCog:', value=f'{run_command["target"]}', inline=True)
        await interaction.response.edit_message(embed=cog_manager_embed)

    @discord.ui.select(
        placeholder='Select operationType',
        options=[
            discord.SelectOption(
                label='Load', value='load', emoji='<:knightyes:722660226716926016>', ),
            discord.SelectOption(
                label='Unload', value='unload', emoji='<:knightno:722660227144482856>', ),
            discord.SelectOption(
                label='Reload', value='reload', emoji='<:nbthinblood:982240285243351080>', )],
        row=1)
    async def operationType_select_callback(self, interaction, select: discord.ui.Select):
        if str(interaction.user) != '.ashywinter':
            return

        global run_command
        run_command["operation"] = f'{select.values[0]}'

        cog_manager_embed.set_field_at(index=1, name='operationType:', value=f'{run_command["operation"]}', inline=True)
        await interaction.response.edit_message(embed=cog_manager_embed)

    @discord.ui.button(label='Run', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.green)
    async def run_button_callback(self, interaction, button):
        if str(interaction.user) != '.ashywinter':
            return

        global run_command
        cmd_operation = run_command["operation"]
        cmd_target = run_command["target"]

        match cmd_operation:
            case 'load':
                await self.CLIENT.load_extension(f'cogs.{cmd_target}')

            case 'unload':
                await self.CLIENT.unload_extension(f'cogs.{cmd_target}')

            case 'unload':
                await self.CLIENT.reload_extension(f'cogs.{cmd_target}')

        cog_manager_embed.set_field_at(index=0, name='targetCog:', value=f'N/A', inline=True)
        cog_manager_embed.set_field_at(index=1, name='operationType:', value=f'N/A', inline=True)
        cog_manager_embed.set_field_at(index=2, name='CMD:', value=f'{cmd_operation} -> {cmd_target}', inline=False)
        run_command["operation"] = 'Ungiven1'
        run_command["target"] = 'Ungiven2'
        await interaction.response.edit_message(embed=cog_manager_embed)


class cog_manager(commands.Cog):
    def __init__(self, CLIENT):
        self.CLIENT = CLIENT

    @commands.command(hidden=True)
    async def cog(self, ctx):
        if not isinstance(ctx.channel, discord.channel.DMChannel):
            await ctx.channel.purge(limit=1)

        if str(ctx.author) != '.ashywinter':
            return

        await ctx.send(embed=cog_manager_embed, view=ExodusView(self.CLIENT))


async def setup(CLIENT):
    await CLIENT.add_cog(cog_manager(CLIENT))
    log.info('$> Cog Manager Loaded')
