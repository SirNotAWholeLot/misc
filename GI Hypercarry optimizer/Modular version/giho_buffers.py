from giho_utility import Char_placeholder
from giho_base_classes import Char_buffer

class Char_vv(Char_buffer):
    '''Somebody doing a VV who is not Kazuha. Faruzan can technically hold VV, but she only buffs Anemo damage which can't be VVed so she is a separate case entirely.'''
    def __init__(self):
        super(Char_vv, self).__init__('VV provider', 'Anemo')
        self.fields = (
            ['Providing elemental RES shred through 4p Viridescent Venerer swirls', 'text', None, None],
        )

    def is_relevant(self, hypercarry):
        return hypercarry.element in ('Pyro', 'Hydro', 'Electro', 'Cryo')
    
    def buff(self, stats, hypercarry, weapon):
        if hypercarry.element in ('Pyro', 'Hydro', 'Electro', 'Cryo'): stats['shred_vv'] = 40
    
class Char_bennett(Char_buffer):
    '''Bennett, the true Pyro Archon. Buffs ATK additively and can also buff Pyro DMG%.
    Default Bennett is assumed to have Base ATK of 750 (approx. lvl 90 Sapwood 90), talent level of 8, C0, and has 4p Noblesse Obligue.'''
    def __init__(self):
        super(Char_bennett, self).__init__('Bennett', 'Pyro')
        self.fields = (
            ['Base ATK', 'int', (0, 9999), 750],
            ['Talent level', 'int', (1, 13), 8],
            ['Constellation', 'int', (0, 6), 0],
            ['Holds 4p Noblesse Obligue', 'bool', None, True]
        )
    
    def is_relevant(self, hypercarry):
        return 'ATK' in hypercarry.scales_with or ('DMG' in hypercarry.scales_with and hypercarry.element == 'Pyro')
        
    def buff_value_atk(self):
        return self.fields[0][3]*((56, 60.2, 64.4, 70, 74.2, 78.4, 84, 89.6, 95.2, 100.8, 106.4, 112, 119, 126)[self.fields[1][3]-1] + (20 if self.fields[2][3] >= 1 else 0))/100
    
    def buff(self, stats, hypercarry, weapon):
        stats['ATK'] = stats['ATK'] + self.buff_value_atk() + (0.2*hypercarry.base_atk(weapon) if self.fields[3][3] else 0)
        stats['DMG'] = stats['DMG'] + (15 if self.fields[2][3] == 6 and hypercarry.element == 'Pyro' else 0)
     
class Char_sara(Char_buffer):
    '''Kujou Sara, Raiden Shogun's personal buffer. Buffs ATK additively and at C6 buffs Electro-only Crit DMG.
    Default Sara is assumed to have Base ATK of 750 (approx. lvl 90 565-bow 90), talent level of 8 and no C6.'''
    def __init__(self):
        super(Char_sara, self).__init__('Sara', 'Electro')
        self.fields = (
            ['Base ATK', 'int', (0, 9999), 750],
            ['Talent level', 'int', (1, 13), 8],
            ['Is C6', 'bool', None, False]
        )
        
    def is_relevant(self, hypercarry):
        return 'ATK' in hypercarry.scales_with or ('CV' in hypercarry.scales_with and hypercarry.element == 'Electro')
        
    def buff_value_atk(self): # CDMG buff is added separately, that's why we need carry's crit stats
        return self.fields[0][3]*((43, 46, 49, 54, 57, 60, 64.4, 69, 73.0, 77.3, 81.6, 85.9, 91.2, 97)[self.fields[1][3]-1])/100

    def buff(self, stats, hypercarry, weapon):
        stats['ATK'] = stats['ATK'] + self.buff_value_atk()
        stats['CV'] = stats['CV'] + (60 if self.fields[2][3] == True and hypercarry.element == 'Electro' else 0)

class Char_furina(Char_buffer):
    '''Mademoiselle Furina, unmatched in universality. Ramping-up buff provides massive DMG% to the whole party.
    Default Furina is assumed to have average Fanfare charge percent of 75, talent level of 8 and no C1.'''
    def __init__(self):
        super(Char_furina, self).__init__('Furina', 'Hydro')
        self.fields = (
            ['Avg. Fanfare', 'int', (0, 300), 200],
            ['Talent level', 'int', (1, 13), 8],
            ['Is C1', 'bool', None, False]
        )

    def is_relevant(self, hypercarry):
        return 'DMG' in hypercarry.scales_with
        
    def buff_value_dmg(self): # This is a DMG% buff, not ATK
        return (0.07, 0.09, 0.11, 0.13, 0.15, 0.17, 0.19, 0.21, 0.23, 0.25, 0.27, 0.29, 0.31)[self.fields[1][3]-1]*((150+max(self.fields[0][3], 250)) if self.fields[2][3] else (self.fields[0][3]))
       
    def buff(self, stats, hypercarry, weapon):
        stats['DMG'] = stats['DMG'] + self.buff_value_dmg()

class Char_kazuha(Char_buffer):
    '''Kaedahara Kazuha, master of VV. In addition to the shred provides an EM buff and swirled element DMG%.
    Default Kazuha is expected to have 800 EM and no C2.'''
    def __init__(self):
        super(Char_kazuha, self).__init__('Kaedehara Kazuha', 'Anemo')
        self.fields = (
            ['Elemental mastery', 'int', (0, 1999), 800],
            ['Is C2', 'bool', None, False],
            ['Holds 4p Viridescent Venerer', 'bool', None, True]
        )

    def is_relevant(self, hypercarry):
        return 'EM' in hypercarry.scales_with or hypercarry.element in ('Pyro', 'Hydro', 'Electro', 'Cryo')
        
    def buff_value_dmg(self, stats):
        return 0.04*(self.fields[0][3] + (200 if self.fields[1][3] else 0) + (75 if stats['elements_in_party'].count('Dendro') >= 2 else 0))

    def buff(self, stats, hypercarry, weapon):
        if self.fields[1][3]: stats['EM'] = stats['EM'] + 200
        if hypercarry.element in ('Pyro', 'Hydro', 'Electro', 'Cryo'):
            stats['DMG'] = stats['DMG'] + self.buff_value_dmg(stats)
            if self.fields[2][3]: stats['shred_vv'] = 40
    
class Char_chevreuse(Char_buffer):
    '''Chevreuse, the glue of Electro-Pyro teams, providing a VV-like effect and some DMG% to them and only them.
    Default Chevreuse is assumed to have 35k hp, and have 0 C6 stacks active.'''
    def __init__(self):
        super(Char_chevreuse, self).__init__('Chevreuse', 'Pyro')
        self.fields = (
            ['HP', 'int', (1, 40000), 35000],
            ['C6 stacks', 'int', (0, 3), 0]
        )
        
    def is_relevant(self, hypercarry):
        return hypercarry.element in ('Pyro', 'Electro')
        
    def buff_value_dmg(self):
        return 0.001*self.fields[0][3] + 20*self.fields[1][3]
    
    def buff(self, stats, hypercarry, weapon):
        '''!! UNFINISHED !! Chevreuse instance cannot know if there is a Hydro resonance'''
        if set(stats['elements_in_party']) == set(('Pyro', 'Electro')):
            stats['DMG'] = stats['DMG'] + self.buff_value_dmg()
            stats['shred_chevreuse'] = 40

class Char_zhongli(Char_buffer):
    '''Zhongli, Morax, Rex Lapis, the Shield Archon. The shield has minor shred and can trigger ToM consistently.
    Default Zhongli provides his shield and holds 4p Tenacity of the Millelith'''
    def __init__(self):
        super(Char_zhongli, self).__init__('Zhongli', 'Geo')
        self.fields = (
            ['Holds 4p Tenacity of the Millelith', 'bool', None, True],
        )
  
    def is_relevant(self, hypercarry):
        return True
        
    def buff(self, stats, hypercarry, weapon):
        stats['ATK'] = stats['ATK'] + (0.2*hypercarry.base_atk(weapon) if self.fields[0][3] else 0)
        stats['shred_zhongli'] = 20
    
class Char_gorou(Char_buffer):
    '''Gorou, Itto's best friend. Provides a DEF buff, minor Geo DMG% and can give some Crit DMG.
    Default Gorou is assumed to have talent level of 8, no C6, and no 4p Noblesse Obligue'''
    def __init__(self):
        super(Char_gorou, self).__init__('Gorou', 'Geo')
        self.fields = (
            ['Talent level', 'int', (1, 13), 8],
            ['Is C6', 'bool', None, False],
            ['Holds 4p Noblesse Obligue', 'bool', None, True]
        )
    
    def is_relevant(self, hypercarry):
        return 'DEF' in hypercarry.scales_with or (('DMG' or 'CV') in hypercarry.scales_with and hypercarry.element == 'Geo')
        
    def buff_value_def(self):
        return (206.16, 221.62, 237.08, 257.7, 273.16, 288.62, 309.24, 329.85, 350.47, 371.08, 391.70, 412.32, 438.09)[self.fields[0][3]-1]
    
    def buff(self, stats, hypercarry, weapon):
        stats['ATK'] = stats['ATK'] + (0.2*hypercarry.base_atk(weapon) if self.fields[2][3] else 0)
        stats['DEF'] = stats['DEF'] + self.buff_value_def() + 0.25*hypercarry.base_stats['DEF']
        stats['DMG'] = stats['DMG'] + (15 if stats['elements_in_party'].count('Geo') >= 3 and hypercarry.element == 'Geo' else 0)
        stats['CV'] = stats['CV'] + (40 if self.fields[1][3] == True and hypercarry.element == 'Geo' else 0)

BUFFER_TYPES = {
    'None': Char_placeholder,
    'Bennett': Char_bennett,
    'Kujou Sara': Char_sara,
    'Furina': Char_furina,
    'Kaedehara Kazuha': Char_kazuha,
    'Chevreuse': Char_chevreuse,
    'Zhongli': Char_zhongli,
    'Gorou': Char_gorou,
    'VV provider': Char_vv,
    'Resonance provider': Char_placeholder
}