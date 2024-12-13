import os

# ! Essential for Client to run.
# ! ALL variables must be set, for safety, never modify these while the bot is running

# ? Find this on your discord developer portal
# This tries to grab the token from your environment
# You can manually enter your Token here, but leave your bot open to hijacking if you ever share this file/the token
# Or you can just be smart about it, and just use an environment.
TOKEN: str = f'{os.environ["TOKEN"]}'

# ? Prefix for all NON-SLASH Commands.
PREFIX: str = f'ex.'

# ? List of cogs that will be loaded on startup
# To add cogs, just add their directory, but instead of "/" use ".", however do not include their file extension.
# I do not recommend removing the cog_manager
INITIALIZATION_COGS: tuple = ('cogs.cog_manager', 'cogs.vtm_toolbox.vampire_toolbox_cog', 'cogs.rolletron.rolletron_cog')

# ? Determines whether the bot will attempt loading its slash-commands.
# Should be kept off, however can be enabled if needed.
SLASH_MODE: bool = False
