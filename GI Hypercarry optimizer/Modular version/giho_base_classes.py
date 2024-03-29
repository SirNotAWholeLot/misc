from giho_utility import Char_placeholder

class Char_hypercarry(Char_placeholder):
    def __init__(self, name='Basic hypercarry', element='Physical', scales_with=('ATK', 'DMG', 'CV')):
        super(Char_hypercarry, self).__init__(name, element)
        self.scales_with = scales_with # What stats do we need to show on the widget? Full list of options is  ('HP', 'ATK', 'DEF', 'EM', 'ER', 'DMG', 'CV')
        # Base stats: character ascension
        self.base_stats = {
            'HP': 10000,
            'ATK': 300,
            'DEF': 800,
            'asc_stat': 'None', # Base hypercarry does not have a relevant ascension stat
            'asc_value': 0
        }
        # Weapons
        self.weapon_types = {
            'Basic weapon': Weapon_base(self)
        }
        self.weapon = self.weapon_types['Basic weapon'] # Since this is a reference and not a copy, it can be direct like this instead of an index with same effect
        # Extra stats - artifact substats and non-accounted-for effects
        self.extra_stats = {
            'HP_flat': 4780, # From sources such as the flower or rare weapon effects
            'HP_perc': 0,
            'ATK_flat': 311,
            'ATK_perc': 0,
            'DEF_flat': 0,
            'DEF_perc': 0,
            'EM': 0,
            'ER': 0,
            'DMG': 0, # Ignoring the goblet mainstat, but including such things as artifact 2p effects
            'CV': 170 # Base level invested
        }
        # Artefact types that interest us for this hypercarry
        self.artifact_types = {
            'Sands': (['Other'] 
                            + (['HP%'] if 'HP' in self.scales_with else [])
                            + (['ATK%'] if 'ATK' in self.scales_with else [])
                            + (['DEF%'] if 'DEF' in self.scales_with else [])
                            + (['EM'] if 'EM' in self.scales_with else [])
                            + (['ER%'] if 'ER' in self.scales_with else [])),
            'Goblet': (['Other']
                            + (['HP%'] if 'HP' in self.scales_with else [])
                            + (['ATK%'] if 'ATK' in self.scales_with else [])
                            + (['DEF%'] if 'DEF' in self.scales_with else [])
                            + (['EM'] if 'EM' in self.scales_with else [])
                            + (['Elemental DMG%'] if 'DMG' in self.scales_with else [])),
            'Circlet': (['Other']
                            + (['HP%'] if 'HP' in self.scales_with else [])
                            + (['ATK%'] if 'ATK' in self.scales_with else [])
                            + (['DEF%'] if 'DEF' in self.scales_with else [])
                            + (['EM'] if 'EM' in self.scales_with else [])
                            + (['CRIT'] if 'CV' in self.scales_with else []))
        }
        self.artifacts = {
            'Sands': 'Other',
            'Goblet': 'Other',
            'Circlet': 'Other'
        }
        # Extras: to be filled on character basis
        self.fields = (
            ['Basic hypercarry has no special optional properties', 'text', None, None],
        )
        
    def base_atk(self, weapon=None):
        if weapon == None:
            weapon = self.weapon
        return self.base_stats['ATK'] + weapon.atk[weapon.level]
    # Note: this one function - or rather the requirement of the 'hypercarry base attack' value for both character and weapon buff calculations complicates things immensely
    # Either a weapon has to be an object referenced as property of a character - in which case it has to contain holder reference which isn't good practice,
    # or it has to be contained within the character object itself - in which case we can't override weapons in a convenient manner
    # Possible solution: rewrite it so that 'hypercarry widget' contains a character widget, a weapon widget, and calls buff functions itself, passing one to another when necessary
        
    def calculate_stats(self, weapon=None, artifacts=None):
        # Calculating 'internal' stats. Allows me to not have to change the calculate_output function for specific hypercarries
        stats = {}
        if weapon == None:
            weapon = self.weapon
        if artifacts == None: # No build override
            sands = self.artifacts['Sands']
            goblet = self.artifacts['Goblet']
            circlet = self.artifacts['Circlet']
        else: # Overriding artifacts with provided
            sands = artifacts[0]
            goblet = artifacts[1]
            circlet = artifacts[2]
        stats['HP'] = (1 
                       + (0.466 if sands == 'HP%' else 0) + (0.466 if goblet == 'HP%' else 0) + (0.466 if circlet == 'HP%' else 0) 
                       + self.extra_stats['HP_perc']/100)*self.base_stats['HP'] + self.extra_stats['HP_flat']
        stats['ATK'] = (1 
                        + (0.466 if sands == 'ATK%' else 0) + (0.466 if goblet == 'ATK%' else 0) + (0.466 if circlet == 'ATK%' else 0) 
                        + self.extra_stats['ATK_perc']/100)*self.base_atk(weapon) + self.extra_stats['ATK_flat']
        stats['DEF'] = (1 
                        + (0.583 if sands == 'DEF%' else 0) + (0.583 if goblet == 'DEF%' else 0) + (0.583 if circlet == 'DEF%' else 0) 
                        + self.extra_stats['DEF_perc']/100)*self.base_stats['DEF'] + self.extra_stats['DEF_flat']
        stats['EM'] = 0 + (186.5 if sands == 'EM' else 0) + (186.5 if goblet == 'EM' else 0) + (186.5 if circlet == 'EM' else 0) + self.extra_stats['EM']
        stats['ER'] = 100 + (51.8 if sands == 'ER%' else 0) + self.extra_stats['ER']
        stats['DMG'] = 0 + ((58.3 if self.element == 'Physical' else 46.6) if goblet == 'Elemental DMG%' else 0) + self.extra_stats['DMG']
        stats['CV'] = 5*2 + 50 + (62.2 if circlet == 'CRIT' else 0) + self.extra_stats['CV'] # 'Effective CV' as a plain sum of 2x CR and CD, assuming balanced stats
        # Ascension stats
        asc_stat_char = self.base_stats['asc_stat']
        asc_stat_weap = weapon.asc['stat']
        stat_mults = (self.base_stats['HP']/100, self.base_atk(weapon)/100, self.base_stats['DEF']/100, 1, 1, 1, 1)
        if asc_stat_char != 'None':
            stats[asc_stat_char] = stats[asc_stat_char] + self.base_stats['asc_value']*stat_mults[list(stats.keys()).index(asc_stat_char)]
        if asc_stat_weap != 'None':
            stats[asc_stat_weap] = stats[asc_stat_weap] + weapon.asc[weapon.level]*stat_mults[list(stats.keys()).index(asc_stat_weap)]
        return stats
    
    def apply_self_buffs(self, stats):
        # Independent self-buffs such as ascension passives giving flat stat increases that can be assumed to be always active
        return stats

    def apply_conversions(self, stats):
        # Post-buff conversions such as Hu Tao's PP and Itto's burst. Basic hypercarry doesn't have any self-buffs, so the values are just returned
        return stats

class Weapon_base():
    def __init__(self, holder=None, name='Basic weapon', atk_values=(380, 440, 500), asc_stat='None', asc_values=(0, 0, 0), psv_type='None', psv_range=(False,), psv_value=((None,),)):
        # Because a weapon holds relatively little information, I did not create a non-widget class for them
        # Values are given for levels 70/70, 80/80, 90/90 because otherwise it's too much numbers and likely irrelevant anyhow.
        self.holder = holder # Required to pass some base stats for weapon passives
        self.name = name
        self.level = '90/90'
        self.refine = 1
        self.atk = {'70/70': atk_values[0], '80/80': atk_values[1], '90/90': atk_values[2]}
        self.asc = {'stat': asc_stat, '70/70': asc_values[0], '80/80': asc_values[1], '90/90': asc_values[2]}
        self.psv = {'type': psv_type, 'range': psv_range, 'active': psv_range[0], 'value': psv_value}
    
    def calculate_refines(self):
        psv_value = [] # Handling refines additively
        for i in range(len(self.psv['value'][0])): psv_value.append(self.psv['value'][0][i] + self.psv['value'][1][i]*(self.refine - 1))
        return psv_value
    
    def apply_buffs(self, stats):
        # Apply weapon buffs to stats: basic weapon has none
        return stats

    def apply_conversions(self, stats):
        # Apply conversions to stats: basic weapon has none
        return stats

class Char_buffer(Char_placeholder):
    def __init__(self, name='None', element='Physical'):
        super(Char_buffer, self).__init__(name, element)
        # Abstract party member that provides elemental resonance, but no direct buffs
        self.fields = tuple()

    def buff(self, stats, hypercarry, weapon):
        return