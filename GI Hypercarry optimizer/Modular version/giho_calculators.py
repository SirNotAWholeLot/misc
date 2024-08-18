def res_mult(res):
    '''Recalculating resistance multipliers using formulas from the wiki.'''
    if res > 75:
        return 1/(4*res/100 + 1)
    elif res > 0:
        return 1 - res/100
    else:
        return 1 - res/200
        
def get_elements_in_party(hypercarry, buffers):
    elements = [hypercarry.element]
    for buffer in buffers:
        if buffer.element != 'None': elements.append(buffer.element)
    return elements        

def calculate_output(enemy_res, hypercarry, weapon=None, artifacts=None, buffers=None):
    '''The main piece - calculates theoretical damage output of the hypercarry.
    First calculates internal stats and resonances,
    then adds self-buffs and weapon buffs,
    then buffs of each of the buffers in the party,
    then applies conversions such as Hu Tao's skill,
    then reoptimizes CV (assumingly we built it balanced for this),
    and last applies enemy resistances.'''
    if weapon == None:
        weapon = hypercarry.weapon
    stats = hypercarry.calculate_stats(weapon = weapon, artifacts = artifacts)
    stats['elements_in_party'] = get_elements_in_party(hypercarry, buffers)
    # Elemental resonances - the ones that count are Pyro, Hydro, Cryo, Geo and Dendro
    if stats['elements_in_party'].count('Pyro') >= 2:
        stats['ATK'] = stats['ATK'] + 0.25*hypercarry.base_atk(weapon)
    if stats['elements_in_party'].count('Hydro') >= 2:
        stats['HP'] = stats['HP'] + 0.25*hypercarry.base_stats['HP']
    if stats['elements_in_party'].count('Cryo') >= 2:
        stats['CV'] = stats['CV'] + 30 # Not really true for Melt, but whatever
    if stats['elements_in_party'].count('Geo') >= 2:
        stats['DMG'] = stats['DMG'] + 15
        if hypercarry.element == 'Geo': enemy_res = enemy_res - 20
    if stats['elements_in_party'].count('Dendro') >= 2:
        stats['EM'] = stats['EM'] + 75 # Average since we don't know the reactions
    # Buffs
    stats = hypercarry.apply_self_buffs(stats)
    stats = weapon.apply_buffs(stats)
    for buffer in buffers:
        if buffer.name != 'None': buffer.buff(stats, hypercarry, weapon)
    for shred in ['shred_vv', 'shred_chevreuse', 'shred_zhongli']:
        if shred in stats: enemy_res = enemy_res - stats[shred]
    # Conversions
    stats = hypercarry.apply_conversions(stats)
    stats = weapon.apply_conversions(stats)
    stats['CR'] = min(stats['CV']/4, 100)
    stats['CD'] = stats['CV'] - 2*stats['CR']
    return stats['ATK']*(1 + stats['DMG']/100)*(1 + (stats['CR']/100)*(stats['CD']/100))*res_mult(enemy_res), stats
    
def format_stats(stats):
    '''Formats stats dictionary into a more human-readable form.'''
    stats_formatted = ''
    shred_sum = 0
    for key, value in stats.items():
        if key in ('HP', 'ATK', 'DEF', 'EM'): stats_formatted = stats_formatted + key + ': ' + "{:.0f}".format(value) + ' | '
        if key in ('ER', 'DMG', 'CR', 'CD'): stats_formatted = stats_formatted + key + ': ' + "{:.1f}".format(value) + '% | '
        if 'shred' in key: shred_sum = shred_sum + stats[key]
    stats_formatted = stats_formatted + 'RES shred: ' + "{:.1f}".format(shred_sum)
    return stats_formatted