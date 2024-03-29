from giho_base_classes import Weapon_base

class Weapon_custom(Weapon_base):
    def __init__(self, holder = None):
        super(Weapon_custom, self).__init__(holder, 'Custom weapon')
        # Custom weapon: customizable stats, no passive
        self.level = 0
        self.atk = [500]
        self.asc = {'stat': 'None', 0: 0}

class Weapon_amenoma_kageuchi(Weapon_base):
    def __init__(self, holder = None):
        super(Weapon_amenoma_kageuchi, self).__init__(holder, 'Amenoma Kageuchi', (347, 401, 454), 'ATK', (45.4, 50.3, 55.1), 'Does not affect stats directly')

class Weapon_finale_of_the_deep(Weapon_base):
    def __init__(self, holder = None):
        super(Weapon_finale_of_the_deep, self).__init__(holder, 'Finale of the Deep', (429, 497, 565), 'ATK', (22.7, 25.1, 27.6), 'stacks', (0, 2), ((12, 150), (3, 37.5)))
        
    def apply_buffs(self, stats):
        psv_value = self.calculate_refines()
        # Finale of the Deep increases ATK by psv_value[0] after using a skill and further by psv_value[1] if the lifebond is cleared
        stats['ATK'] = stats['ATK'] + (psv_value[0] if self.psv['active'] >= 1 else 0)*self.holder.base_atk(self)/100
        stats['ATK'] = stats['ATK'] + (psv_value[1] if self.psv['active'] >= 2 else 0)
        return stats

class Weapon_mistsplitter_reforged(Weapon_base):
    def __init__(self, holder = None):
        super(Weapon_mistsplitter_reforged, self).__init__(holder, 'Mistsplitter Reforged', (506, 590, 674), 'CV', (36.3, 40.2, 44.1), 'stacks', (0, 3), ((12, 8), (3, 2)))
        
    def apply_buffs(self, stats):
        psv_value = self.calculate_refines()
        # Mistsplitter Reforged provides an unconditional psv_value[0] DMG% bonus and 1x/2x/3.5x psv_value[1] DMG% bonus from stacks
        stats['DMG'] = stats['DMG'] + psv_value[0] + psv_value[1]*(0, 1, 2, 3.5)[self.psv['active']]
        return stats
    
class Weapon_the_catch(Weapon_base):
    def __init__(self, holder = None):
        super(Weapon_the_catch, self).__init__(holder, 'The Catch', (388, 449, 510), 'ER', (37.9, 41.9, 45.9), 'bool', (False, True), ((16, 6), (4, 1.5)))
        # The Catch is assumed to be R5 because why not
        self.refine = 5
        
    def apply_buffs(self, stats):
        psv_value = self.calculate_refines()
        # The Catch increases DMG by psv_value[0] and CRIT Rate by psv_value[1] if what we are calculating for is an elemental burst
        stats['DMG'] = stats['DMG'] + (psv_value[0] if self.psv['active'] == True else 0)
        stats['CV'] = stats['CV'] + (psv_value[1]*2 if self.psv['active'] == True else 0)
        return stats
        
class Weapon_engulfing_lightning(Weapon_base):
    def __init__(self, holder = None):
        super(Weapon_engulfing_lightning, self).__init__(holder, 'Engulfing Lightning', (457, 532, 608), 'ER', (45.4, 50.3, 55.1), 'bool', (False, True), ((28, 80), (7, 10)))

    def apply_buffs(self, stats):
        # Engulfing Lightning increases ER by 30% if what we are calculating for is an elemental burst
        stats['ER'] = stats['ER'] + (30 if self.psv['active'] == True else 0)
        return stats

    def apply_conversions(self, stats):
        psv_value = self.calculate_refines()
        # Engulfing Lightning converts ER over 100 to ATK at psv_value[0]*base_atk efficiency, up to psv_value[1]% total
        stats['ATK'] = stats['ATK'] + max(psv_value[1], psv_value[0]*(stats['ER']/100 - 1))*self.holder.base_atk(self)/100
        return stats
    
class Weapon_serpent_spine(Weapon_base):
    def __init__(self, holder = None):
        super(Weapon_serpent_spine, self).__init__(holder, 'Serpent Spine', (388, 449, 510), 'CV', (45.4, 50.3, 55.1), 'stacks', (0, 5), ((6,), (1,)))
        
    def apply_buffs(self, stats):
        psv_value = self.calculate_refines()
        # Serpent Spine provides psv_value[0] DMG% bonus for every stack
        stats['DMG'] = stats['DMG'] + psv_value[0]*self.psv['active']
        return stats

class Weapon_redhorn_stonethresher(Weapon_base):
    def __init__(self, holder = None):
        super(Weapon_redhorn_stonethresher, self).__init__(holder, 'Redhorn Stonethresher', (408, 475, 542), 'CV', (72.7, 80.4, 88.2), 'perc', (0, 100), ((28, 40), (7, 10)))
        
    def apply_buffs(self, stats):
        psv_value = self.calculate_refines()
        # Redhorn Stonethresher provides psv_value[0] DEF% bonus and increases Normal/Charged attack DMG% by psv_value[1]
        stats['DEF'] = stats['DEF'] + psv_value[0]*self.holder.base_stats['DEF']/100
        stats['DMG'] = stats['DMG'] + (psv_value[1] if self.psv['active'] else 0)
        return stats        