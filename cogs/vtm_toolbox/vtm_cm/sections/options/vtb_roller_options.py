from discord import SelectOption
from misc.config.main_config import EXODUS_EMOJI

difficulty_options = [
    SelectOption(
        label='Zero', value='0', emoji=EXODUS_EMOJI
    ),
    SelectOption(
        label='One', value='1', emoji=EXODUS_EMOJI
    ),
    SelectOption(
        label='Two', value='2', emoji=EXODUS_EMOJI
    ),
    SelectOption(
        label='Three', value='3', emoji=EXODUS_EMOJI
    ),
    SelectOption(
        label='Four', value='4', emoji=EXODUS_EMOJI
    ),
    SelectOption(
        label='Five', value='5', emoji=EXODUS_EMOJI
    ),
    SelectOption(
        label='Six', value='6', emoji=EXODUS_EMOJI
    ),
    SelectOption(
        label='Seven', value='7', emoji=EXODUS_EMOJI
    ),
    SelectOption(
        label='Eight', value='8', emoji=EXODUS_EMOJI
    ),
    SelectOption(
        label='Nine', value='9', emoji=EXODUS_EMOJI
    ),
    SelectOption(
        label='Ten', value='10', emoji=EXODUS_EMOJI
    ),
    SelectOption(
        label='Eleven', value='11', emoji=EXODUS_EMOJI
    ),
    SelectOption(
        label='Twelve', value='12', emoji=EXODUS_EMOJI
    ),
    SelectOption(
        label='Thirteen', value='13', emoji=EXODUS_EMOJI
    )]

attribute_options = [
            SelectOption(
                label='Strength', value='Strength',
                emoji=EXODUS_EMOJI,
            ),
            SelectOption(
                label='Dexterity', value='Dexterity',
                emoji=EXODUS_EMOJI,
            ),
            SelectOption(
                label='Stamina', value='Stamina',
                emoji=EXODUS_EMOJI,
            ),
            SelectOption(
                label='Charisma', value='Charisma',
                emoji=EXODUS_EMOJI,
            ),
            SelectOption(
                label='Manipulation', value='Manipulation',
                emoji=EXODUS_EMOJI,
            ),
            SelectOption(
                label='Composure', value='Composure',
                emoji=EXODUS_EMOJI,
            ),
            SelectOption(
                label='Intelligence', value='Intelligence',
                emoji=EXODUS_EMOJI,
            ),
            SelectOption(
                label='Wits', value='Wits',
                emoji=EXODUS_EMOJI,
            ),
            SelectOption(
                label='Resolve', value='Resolve',
                emoji=EXODUS_EMOJI,
            )]

physical_skill_options = [
    SelectOption(
        label='Athletics', value='Athletics', emoji=EXODUS_EMOJI
    ),
    SelectOption(
        label='Brawl', value='Brawl', emoji=EXODUS_EMOJI
    ),
    SelectOption(
        label='Craft', value='Craft', emoji=EXODUS_EMOJI
    ),
    SelectOption(
        label='Drive', value='Drive', emoji=EXODUS_EMOJI
    ),
    SelectOption(
        label='Firearms', value='Firearms', emoji=EXODUS_EMOJI
    ),
    SelectOption(
        label='Larceny', value='Larceny', emoji=EXODUS_EMOJI
    ),
    SelectOption(
        label='Melee', value='Melee', emoji=EXODUS_EMOJI
    ),
    SelectOption(
        label='Stealth', value='Stealth', emoji=EXODUS_EMOJI
    ),
    SelectOption(
        label='Survival', value='Survival', emoji=EXODUS_EMOJI
    ), ]

social_skill_options = [
    SelectOption(
        label='Animal Ken', value='Animal Ken', emoji=EXODUS_EMOJI
    ),
    SelectOption(
        label='Etiquette', value='Etiquette', emoji=EXODUS_EMOJI
    ),
    SelectOption(
        label='Insight', value='Insight', emoji=EXODUS_EMOJI
    ),
    SelectOption(
        label='Intimidation', value='Intimidation', emoji=EXODUS_EMOJI
    ),
    SelectOption(
        label='Leadership', value='Leadership', emoji=EXODUS_EMOJI
    ),
    SelectOption(
        label='Performance', value='Performance', emoji=EXODUS_EMOJI
    ),
    SelectOption(
        label='Persuasion', value='Persuasion', emoji=EXODUS_EMOJI
    ),
    SelectOption(
        label='Streetwise', value='Streetwise', emoji=EXODUS_EMOJI
    ),
    SelectOption(
        label='Subterfuge', value='Subterfuge', emoji=EXODUS_EMOJI
    ), ]

mental_skill_options = [
    SelectOption(
        label='Academics', value='Academics', emoji=EXODUS_EMOJI
    ),
    SelectOption(
        label='Awareness', value='Awareness', emoji=EXODUS_EMOJI
    ),
    SelectOption(
        label='Finance', value='Finance', emoji=EXODUS_EMOJI
    ),
    SelectOption(
        label='Investigation', value='Investigation', emoji=EXODUS_EMOJI
    ),
    SelectOption(
        label='Medicine', value='Medicine', emoji=EXODUS_EMOJI
    ),
    SelectOption(
        label='Occult', value='Occult', emoji=EXODUS_EMOJI
    ),
    SelectOption(
        label='Politics', value='Politics', emoji=EXODUS_EMOJI
    ),
    SelectOption(
        label='Science', value='Science', emoji=EXODUS_EMOJI
    ),
    SelectOption(
        label='Technology', value='Technology', emoji=EXODUS_EMOJI
    ), ]

discipline_options = [
    SelectOption(label='Animalism', value='Animalism', emoji=EXODUS_EMOJI),
    SelectOption(label='Auspex', value='Auspex', emoji=EXODUS_EMOJI),
    SelectOption(label='Blood Sorcerery', value='Blood Sorcery', emoji=EXODUS_EMOJI),
    SelectOption(label='Blood Rituals', value='Blood Rituals', emoji=EXODUS_EMOJI),
    SelectOption(label='Celerity', value='Celerity', emoji=EXODUS_EMOJI),
    SelectOption(label='Chemeristry', value='Chemeristry', emoji=EXODUS_EMOJI),
    SelectOption(label='Dementation', value='Dementation', emoji=EXODUS_EMOJI),
    SelectOption(label='Dominate', value='Dominate', emoji=EXODUS_EMOJI),
    SelectOption(label='Fortitude', value='Fortitude', emoji=EXODUS_EMOJI),
    SelectOption(label='Necromancy', value='Necromancy', emoji=EXODUS_EMOJI),
    SelectOption(label='Obfuscate', value='Obfuscate', emoji=EXODUS_EMOJI),
    SelectOption(label='Obtenebration', value='Obtenebration', emoji=EXODUS_EMOJI),
    SelectOption(label='Potence', value='Potence', emoji=EXODUS_EMOJI),
    SelectOption(label='Presence', value='Presence', emoji=EXODUS_EMOJI),
    SelectOption(label='Protean', value='Protean', emoji=EXODUS_EMOJI),
    SelectOption(label='Thin-blood Alchemy', value='Thin-Blood Alchemy', emoji=EXODUS_EMOJI),
    SelectOption(label='Hidden/Extra 1', value='Hidden/Extra 1', emoji=EXODUS_EMOJI),
    SelectOption(label='Hidden/Extra 2', value='Hidden/Extra 2', emoji=EXODUS_EMOJI),
    SelectOption(label='Hidden/Extra 3', value='Hidden/Extra 3', emoji=EXODUS_EMOJI)]

extra_options = [
    SelectOption(
        label='One', value='1', emoji=EXODUS_EMOJI
    ),
    SelectOption(
        label='Two', value='2', emoji=EXODUS_EMOJI
    ),
    SelectOption(
        label='Three', value='3', emoji=EXODUS_EMOJI
    ),
    SelectOption(
        label='Four', value='4', emoji=EXODUS_EMOJI
    ),
    SelectOption(
        label='Five', value='5', emoji=EXODUS_EMOJI
    ),
    SelectOption(
        label='Minus One', value='-1', emoji=EXODUS_EMOJI
    ),
    SelectOption(
        label='Minus Two', value='-2', emoji=EXODUS_EMOJI
    ),
    SelectOption(
        label='Minus Three', value='-3', emoji=EXODUS_EMOJI
    ),
    SelectOption(
        label='Minus Four', value='-4', emoji=EXODUS_EMOJI
    ),
    SelectOption(
        label='Minus Five', value='-5', emoji=EXODUS_EMOJI)]

hunt_mod_options = [SelectOption(label='Negative One', value='-1', emoji=EXODUS_EMOJI),
                    SelectOption(label='Negative Two', value='-2', emoji=EXODUS_EMOJI),
                    SelectOption(label='Negative Three', value='-3', emoji=EXODUS_EMOJI),
                    SelectOption(label='Negative Four', value='-4', emoji=EXODUS_EMOJI),
                    SelectOption(label='Negative Five', value='-5', emoji=EXODUS_EMOJI),
                    SelectOption(label='Zero', value='0', emoji=EXODUS_EMOJI),
                    SelectOption(label='One', value='1', emoji=EXODUS_EMOJI),
                    SelectOption(label='Two', value='2', emoji=EXODUS_EMOJI),
                    SelectOption(label='Three', value='3', emoji=EXODUS_EMOJI),
                    SelectOption(label='Four', value='4', emoji=EXODUS_EMOJI),
                    SelectOption(label='Five', value='5', emoji=EXODUS_EMOJI),]
