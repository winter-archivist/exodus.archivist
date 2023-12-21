from misc.config import mainConfig as mc
from discord import Embed

selection_embed = Embed(title='', description=f'', color=mc.embed_colors["purple"])
selection_embed.add_field(name='Character Name', value=f'', inline=False)
selection_embed.add_field(name='Roll Information', value='', inline=False)
selection_embed.add_field(name='Roll Pool:', value=f'')
selection_embed.add_field(name='Difficulty:', value=f'')
selection_embed.add_field(name='Roll Composition:', value=f'')

roll_details_embed = Embed(title='Extra Details:', description=f'{mc.ISSUE_CONTACT}', color=mc.embed_colors["black"])
not_enough_wp_embed = Embed(title='Willpower Reroll',
                            description=f'You don\'t have enough willpower. \n\n {mc.ISSUE_CONTACT}',
                            color=mc.embed_colors["red"])
