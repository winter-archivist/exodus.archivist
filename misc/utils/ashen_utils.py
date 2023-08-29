from zenlog import log
import yaml


async def cacheHandler(*, primaryRunType=None, secondaryRunType=None, targetCache=None, dataInput=None, searchFor=None):
    if primaryRunType == '-r':  # Read data from cache

        if targetCache is None:
            log.critical('*> No `targetCache` passed into `cacheHandler` for `-r` runType')
            return

        with open(f'{targetCache}', 'r') as file:
            data = yaml.safe_load(file)
        return data

    elif primaryRunType == '-w' and isinstance(dataInput, dict):
        if targetCache is None:
            log.critical('*> No `targetCache` passed into `cacheHandler` for `-w` runType')
            return
        if dataInput is None:
            log.critical('*> No `dataInput` passed into `cacheHandler` for `-w` runType')
            return

        with open(f'{targetCache}', 'a' if dataInput else 'w') as file:
            yaml.dump(dataInput, file)

    elif primaryRunType == '-e':  # simple exist check
        if targetCache is None:
            log.critical('*> No `targetCache` passed into `cacheHandler` for `-e` runType')
            return

        with open(f'{targetCache}', 'r') as file:
            data = yaml.safe_load(file)
        if data is None:  # Checks if Data even Exists, this prevents error caused by checking for something in nothing
            return None
        elif searchFor in data:
            return True
        else:
            return False

    if secondaryRunType == '--c':  # Clears the target YAML file
        if targetCache is None:
            log.critical('*> No `fileName` passed into `cacheHandler` for `-c` runType')
            return
        with open(f'{targetCache}', 'w') as file:
            pass


async def embedHandler(*, primaryRunType, secondaryRunType=None, interaction=None, handled_embeds):

    if primaryRunType == '-$':  # Embed Initial Set

        if secondaryRunType == '--cm':  # Cog Manager
            cog_manager_embed = handled_embeds[0]
            yaml_error_embed = handled_embeds[1]
            cog_manager_embed.add_field(name='targetCog:', value=f'N/A', inline=False)
            cog_manager_embed.add_field(name='operationType:', value=f'N/A', inline=False)
            cog_manager_embed.add_field(name='Run: ', value=f'N/A', inline=False)
            yaml_error_embed.add_field(name='Issue:',
                                       value=f'OH SHIT STUFF FUCKED UP; PLEASE CONTACT `.ashywinter` ON DISCORD',
                                       inline=False)
            yaml_error_embed.add_field(name='Solution:', value=f'Cache Cleared', inline=False)
            log.info('> Embeds Set for CogManager...')

    elif primaryRunType == '-r':  # Resets an embed

        if interaction is None:  # Logs Error & returns
            log.critical('*> No `interaction` passed into `embedHandler` for `-r` primaryRunType')
            return

        if handled_embeds is None:
            log.critical('*> No `handled_embeds` passed into `embedHandler` for `-r` primaryRunType')
            return

        if secondaryRunType == '--cm':  # Cog Manager
            cog_manager_embed = handled_embeds

            cog_manager_embed.set_field_at(index=0, name='targetCog:', value=f'N/A', inline=False)
            cog_manager_embed.set_field_at(index=1, name='operationType:', value=f'N/A', inline=False)
            await interaction.response.edit_message(embed=cog_manager_embed)

    elif primaryRunType == '-u':  # updates selection with specification

        if interaction is None:  # Logs Error & returns
            log.critical('*> No `interaction` passed into `embedHandler` for `-u` runType')
            return

        # do real shit
        pass
