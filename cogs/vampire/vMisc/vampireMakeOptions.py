from discord import SelectOption

one_to_five_options = [
    SelectOption(
        label='One', value='1', emoji='<:snek:785811903938953227>'
    ),
    SelectOption(
        label='Two', value='2', emoji='<:snek:785811903938953227>'
    ),
    SelectOption(
        label='Three', value='3', emoji='<:snek:785811903938953227>'
    ),
    SelectOption(
        label='Four', value='4', emoji='<:snek:785811903938953227>'
    ),
    SelectOption(
        label='Five', value='5', emoji='<:snek:785811903938953227>'
    )]
clan_options = [
    SelectOption(
        label='C0', value='0', emoji='<:snek:785811903938953227>'
    ),
    SelectOption(
        label='C1', value='1', emoji='<:snek:785811903938953227>'
    ),
    SelectOption(
        label='C2', value='2', emoji='<:snek:785811903938953227>'
    ),
    SelectOption(
        label='C3', value='3', emoji='<:snek:785811903938953227>'
    ),]
generation_options = [
    SelectOption(
        label='Generation 15', value='15', emoji='<:snek:785811903938953227>'
    ),
    SelectOption(
        label='Generation 14', value='14', emoji='<:snek:785811903938953227>'
    ),
    SelectOption(
        label='Generation 13', value='13', emoji='<:snek:785811903938953227>'
    ),
    SelectOption(
        label='Generation 12', value='12', emoji='<:snek:785811903938953227>'
    ),
    SelectOption(
        label='Generation 11', value='11', emoji='<:snek:785811903938953227>'
    ),
    SelectOption(
        label='Generation 10', value='10', emoji='<:snek:785811903938953227>'
    ),
    SelectOption(
        label='Generation 9', value='9', emoji='<:snek:785811903938953227>'
    ),
    SelectOption(
        label='Generation 8', value='8', emoji='<:snek:785811903938953227>'
    ),
    SelectOption(
        label='Generation 7', value='7', emoji='<:snek:785811903938953227>'
    ),
    SelectOption(
        label='Generation 6', value='6', emoji='<:snek:785811903938953227>'
    ),
    SelectOption(
        label='Generation 5', value='5', emoji='<:snek:785811903938953227>'
    ),
    SelectOption(
        label='Generation 4', value='4', emoji='<:snek:785811903938953227>'
    ),
    SelectOption(
        label='Generation 3', value='3', emoji='<:snek:785811903938953227>'
    ),
    SelectOption(
        label='Generation 2', value='2', emoji='<:snek:785811903938953227>'
    ),
    SelectOption(
        label='Generation 1', value='1', emoji='<:snek:785811903938953227>'
    ),
]
skill_options = [
    SelectOption(
        label='Athletics', value='Athletics', emoji='<:snek:785811903938953227>'
    ),
    SelectOption(
        label='Brawl', value='Brawl', emoji='<:snek:785811903938953227>'
    ),
    SelectOption(
        label='Craft', value='Craft', emoji='<:snek:785811903938953227>'
    ),
    SelectOption(
        label='Drive', value='Drive', emoji='<:snek:785811903938953227>'
    ),
    SelectOption(
        label='Firearms', value='Firearms', emoji='<:snek:785811903938953227>'
    ),
    SelectOption(
        label='Larceny', value='Larceny', emoji='<:snek:785811903938953227>'
    ),
    SelectOption(
        label='Melee', value='Melee', emoji='<:snek:785811903938953227>'
    ),
    SelectOption(
        label='Stealth', value='Stealth', emoji='<:snek:785811903938953227>'
    ),
    SelectOption(
        label='Survival', value='Survival', emoji='<:snek:785811903938953227>'
    ),
    SelectOption(
        label='Animal Ken', value='Animal Ken', emoji='<:snek:785811903938953227>'
    ),
    SelectOption(
        label='Etiquette', value='Etiquette', emoji='<:snek:785811903938953227>'
    ),
    SelectOption(
        label='Insight', value='Insight', emoji='<:snek:785811903938953227>'
    ),
    SelectOption(
        label='Intimidation', value='Intimidation', emoji='<:snek:785811903938953227>'
    ),
    SelectOption(
        label='Leadership', value='Leadership', emoji='<:snek:785811903938953227>'
    ),
    SelectOption(
        label='Performance', value='Performance', emoji='<:snek:785811903938953227>'
    ),
    SelectOption(
        label='Persuasion', value='Persuasion', emoji='<:snek:785811903938953227>'
    ),
    SelectOption(
        label='Streetwise', value='Streetwise', emoji='<:snek:785811903938953227>'
    ),
    SelectOption(
        label='Subterfuge', value='Subterfuge', emoji='<:snek:785811903938953227>'
    ),
    SelectOption(
        label='Academics', value='Academics', emoji='<:snek:785811903938953227>'
    ),
    SelectOption(
        label='Awareness', value='Awareness', emoji='<:snek:785811903938953227>'
    ),
    SelectOption(
        label='Finance', value='Finance', emoji='<:snek:785811903938953227>'
    ),
    SelectOption(
        label='Investigation', value='Investigation', emoji='<:snek:785811903938953227>'
    ),
    SelectOption(
        label='Medicine', value='Medicine', emoji='<:snek:785811903938953227>'
    ),
    SelectOption(
        label='Occult', value='Occult', emoji='<:snek:785811903938953227>'
    ),
    SelectOption(
        label='Politics', value='Politics', emoji='<:snek:785811903938953227>'
    ),
    SelectOption(
        label='Science', value='Science', emoji='<:snek:785811903938953227>'
    ),
    SelectOption(
        label='Technology', value='Technology', emoji='<:snek:785811903938953227>'
    )
]

# ? ownerInfo
# ! Auto-Set userID/userName

# ? rerollInfo
# * Keep ALL = 0

# ? commandVars
# * Keep difficulty, rollPool, result = 0
# * Keep poolComp = 'Empty'

# ? Char Info
# ! Set blood_potency = one_to_five_options
# ! Set clan = clan_options
# ! Set generation = generation_options
# ! Set bane_severity Based Off Generation
# * Keep Hunger = 0

# ? charAttributes
# ! Set ALL_attributes = one_to_five_options

# ? physicalSkills
# ? socialSkills
# ? mentalSkills
# * Basically you select 0, 1, 2, 3, 4, 5 dots for each skill
# ! Set allSkills = physical_skills_options

# ? disciplines
# ! Set ALL_discipline = one_to_five_options

# ? health
# ! Auto-Set /w Stamina+3: Allow Edits in vampireManager

# ? willpower
# ! Auto-Set Composure+Resolve: Allow Edits in vampireManager
