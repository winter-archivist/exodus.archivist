import discord
from discord.ext import commands

from zenlog import log

from misc import ashen_utils as au
from cogs.shared.config import vampire as v


async def vtmMenuHandler(parsingInfo, veInfo):
    targetUser, ctx, adminPanelPassphrase, self = parsingInfo
    adminEmbed, standardEmbed, deniedEmbed = veInfo[1]
    adminView, standardView = veInfo[2]

    if await au.roleCheck(targetUser, ctx, '.TheStoryTeller') and adminPanelPassphrase == 'Bypass':
        await ctx.send(embed=adminEmbed, view=adminView(self.CLIENT))

    elif await au.roleCheck(targetUser, ctx, f'{veInfo[1]}') or await au.roleCheck(targetUser, ctx, '.TheStoryTeller'):
        await ctx.send(embed=standardEmbed, view=standardView(self.CLIENT))

    else:
        await ctx.send(embed=deniedEmbed)


class Vampire(commands.Cog):
    def __init__(self, CLIENT):
        self.CLIENT = CLIENT

    @commands.command()
    @commands.has_role(".Kindred")
    async def vtm(self, ctx, view, adminPanelPassphrase: str = None, targetUser: discord.Member = None):
        """{view}"""
        if not isinstance(ctx.channel, discord.channel.DMChannel): await ctx.channel.purge(limit=1)

        if targetUser is None: targetUser = ctx.author
        # Unless specified, targetUser is just whoever sent the command
        """
        ALL CODE THAT RUNS UNDER THIS 
        -> --> NEEDS <-- <-
        TO USE targetUser NOT ctx.author
        
        DOING THIS ALLOWS ME TO INTERACT WITH MENUS
        AS IF FROM ANOTHER PLAYER'S ACCOUNT
        """
        parsingInfo = (targetUser, ctx, adminPanelPassphrase, self)
        # Used by all the views below, stays the same so no need to repeat
        # Do not change this, everything will break :)

        match view:
            # Don't use vtmMenuHandler :: Handle _ALL_ Logic Locally or in ve file
            case 'chargen':
                await ctx.send(embed=v.gen.chargen_embed, view=v.gen.CharGenView(self.CLIENT))  # CharGen View
            case 'homebrew':
                await ctx.send(embed=v.hbr.homebrew_embed, view=v.hbr.HomebrewView(self.CLIENT))  # Homebrew View
            case 'roll':
                await ctx.send(embed=v.rll.roll_embed, view=v.rll.RollView(self.CLIENT))  # Rolling View

            # Uses vtmMenuHandler :: Logic should all be handled at declaration
            case 'cobweb':
                await vtmMenuHandler(parsingInfo, v.web.cobwebInfo)
            case 'mark':
                await vtmMenuHandler(parsingInfo, v.mrk.markInfo)
            case 'nomad':
                await vtmMenuHandler(parsingInfo, v.nmd.nomadInfo)
            case 'rat':
                await vtmMenuHandler(parsingInfo, v.rat.ratInfo)

            case _:  # Local Logic :: Handle Logic Locally
                await ctx.send(embed=v.nov.no_view_embed)


async def setup(CLIENT):
    await au.embedHandler(primaryRunType='-$', secondaryRunType='--vr', handled_embeds=None)
    await CLIENT.add_cog(Vampire(CLIENT))
    log.info('> Vampire Loaded')


async def teardown():
    log.critical('> Vampire Unloaded')
