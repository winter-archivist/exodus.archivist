import discord
from discord.ext import commands
from discord.ui import View

from zenlog import log

from misc import ashen_utils as au

cog_manager_embed = discord.Embed(title='Cog Manager', description='', color=0x8A2BE2)
non_admin_embed = discord.Embed(title='Requirements Unmet',
                                description='You\'re not an administrator of this bot.', color=0xFF0000)
yaml_error_embed = discord.Embed(title='Cog Manager Error', color=0xFF0000)


async def CacheData_ExistCheck(*, checkFor, interaction):
    does_exist = await au.cacheHandler(primaryRunType='-e', targetCache='cogs/shared/cache/cogManager.yaml', searchFor=checkFor)
    if bool(does_exist) is True:
        await au.embedHandler(primaryRunType='-r', secondaryRunType='--cm', interaction=interaction, handled_embeds=cog_manager_embed)
        await au.cacheHandler(secondaryRunType='--c', targetCache='cogs/shared/cache/cogManager.yaml')
        yaml_error_embed.set_field_at(index=0, name='Issue:', value=f'targetCog Already Provided', inline=False)
        await interaction.followup.send(embed=yaml_error_embed, ephemeral=True)
        return True


class ExodusView(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.select(
        placeholder='Select targetCog',
        options=[
            discord.SelectOption(
                label='Template', value='cogs.template',
                emoji='<a:pydis_pridespin:1113716405192376351>',
            ),
            discord.SelectOption(
                label='Orokast Rolls', value='cogs.orokast_rolls',
                emoji='<:pixels_snek_2:847766933084045332>',
            ),
            discord.SelectOption(
                label='General Rolls', value='cogs.general_rolls',
                emoji='<:gorbbrain:725954288005677056>',
            )],
        row=0)
    async def targetCog_select_callback(self, interaction, select: discord.ui.Select):
        if str(interaction.user) != '.ashywinter':
            await interaction.response.send_message(embed=non_admin_embed, ephemeral=True)
            return

        if await CacheData_ExistCheck(checkFor='targetCog', interaction=interaction) is True:
            return

        await au.cacheHandler(primaryRunType='-w', targetCache='cogs/shared/cache/cogManager.yaml', dataInput={'targetCog': f'{select.values[0]}'})
        cog_manager_embed.set_field_at(index=0, name='targetCog:', value=f'{select.values[0]}', inline=False)
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
            await interaction.response.send_message(embed=non_admin_embed, ephemeral=True)
            return

        if await CacheData_ExistCheck(checkFor='operationType', interaction=interaction) is True:
            return

        await au.cacheHandler(primaryRunType='-w', targetCache='cogs/shared/cache/cogManager.yaml', dataInput={'operationType': f'{select.values[0]}'})

        cog_manager_embed.set_field_at(index=1, name='operationType:', value=f'{select.values[0]}', inline=False)
        await interaction.response.edit_message(embed=cog_manager_embed)

    @discord.ui.button(label='Run', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.green)
    async def run_button_callback(self, interaction, button):
        if str(interaction.user) != '.ashywinter':
            await interaction.response.send_message(embed=non_admin_embed, ephemeral=True)
            return

        data = await au.cacheHandler(primaryRunType='-r', targetCache='cogs/shared/cache/cogManager.yaml')
        use_data = {}; use_data.update(data)
        target_cog = use_data['targetCog']; operation_type = use_data['operationType']

        if operation_type == 'load':
            await self.CLIENT.load_extension(f'{target_cog}')

        elif operation_type == 'unload':
            await self.CLIENT.unload_extension(f'{target_cog}')

        elif operation_type == 'reload':
            await self.CLIENT.reload_extension(f'{target_cog}')

        await au.embedHandler(primaryRunType='-r', secondaryRunType='--cm', interaction=interaction, handled_embeds=cog_manager_embed)
        await au.cacheHandler(secondaryRunType='--c', targetCache='cogs/shared/cache/cogManager.yaml')
        cog_manager_embed.set_field_at(index=2, name='Run:', value=f'{operation_type} -> {target_cog}', inline=False)

    @discord.ui.button(label='Clear', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.red)
    async def clear_button_callback(self, interaction, button):
        if str(interaction.user) != '.ashywinter':
            await interaction.response.send_message(embed=non_admin_embed, ephemeral=True)
            return

        await au.embedHandler(primaryRunType='-r', secondaryRunType='--cm', interaction=interaction, handled_embeds=cog_manager_embed)
        await au.cacheHandler(secondaryRunType='--c', targetCache='cogs/shared/cache/cogManager.yaml')


class cog_manager(commands.Cog):
    def __init__(self, CLIENT):
        self.CLIENT = CLIENT

    @commands.command(hidden=True)
    async def _cog(self, ctx):

        if not isinstance(ctx.channel, discord.channel.DMChannel):
            await ctx.channel.purge(limit=1)

        if str(ctx.author) == '.ashywinter':
            await au.cacheHandler(secondaryRunType='--c', targetCache='cogs/shared/cache/cogManager.yaml')
            await ctx.author.send(embed=cog_manager_embed, view=ExodusView(self.CLIENT))

    @commands.command(hidden=True)
    async def cog(self, ctx):

        if not isinstance(ctx.channel, discord.channel.DMChannel):
            await ctx.channel.purge(limit=1)

        if str(ctx.author) == '.ashywinter':
            await au.cacheHandler(secondaryRunType='--c', targetCache='cogs/shared/cache/cogManager.yaml')
            await ctx.send(embed=cog_manager_embed, view=ExodusView(self.CLIENT))


async def setup(CLIENT):
    await au.embedHandler(primaryRunType='-$', secondaryRunType='--cm', handled_embeds=(cog_manager_embed, yaml_error_embed))
    # await embedHandler(runType='-s')
    await au.cacheHandler(secondaryRunType='--c', targetCache='cogs/shared/cache/cogManager.yaml')
    await CLIENT.add_cog(cog_manager(CLIENT))
    log.info('> Cog Manager Loaded')


async def teardown():
    log.critical('> Cog Manager Unloaded | _FIND OUT WHY HOLY SHIT_')
