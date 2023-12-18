import discord


async def interactionExpirationChecker(interaction: discord.Interaction):
    if interaction.is_expired() is True:
        await interaction.response.send_message(content='> This Command has Expired', ephemeral=True)
        return
    elif interaction.is_expired() is False:
        pass
