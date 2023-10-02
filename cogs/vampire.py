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
        if not isinstance(ctx.channel, discord.channel.DMChannel): await ctx.channel.purge(limit=1)

        if targetUser is None: targetUser = ctx.author
        # Unless specified, targetUser is just whoever sent the command
        """
        ALL CODE THAT RUNS UNDER THIS NEEDS TO USE THE targetUser NOT THE ctx.author
        DOING THIS ALLOWS ME TO ALTER THINGS AS IF FROM ANOTHER PLAYER'S ACCOUNT
        """
        parsingInfo = (targetUser, ctx, adminPanelPassphrase, self)
        # Used by all the views below, stays the same so no need to repeat
        # Do not change this, everything will break :)

        if view == 'chargen':  # Local Logic
            await ctx.send(embed=v.gen.chargen_embed, view=v.gen.CharGenView(self.CLIENT))  # CharGen View

        elif view == 'homebrew':  # Local Logic
            await ctx.send(embed=v.hbr.homebrew_embed, view=v.hbr.HomebrewView(self.CLIENT))  # Homebrew View

        elif view == 'cobweb':
            await vtmMenuHandler(parsingInfo, v.web.cobwebInfo)

        elif view == 'mark':
            await vtmMenuHandler(parsingInfo, v.mrk.markInfo)

        elif view == 'nomad':  # Very Heavily a Maybe? Basically Random Encounters for the RV
            await vtmMenuHandler(parsingInfo, v.nmd.nomadInfo)

        elif view == 'rat':  # Very Heavily a Maybe? Basically Random Encounters/Info Gathering for Nosferatu
            await vtmMenuHandler(parsingInfo, v.rat.ratInfo)


async def setup(CLIENT):
    await CLIENT.add_cog(Vampire(CLIENT))
    log.info('> Vampire Loaded')


async def teardown():
    log.critical('> Vampire Unloaded')
