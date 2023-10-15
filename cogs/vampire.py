import discord
from discord.ext import commands

from zenlog import log

from misc import ashen_utils as au
from cogs.shared.config import vampire as v
import sqlite3


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
        # Used by all vtmMenuHandler views
        # Do not change this, they will all fucking shatter :)

        match view:
            # Don't use vtmMenuHandler :: Determining Logic is Handled Here. Use veV file for View Logic
            case 'homebrew':
                await ctx.send(embed=v.hbr.homebrew_embed, view=v.hbr.HomebrewView(self.CLIENT))  # Homebrew View
            case 'roll':
                await ctx.send(embed=v.rll.roll_embed, view=v.rll.RollView(self.CLIENT))  # Rolling View

            # Uses vtmMenuHandler :: Determining Logic is at vtmMenuHandler. Use veV file for View Logic
            case 'cobweb':
                await vtmMenuHandler(parsingInfo, v.web.cobwebInfo)
            case 'mark':
                await vtmMenuHandler(parsingInfo, v.mrk.markInfo)
            case 'nomad':
                await vtmMenuHandler(parsingInfo, v.nmd.nomadInfo)
            case 'rat':
                await vtmMenuHandler(parsingInfo, v.rat.ratInfo)

            case _:  # No Logic
                await ctx.send(embed=v.nov.no_view_embed)

    @commands.command()
    async def make(self, ctx):
        if not isinstance(ctx.channel, discord.channel.DMChannel): await ctx.channel.purge(limit=1)
        if str(ctx.author) != '.ashywinter':
            await ctx.send('No. uwu')
            return
        db = sqlite3.connect(f'{au.vePCDBLocation}apollyon.sqlite')
        cursor = db.cursor()
        # Blank Vampire database Maker
        cursor.execute('CREATE TABLE IF NOT EXISTS ownerid(id TEXT)')
        cursor.execute('CREATE TABLE IF NOT EXISTS physicalStats(strength INTEGER, dexterity INTEGER, stamina INTEGER)')
        cursor.execute('CREATE TABLE IF NOT EXISTS socialStats(charisma INTEGER, manipulation INTEGER, composure INTEGER)')
        cursor.execute('CREATE TABLE IF NOT EXISTS mentalStats(intelligence INTEGER, wits INTEGER, resolve INTEGER)')
        cursor.execute('CREATE TABLE IF NOT EXISTS hunger(hungerCount INTEGER)')

        # Basic Value Input into Blank Vampire DB
        cursor.execute('INSERT INTO physicalStats (strength, dexterity, stamina) VALUES(1,2,3)')
        cursor.execute('INSERT INTO socialStats (charisma, manipulation, composure) VALUES(3,4,5)')
        cursor.execute('INSERT INTO mentalStats (intelligence, wits, resolve) VALUES(6,7,8)')
        cursor.execute('INSERT INTO hunger (hungerCount) VALUES(1)')
        db.commit()
        db.close()


async def setup(CLIENT):
    await au.embedHandler(primaryRunType='-$', secondaryRunType='--vr', handled_embeds=None)
    await CLIENT.add_cog(Vampire(CLIENT))
    log.info('> Vampire Loaded')


async def teardown():
    log.critical('> Vampire Unloaded')
