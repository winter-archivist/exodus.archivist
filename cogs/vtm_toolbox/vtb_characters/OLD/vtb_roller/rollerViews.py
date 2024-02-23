

async def reRoller(self, interaction, button, return_page):
    character_name = await vU.getCharacterName(interaction)

    # Finding Starting Roll Pool, Difficulty, & Roll Info
    with sqlite3.connect(f'cogs//vampire//vtb_characters//{str(interaction.user.id)}//{character_name}//{character_name}.sqlite') as db:
        cursor = db.cursor()
        roll_pool = int(cursor.execute('SELECT rollPool FROM commandVars').fetchone()[0])
        difficulty = int(cursor.execute('SELECT difficulty from commandVars').fetchone()[0])
        wp_base = cursor.execute('SELECT willpowerBase FROM willpower').fetchone()[0]
        wp_SUP = cursor.execute('SELECT willpowerSUP FROM willpower').fetchone()[0]
        wp_AGG = cursor.execute('SELECT willpowerAGG FROM willpower').fetchone()[0]
        hunger_crit = cursor.execute('SELECT hungerCritDie FROM rerollInfo').fetchone()[0]
        regular_crit = cursor.execute('SELECT regularCritDie FROM rerollInfo').fetchone()[0]
        regular_success = cursor.execute('SELECT regularSuccess FROM rerollInfo').fetchone()[0]
        hunger_success = cursor.execute('SELECT hungerCritDie FROM rerollInfo').fetchone()[0]
        regular_fail = cursor.execute('SELECT regularFail FROM rerollInfo').fetchone()[0]
        hunger_skulls = cursor.execute('SELECT hungerSkull FROM rerollInfo').fetchone()[0]

    roll_results: dict = {'regular_crit'  : regular_crit, 'hunger_crit': hunger_crit, 'regular_success': regular_success,
                          'hunger_success': hunger_success, 'regular_fail': regular_fail, 'hunger_skull': hunger_skulls}

    # Reroll up to 3 regular-failures
    if roll_results['regular_fail'] >= 3:
        rerolls = 3
        roll_results['regular_fail'] -= 3
    else:
        rerolls = roll_results['regular_fail']
        roll_results['regular_fail'] -= roll_results['regular_fail']

    # Find new roll numbers
    while 0 < rerolls:
        die_result = randint(1, 10)

        if die_result == 10:
            roll_results['regular_crit'] += 1
        elif die_result >= 6:
            roll_results['regular_success'] += 1
        elif die_result <= 5:
            roll_results['regular_fail'] += 1

        rerolls -= 1

    # Update roll info
    try:
        with sqlite3.connect(f'cogs//vampire//vtb_characters//{str(interaction.user.id)}//{character_name}//{character_name}.sqlite') as db:
            cursor = db.cursor()
            cursor.execute('UPDATE rerollInfo SET regularCritDie=?, regularSuccess=?, regularFail=?',
                           (roll_results['regular_crit'], roll_results['regular_success'], roll_results['regular_fail']))
            db.commit()
    except sqlite3.Error as e:
        log.error(f'reRoller_2 | SQLITE3 ERROR | {e}')

    # Find New Crits
    crits = 0
    flag = ''
    while_total = roll_results['regular_crit'] + roll_results['hunger_crit']
    while while_total > 0:
        if roll_results['regular_crit'] + roll_results['hunger_crit'] > 2:
            if roll_results['regular_crit'] >= 2:
                crits += 4
                roll_results['regular_crit'] -= 2

            elif roll_results['hunger_crit'] >= 2:
                crits += 4
                flag = 'Messy Crit'
                roll_results['hunger_crit'] -= 2

            elif roll_results['regular_crit'] + roll_results['hunger_crit'] >= 2:
                crits += 4
                flag = 'Messy Crit'
                break
        else:
            break
        while_total -= 1

    crits += roll_results['hunger_crit'] + roll_results['regular_crit']
    total_successes = int(roll_results['regular_success'] + roll_results['hunger_success'] + crits)

    if total_successes >= difficulty and flag == '':
        flag = 'Regular Success'
    elif total_successes <= difficulty and flag == '':
        flag = 'Regular Fail'

    if wp_base <= wp_AGG:
        button.disabled = True
        button.label = 'Fate Sealed'
        await interaction.response.edit_message(view=self)
        return
    elif wp_base <= wp_SUP:
        db.cursor().execute('UPDATE willpower SET willpowerAGG=?', (str(wp_AGG + 1),))
    else:
        db.cursor().execute('UPDATE willpower SET willpowerSUP=?', (str(wp_SUP + 1),))
    db.commit()

    button.disabled = True
    button.label = 'Fate Tempted'

    # Assigns Information
    return_page.add_field(name='Roll Result:', value=f'{total_successes} | {flag}')
    log.crit(f'{total_successes=} | {crits=} | {difficulty=}')
    return return_page
