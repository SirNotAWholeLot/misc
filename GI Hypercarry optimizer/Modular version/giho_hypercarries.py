from giho_base_classes import Char_hypercarry
from giho_weapons import *

class Char_hypercarry_custom(Char_hypercarry):
    def __init__(self):
        super(Char_hypercarry_custom, self).__init__('Custom hypercarry', 'Physical', ('HP', 'ATK', 'DEF', 'EM', 'ER', 'DMG', 'CV'))
        self.weapon_types = {
            'Custom weapon': Weapon_custom(self) # As with all of these fields, overriding the dictionary containing Weapon_basic to simplify dependencies
        }
        self.weapon = self.weapon_types['Custom weapon']
        self.fields = (
            ['Custom hypercarry has no special optional properties', 'text', None, None],
        )

class Char_ayaka(Char_hypercarry):
    def __init__(self):
        super(Char_ayaka, self).__init__('Kamisato Ayaka', 'Cryo', ('ATK', 'DMG', 'CV'))
        # Default Ayaka is assumed to be lvl 90, holding a Amenoma Kageuchi and 4p Blizzard Strayer. C4 is currently not counted because it is finicky
        self.base_stats['HP'] = 12858
        self.base_stats['ATK'] = 342
        self.base_stats['DEF'] = 783
        self.base_stats['asc_stat'] = 'CV'
        self.base_stats['asc_value'] = 38.4
        self.weapon_types = {
            'Custom weapon': Weapon_custom(self),
            'Amenoma Kageuchi': Weapon_amenoma_kageuchi(self),
            'Finale of the Deep': Weapon_finale_of_the_deep(self),
            'Mistsplitter Reforged': Weapon_mistsplitter_reforged(self)
        }
        self.weapon = self.weapon_types['Amenoma Kageuchi']
        self.fields = (
            ['Blizzard Strayer', 'str', ('No 4p bonus', '4p Cryo', '4p Freeze'), '4p Freeze'],
        )

    def apply_self_buffs(self, stats):
        # Ayaka benefits from A1 (negligible so doesn't count) and A4, can benefit from 4p BS
        stats['DMG'] = stats['DMG'] + 18
        stats['CV'] = stats['CV'] + (40 if self.fields[0][3] == '4p Cryo' else 0) + (80 if self.fields[0][3] == '4p Freeze' else 0)
        return stats
    
class Char_hutao(Char_hypercarry):
    def __init__(self):
        super(Char_hutao, self).__init__('Hu Tao', 'Pyro', ('HP', 'ATK', 'DMG', 'CV'))
        # Default Hu Tao is assumed to be lvl 90, holding a 500 ATK weapon and 4p Crimson Witch of Flames, healthy. Constellations are currently not counted because they are finicky
        self.base_stats['HP'] = 15552
        self.base_stats['ATK'] = 106
        self.base_stats['DEF'] = 876
        self.base_stats['asc_stat'] = 'HP'
        self.base_stats['asc_value'] = 38.4
        self.weapon_types = {
            'Custom weapon': Weapon_custom(self)
        }
        self.weapon = self.weapon_types['Custom weapon']
        self.fields = (
            ['Talent level', 'int', (1, 13), 8],
            ['Under 50% health', 'bool', None, False],
            ['Artifact set bonus', 'str', ('No 4p set bonus', 'Crimson Witch of Flames', 'Shimenawa\'s Reminiscence'), 'Crimson Witch of Flames']
        )

    def apply_self_buffs(self, stats):
        # Hu Tao can benefit from A4, 4p CW and 4p SR
        stats['DMG'] = stats['DMG'] + (33 if self.fields[1][3] else 0) + (0, 15*0.5, 50)[self.fields[2][2].index(self.fields[2][3])]
        return stats

    def apply_conversions(self, stats):
        # Hu Tao converts max HP to ATK
        stats['ATK'] = stats['ATK'] + min(self.base_atk()*4, stats['HP']*((3.84, 4.07, 4.3, 4.6, 4.83, 5.06, 5.36, 5.66, 5.96, 6.26, 6.55, 6.85, 7.15)[self.fields[0][3]])/100)
        return stats
    
class Char_ei(Char_hypercarry):
    def __init__(self):
        super(Char_ei, self).__init__('Raiden Shogun', 'Electro', ('ATK', 'ER', 'DMG', 'CV'))
        # Default Ei is assumed to be lvl 90 holding The Catch R5 at lvl 90 and 4p Emblem of Severed Fate
        self.base_stats['HP'] = 12907
        self.base_stats['ATK'] = 337
        self.base_stats['DEF'] = 789
        self.base_stats['asc_stat'] = 'ER'
        self.base_stats['asc_value'] = 32
        self.weapon_types = {
            'Custom weapon': Weapon_custom(self),
            'The Catch': Weapon_the_catch(self),
            'Engulfing Lightning': Weapon_engulfing_lightning(self)
        }
        self.weapon = self.weapon_types['The Catch']
        self.weapon_types['The Catch'].psv['active'] = True # Since Ei uses burst in HC mode
        self.weapon_types['Engulfing Lightning'].psv['active'] = True
        self.fields = (
            ['Holds 4p Emblem of Severed Fate', 'bool', None, True],
        )
    
    def apply_conversions(self, stats):
        # Ei converts ER to DMG% with her A4, can benefit from 4p EosF
        stats['DMG'] = stats['DMG'] + 0.4*(stats['ER'] - 100) + (max(0.25*stats['ER'], 75) if self.fields[0][3] else 0)
        return stats
       
class Char_diluc(Char_hypercarry):
    def __init__(self):
        super(Char_diluc, self).__init__('Diluc', 'Pyro', ('ATK', 'DMG', 'CV'))
        # Default Diluc is assumed to be lvl 90 holding a 500 ATK weapon and 4p Crimson Witch of Flames. Constellations are currently not counted because they are finicky
        self.base_stats['HP'] = 12980
        self.base_stats['ATK'] = 334
        self.base_stats['DEF'] = 783
        self.base_stats['asc_stat'] = 'CV'
        self.base_stats['asc_value'] = 38.4
        self.weapon_types = {
            'Custom weapon': Weapon_custom(self),
            'Serpent Spine': Weapon_serpent_spine(self),
            'Redhorn Stonethresher': Weapon_redhorn_stonethresher(self)
        }
        self.weapon = self.weapon_types['Custom weapon']
        self.weapon_types['Serpent Spine'].psv['active'] = 5 # We can assume it is maxed if used properly
        self.weapon_types['Redhorn Stonethresher'].psv['active'] = 60 # Eyeballing for Diluc
        self.fields = (
            ['Holds 4p Crimson Witch', 'bool', None, True],
        )
    
    def apply_self_buffs(self, stats):
        # Diluc benefits from A4, and can benefit from 4p CW
        stats['DMG'] = stats['DMG'] + 20 + (15*1.5 if self.fields[0][3] else 0)
        return stats

class Char_itto(Char_hypercarry):
    def __init__(self):
        super(Char_itto, self).__init__('Arataki Itto', 'Geo', ('ATK', 'DEF', 'DMG', 'CV'))
        # Default Itto is assumed to be lvl 90 holding a 500 ATK weapon and 4p Husk of Opulent Dreams. Constellations are currently not counted because they are finicky
        self.base_stats['HP'] = 12858
        self.base_stats['ATK'] = 227
        self.base_stats['DEF'] = 959
        self.base_stats['asc_stat'] = 'CV'
        self.base_stats['asc_value'] = 38.4
        self.weapon_types = {
            'Custom weapon': Weapon_custom(self),
            'Serpent Spine': Weapon_serpent_spine(self),
            'Redhorn Stonethresher': Weapon_redhorn_stonethresher(self)
        }
        self.weapon_types['Serpent Spine'].psv['active'] = 5 # We can assume it is maxed if used properly
        self.weapon_types['Redhorn Stonethresher'].psv['active'] = 80 # Since Itto's damage mostly comes from normal/charged attacks
        self.fields = (
            ['Talent level', 'int', (1, 13), 8],
            ['Holds 4p Husk of Opulent Dreams', 'bool', None, True]
        )
    
    def apply_self_buffs(self, stats):
        # Itto benefits from A4 (a 35% extra DEF conversion for Kesagiri results in... 20% average?), and can benefit from 4p Husk, which he maxes out almost instantly
        stats['DEF'] = stats['DEF'] + (20 + (6*4 if self.fields[1][3] else 0))*self.base_stats['DEF']/100
        stats['DMG'] = stats['DMG'] + (6*4 if self.fields[1][3] else 0)
        return stats

    def apply_conversions(self, stats):
        # Itto converts DEF to ATK
        stats['ATK'] = stats['ATK'] + stats['DEF']*((57.6, 61.92, 66.24, 72, 76.32, 80.64, 86.4, 92.16, 97.92, 103.68, 109.44, 115.2, 122.4)[self.fields[0][3]])/100
        return stats

HC_TYPES = {
    'Basic hypercarry': Char_hypercarry,
    'Kamisato Ayaka': Char_ayaka,
    'Hu Tao': Char_hutao,
    'Raiden Shogun': Char_ei,
    'Diluc': Char_diluc,
    'Arataki Itto': Char_itto,
    'Custom hypercarry': Char_hypercarry_custom
}