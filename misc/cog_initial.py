from zenlog import log


async def initialCogs(CLIENT):
    log.warn('$ Loading Bootstrap Cogs...')
    await bootstrapCogs(CLIENT)

    log.warn('$ Loading Convenience Cogs...')
    await convenienceCogs(CLIENT)

    log.warn('$ Loading Unstable Cogs...')
    await unstableCogs(CLIENT)

    # ! This is a small script purely for use of myself. Remove it when you're using the bot, it has no effect.
    try:
        await CLIENT.load_extension('cogs.ddtr')
    except Exception as e:
        log.warn(f"<<<{e} | REMOVE THE TRY STATEMENT IN misc/cog_initial.py CONTAINING await CLIENT.load_extension('cogs.ddtr') >>>")
        exit()


async def bootstrapCogs(CLIENT):
    bootstrap_cogs = ('cogManager',)
    forVar = 0
    for x in bootstrap_cogs:
        target = bootstrap_cogs[forVar]
        try:
            await CLIENT.load_extension(f'{target}')
        except Exception as e:
            log.warn(f"<<<$ Failed to load {target} {e}>>>")
            exit()
        forVar = 1


async def convenienceCogs(CLIENT):
    convenience_cogs = ('cogs.vampire.vampireRoll',)
    forVar = 0
    for x in convenience_cogs:
        target = convenience_cogs[forVar]
        try:
            await CLIENT.load_extension(f'{target}')
        except Exception as e:
            log.warn(f"<<<$ Failed to load {target} {e}>>>")
            exit()
        forVar = 1


async def unstableCogs(CLIENT):
    unstable_cogs = ('cogs.exonotes.exoNotes',)
    forVar = 0
    for x in unstable_cogs:
        target = unstable_cogs[forVar]
        try:
            await CLIENT.load_extension(f'{target}')
        except Exception as e:
            log.warn(f"<<<$ Failed to load {target} {e}>>>")
            exit()
        forVar = 1