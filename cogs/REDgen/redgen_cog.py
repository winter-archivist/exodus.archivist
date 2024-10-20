import discord
from zenlog import log
import discord.ext

from random import randint


async def generate(target_string: str, OPTIONS: tuple, RANGE: tuple, NAME: str):
    target_string += f'{NAME}: {OPTIONS[randint(RANGE[0], RANGE[1])]} \n'
    return target_string


class REDGEN(discord.ext.commands.Cog):
    # This was scrapped together in very little time, it is bad code
    def __init__(self, CLIENT):
        self.CLIENT = CLIENT

    @discord.app_commands.command(name='redgen', description='Generates a Random Cyberpunk RED character.')
    async def redgen(self, interaction: discord.Interaction):
        if interaction.user.id != 567819777209532418:
            return
        to_write: str = ''

        # RANGES
        R10: tuple = (0, 9)

        roles: tuple = \
            ('Rockerboy', 'Solo', 'Netrunner',
             'Tech', 'Medtech', 'Media',
             'Exec', 'Lawman', 'Fixer',
             'Nomad')
        cultural_origins: tuple = \
            ('North American', 'South/Central American', 'Western European',
             'Easter European', 'Middle Eastern/North African', 'Sub-Saharan African',
             'South Asian', 'South East Asian', 'East Asian',
             'Oceania/Pacific Islander')
        personalities: tuple = \
            ('Shy & Secretive', 'Rebellious, Antisocial, & Violent', 'Arrogant, Proud, & Aloof',
             'Moody, Rash, & Headstrong', 'Picky, Fuss, & Nervous', 'Stable & Serious',
             'Silly & Fluff-Headed', 'Sneaky & Deceptive', 'Intellectual & Detached',
             'Friendly & Outgoing')
        clothing_styles: tuple = \
            ('Generic Chic', 'Leisurewear', 'Urban Flash',
             'Business-wear', 'High Fashion', 'Bohemian',
             'Bag Lady Chic', 'Gang Colors', 'Nomad Leathers',
             'Asia Pop')
        affectations: tuple = \
            ('Tattoos', 'Mirrorshades', 'Ritual Scars',
             'Spiked Gloves', 'Nose Rings', 'Tongue or other Piercings',
             'Strange fingernail implants', 'Spiked boots or heels', 'fingerless gloves',
             'Strange Contacts')
        concepts_valued_most: tuple = \
            ('Money', 'Honor', 'Your Word',
             'Honesty', 'Knowledge', 'Vengeance',
             'Love', 'Power', 'Family',
             'Friendship')
        feelings_towards_people: tuple = \
            ('I stay neutral', 'I stay neutral', 'I like almost everyone',
             'I hate almost everyone', 'People are Tools. Use them for your own goals then discard them.',
             'Every person is a valuable individual',
             'People are obstacles to be destroyed if they cross me', 'People are untrustworthy. Don\'t Depend on them.',
             'Wipe \'em all out and let the cockroaches take over.',
             'People are wonderful.')
        people_valued_most: tuple = \
            ('A parent', 'A brother or sister', 'A lover',
             'A friend', 'Yourself', 'A pet',
             'A Teacher or Mentor', 'A public figure', 'A personal hero',
             'No One')
        items_valued_most: tuple = \
            ('A Weapon', 'A Tool', 'A Piece of Clothing',
             'A photograph', 'A book or diary', 'A recording',
             'A musical instrument', 'A piece of jewelry', 'A toy',
             'A letter')
        backgrounds: tuple = \
            ('Corporate Execs', 'Corporate Managers', 'Corporate Technicians',
             'Nomad Pack', 'Ganger "Family"', 'Combat Zoners',
             'Urban Homeless', 'Megastructure Warren Rats', 'Reclaimers',
             'Edgerunners')
        childhood_environments: tuple = \
            ('Ran on The Street, with no adult supervision', 'Spent in safe corp zone walled off from the rest of the city',
             'In a nomad pack moving from place to place',
             'In a Nomad Pack with roots in transport',
             'In a decaying, once upscale, neighborhood, now holding off the boosters to survive',
             'In the heart of the Combat Zone, living in a wrecked building or other squat',
             'In a huge "megastructure" building controlled by a Corp or the City.',
             'In the ruins of a deserted town or city taken over by reclaimers',
             'In a Drift nation that is a meeting place for all kinds of people',
             'In a Corporate luxury "starscraper", high above the rest of the teeming rabble.')
        family_crisises: tuple = \
            ('Your family lost everything through betrayal', 'Your family lost everything through bad management',
             'Your family was exiled or otherwise driven from their original home/nation/Corporation',
             'Your family is imprisoned, and you alone escaped.', 'Your family vanished. You are the only remaining member.',
             'Your family was killed, and you were the only survivor',
             'Your family is involved in a long-term conspiracy, organization, or association, such as a crime, family or revolutionary group.',
             'Your family was scattered to the winds due to misfortune',
             'Your family is cursed with a hereditary fued that has lasted for generation.',
             'You are the inheritor of a family debtl you must honor this debt before moving on with your life.')
        life_goals: tuple = \
            ('Get rid of a bad reputation', 'Gain power & control', 'Get off the street no matter what it takes',
             'Cause Pain & Suffering to anyone who crosses you', 'Live down your past life and try to forget it',
             'Hunt down those responsible for your miserable life and make them pay',
             'Get what\'s rightfully yours.',
             'Save, if possible, anyone else involved in your background, like a lover, or family member.',
             'Gain Fame & Recognition.',
             'Become Feared & Respected.')

        INPUT_OPTIONS: tuple = (roles, cultural_origins, personalities, clothing_styles, affectations, concepts_valued_most,
                                feelings_towards_people, people_valued_most, items_valued_most, backgrounds,
                                childhood_environments, family_crisises, life_goals)
        INPUT_NAMES: tuple = ('Role', 'Cultural Origin', 'Personality', 'Clothing Style', 'Affectation', 'Concept Most Valued',
                              'Feeling Towards People', 'Person Valued Most', 'Item Valued Most', 'Background',
                              'Childhood Environment', 'Family Crisis', 'Life Goal')
        while_var: int = 0
        while while_var != 13:
            to_write = await generate(target_string=to_write,
                                      OPTIONS=INPUT_OPTIONS[while_var],
                                      RANGE=R10,
                                      NAME=INPUT_NAMES[while_var])
            while_var += 1

        friend_chance: int = randint(0, 9)
        if friend_chance > 7:
            friend_relationships: tuple = \
                ('Like an older sibling to you', 'Like a younger sibling to you', 'A teacher or mentor',
                 'A partner or coworker', 'A former lover', 'An old enemy',
                 'Like a parent to you', 'An old Childhood friend', 'Someone you know from The Street',
                 'Someone with a common interest or goal.')
            friend_relationship: str = friend_relationships[randint(0, 9)]
        else:
            friend_relationship: str = 'None'
        to_write += f'Friend Relationship: {friend_relationship} \n'

        enemy_chance: int = randint(1, 11)
        if enemy_chance > 7:
            enemies: tuple = \
                ('Ex-Friend', 'Ex-lover', 'Estrangled Relative',
                 'Childhood Enemy', 'Person working for you', 'Person you work for',
                 'Partner or Coworker', 'Corporate Exec', 'Government Official',
                 'Boosterganger')
            enemy: str = enemies[randint(0, 9)]

            enemy_whys: tuple = \
                ('Caused the other to lose face or status', 'Caused the loss of a lover, friend, or relative',
                 'Caused a major public humiliation',
                 'Accused the other of cowardice or some other major personal flaw', 'Deserted or betrayed the other',
                 'Turned down the other\'s offer of a job or romantic involvement',
                 'You just don\'t like each other', 'One of you was a romantic rival', 'One of you was a business rival.',
                 'One of you set the other up for a crime they didn\'t commit.')
            enemy_why: str = enemy_whys[randint(0, 9)]
            to_write += f'Enemy Cause: {enemy_why} \n'

            enemy_capabilities: tuple = \
                (
                    'Just themselves & even they won\'t go out of their way', 'Just themselves',
                    'Just themselves and a close friend',
                    'Themselves & a few (1d6/2) friends', 'Themselves & a few (1d10/2) friends',
                    'An entire gang (at least 1d10+5 People)',
                    'The Local Cops or Other Lawmen', 'A powerful gang lord or small corporation', 'A powerful Corporation',
                    'An entire city or government or agency')
            enemy_capability: str = enemy_capabilities[randint(0, 9)]
            to_write += f'Enemy Capability: {enemy_capability} \n'

            enemy_endings: tuple = \
                ('Avoid the scum', 'Avoid the scum',
                 'Go into a murderous rage and try to physically rip their face off',
                 'Go into a murderous rage and try to physically rip their face off',
                 'Backstab them indirectly', 'Backstab them indirectly',
                 'Verbally attack them', 'Verbally attack them',
                 'Set them up for a crime or other transgression they didn\'t commit',
                 'Set out to murder or maim them.')
            enemy_ending: str = enemy_endings[randint(0, 9)]
            to_write += f'Enemy If Encountered: {enemy_ending} \n'
        else:
            enemy: str = 'None'
        to_write += f'Enemy: {enemy} \n'

        tragic_love_chance: int = randint(0, 9)
        if tragic_love_chance > 7:
            tragic_loves: tuple = \
                ('Your lover died in an accident', 'Your lover mysteriously vanished', 'It just didn\'t work out',
                 'A personal goal or vendetta came between you & your lover', 'Your lover was kidnapped',
                 'Your lover went insane or cyberpsycho',
                 'Your lover committed suicide', 'Your lover was killed in a fight', 'A rival cut you out of the action.',
                 'Your lover is imprisoned or exiled.')
            tragic_love: str = roles[randint(0, 9)]
        else:
            tragic_love: str = 'None'
        to_write += f'Tragic Love: {tragic_love} \n'

        # generates a list of 9 numbers from 2 to 8.
        stats: list = []
        while_var: int = 0
        while while_var != 10:
            random_number: int = randint(2, 8)
            stats.append(random_number)
            while_var += 1

        # Brute forces the sum of stats[] to be 62.
        while sum(stats) != 62:
            # If the sum is lesser or greater than 62 it randomly selects a stat
            random_target: int = randint(1, 8)
            if sum(stats) > 62:
                # If the sum is greater than 62
                # Reduce the randomly selected Stat by one
                # if it isn't at the minimum value
                if stats[random_target] != 2:
                    stats[random_target] -= 1
            elif sum(stats) < 62:
                # If the sum is lesser than 62
                # Increase the randomly selected Stat by one
                # if it isn't at the maximum value
                if stats[random_target] != 8:
                    stats[random_target] += 1

        STATS_NAMES: tuple = (
            'Intelligence', 'Willpower', 'Cool', 'Empathy', 'Technique', 'Reflexes', 'Luck', 'Body', 'Dexterity', 'Movement')
        while_var = 0
        while while_var != 9:
            to_write += f'{STATS_NAMES[while_var]}: {stats[while_var]} \n'
            while_var += 1

        with open('cogs/REDgen/generated_character.txt', 'w') as file:
            file.write(to_write)

        await interaction.response.send_message(file=discord.File('cogs/REDgen/generated_character.txt'))
        return


async def setup(CLIENT):
    await CLIENT.add_cog(REDGEN(CLIENT))
