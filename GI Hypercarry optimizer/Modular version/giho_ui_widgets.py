from PyQt5 import QtWidgets
from giho_utility import *
from giho_base_classes import *
from giho_hypercarries import Char_hypercarry_custom
from giho_weapons import Weapon_custom

class Widget_hypercarry(Widget_char_placeholder):
    def __init__(self, char_type = Char_hypercarry):
        super(Widget_hypercarry, self).__init__(char_type)
        layout_main = QtWidgets.QVBoxLayout(self)
        # Base stats
        label_stats_base = QtWidgets.QLabel('Base stats:', self)
        layout_stats_base = QtWidgets.QHBoxLayout()
        if char_type != Char_hypercarry_custom: # Static stats for existing characters
            self.widgets_stats_base = []
            self.widgets_stats_base.append(make_labled_box(self, 'Element', 'bold', None, self.character.element))
            for attr in ('HP', 'ATK', 'DEF'):
                if attr in self.character.scales_with: self.widgets_stats_base.append(make_labled_box(self, attr, 'bold', None, str(self.character.base_stats[attr])))
            self.widgets_stats_base.append(make_labled_box(self, 'Ascension stat', 'bold', None, self.character.base_stats['asc_stat']
                                                            + ('' if self.character.base_stats['asc_stat'] == 'None' else '  -')))
            self.widgets_stats_base.append(make_labled_box(self, None, 'bold', None, ('' if self.character.base_stats['asc_stat'] == 'None'
                                                      else str(self.character.base_stats['asc_value']) + ('%' if self.character.base_stats['asc_stat'] != 'CV' else '')) ))
            for item in self.widgets_stats_base:
                if item['label'] != None: layout_stats_base.addWidget(item['label'])
                if item['box'] != None: layout_stats_base.addWidget(item['box'])
        else: # Editable stats for abstract hypercarry
            self.widgets_stats_base = []
            self.stats_base_types = (
                ['Element', 'str', ('Physical', 'Anemo', 'Pyro', 'Hydro', 'Electro', 'Cryo', 'Geo', 'Dendro'), self.character.element],
                ['HP', 'int', (1, 50000), self.character.base_stats['HP']],
                ['ATK', 'int', (1, 1000), self.character.base_stats['ATK']],
                ['DEF', 'int', (1, 2000), self.character.base_stats['DEF']],
                ['Ascension stat', 'str', ['None'] + list(self.character.scales_with), self.character.base_stats['asc_stat']],
                ['-', 'double', (0, 1000), self.character.base_stats['asc_value']]
            )
            for item in self.stats_base_types: self.widgets_stats_base.append(make_labled_box(self, *item, self.update_char_base))
            for item in self.widgets_stats_base:
                if item['label'] != None: layout_stats_base.addWidget(item['label'])
                if item['box'] != None: layout_stats_base.addWidget(item['box'])
        layout_stats_base.addSpacerItem(QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        # Weapon
        layout_label_weapon = QtWidgets.QHBoxLayout()
        label_weapon = QtWidgets.QLabel('Weapon:', self)
        self.box_weapon = make_combo_box(self, tuple(self.character.weapon_types.keys()), self.character.weapon.name, self.update_weapon)
        layout_label_weapon.addWidget(label_weapon)
        layout_label_weapon.addWidget(self.box_weapon)
        layout_label_weapon.addSpacerItem(QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        self.layout_weapon = QtWidgets.QStackedLayout()
        for item in self.character.weapon_types.values(): self.layout_weapon.addWidget(Widget_weapon(item))
        self.layout_weapon.setCurrentIndex(tuple(self.character.weapon_types.keys()).index(self.character.weapon.name))
        frame_weapon = make_basic_frame(self.layout_weapon)
        # Artifacts
        label_artifacts = QtWidgets.QLabel('Artifacts: types by main stat', self)
        layout_artifacts = QtWidgets.QHBoxLayout()
        widgets_to_add = []
        self.boxes_artifacts = {}
        for slot in ('Sands', 'Goblet', 'Circlet'):
            widgets_to_add.append(make_labled_box(self, slot, 'str', self.character.artifact_types[slot], self.character.artifacts[slot], self.update_equipment))
            self.boxes_artifacts.update({slot: widgets_to_add[-1]['box']})
        for item in widgets_to_add:
            layout_artifacts.addWidget(item['label'])
            layout_artifacts.addWidget(item['box'])            
        layout_artifacts.addSpacerItem(QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        # Extra stats
        label_stats_extra = QtWidgets.QLabel('Extra stats: artifact substats, set bonuses', self)
        layout_stats_extra = QtWidgets.QHBoxLayout()
        widgets_to_add = []
        self.boxes_extra = {}
        for stat in self.character.scales_with:
            if stat in ('HP', 'ATK', 'DEF'): # Cannot be really optimized with make_labled_box because of the grid layouts, I can save a couple lines at best
                layout_stat = QtWidgets.QGridLayout()
                label_stat_flat = QtWidgets.QLabel('Flat ' + stat + ':', self)
                self.boxes_extra[stat + '_flat'] = make_spin_box(self, (0, 9999), self.character.extra_stats[stat + '_flat'], self.update_equipment)
                label_stat_perc = QtWidgets.QLabel(stat + '%:', self)
                self.boxes_extra[stat + '_perc'] = make_double_spin_box(self, (0, 999), self.character.extra_stats[stat + '_perc'], self.update_equipment)
                layout_stat.addWidget(label_stat_flat, 0, 0)
                layout_stat.addWidget(label_stat_perc, 1, 0)
                layout_stat.addWidget(self.boxes_extra[stat + '_flat'], 0, 1)
                layout_stat.addWidget(self.boxes_extra[stat + '_perc'], 1, 1)
                widgets_to_add = widgets_to_add + [layout_stat]
                del layout_stat # Clearing references, the elements themselves are already attached to something and as such won't be deleted
                del label_stat_flat
                del label_stat_perc
            elif stat == 'EM': # EM is an integer unlke all other single-number stats
                label_stat = QtWidgets.QLabel(stat + ':', self)
                self.boxes_extra[stat] = make_spin_box(self, (0, 999), self.character.extra_stats[stat], self.update_equipment)
                widgets_to_add = widgets_to_add + [label_stat, self.boxes_extra[stat]]
                del label_stat
            else:
                label_stat = QtWidgets.QLabel(stat + ':', self)
                self.boxes_extra[stat] = make_double_spin_box(self, (0, 999), self.character.extra_stats[stat], self.update_equipment)
                widgets_to_add = widgets_to_add + [label_stat, self.boxes_extra[stat]]
                del label_stat
        for item in widgets_to_add:
            if type(item) in (QtWidgets.QHBoxLayout, QtWidgets.QVBoxLayout, QtWidgets.QGridLayout, QtWidgets.QStackedLayout): layout_stats_extra.addLayout(item)
            else: layout_stats_extra.addWidget(item)
        layout_stats_extra.addSpacerItem(QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        # Character-specific fields
        layout_char_fields = QtWidgets.QHBoxLayout()
        self.widgets_fields = []
        for item in self.character.fields:
            self.widgets_fields.append(make_labled_box(self, *item, self.update_char_fields))
        for item in self.widgets_fields: 
            if item['label'] != None: layout_char_fields.addWidget(item['label'])
            if item['box'] != None: layout_char_fields.addWidget(item['box'])
        layout_char_fields.addSpacerItem(QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        #
        for item in (label_stats_base, layout_stats_base, layout_label_weapon, frame_weapon, label_artifacts, layout_artifacts, label_stats_extra, layout_stats_extra, layout_char_fields):
            if type(item) in (QtWidgets.QHBoxLayout, QtWidgets.QVBoxLayout, QtWidgets.QGridLayout, QtWidgets.QStackedLayout): layout_main.addLayout(item)
            else: layout_main.addWidget(item)
        layout_main.addSpacerItem(QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))

    def update_char_base(self): # This function refers to attributes that only exist for abstract hypercarry, but should only be called by an abstract hypercarry
        self.character.element = self.widgets_stats_base[0]['box'].currentText()
        if 'HP' in self.character.scales_with: self.character.base_stats['HP'] = self.widgets_stats_base[1]['box'].value()
        if 'ATK' in self.character.scales_with: self.character.base_stats['ATK'] = self.widgets_stats_base[2]['box'].value()
        if 'DEF' in self.character.scales_with: self.character.base_stats['DEF'] = self.widgets_stats_base[3]['box'].value()
        self.character.base_stats['asc_stat'] = self.widgets_stats_base[4]['box'].currentText()
        self.character.base_stats['asc_value'] = self.widgets_stats_base[5]['box'].value()

    def update_weapon(self):
        weapon_name = self.box_weapon.currentText()
        if weapon_name != self.character.weapon.name:
            self.layout_weapon.setCurrentIndex(tuple(self.character.weapon_types.keys()).index(weapon_name))
            self.character.weapon = self.layout_weapon.currentWidget().weapon
            # Theoretically, any calculation character does with the weapon can be handled by character object asking it's parent widget
        
    def update_equipment(self):
        for stat in self.character.scales_with:
            if stat in ('HP', 'ATK', 'DEF'):
                self.character.extra_stats[stat + '_flat'] = self.boxes_extra[stat + '_flat'].value()
                self.character.extra_stats[stat + '_perc'] = self.boxes_extra[stat + '_perc'].value()
            else:
                self.character.extra_stats[stat] = self.boxes_extra[stat].value()
        for slot in ('Sands', 'Goblet', 'Circlet'):
            self.character.artifacts[slot] = self.boxes_artifacts[slot].currentText()

    def update_char_fields(self):
        for item, widget in zip(self.character.fields, self.widgets_fields):
            item[3] = getattr(widget['box'], {'bool': 'isChecked', 'str': 'currentText', 'int': 'value', 'double': 'value'}[item[1]])()

class Widget_weapon(QtWidgets.QWidget):
    def __init__(self, weapon):
        super(Widget_weapon, self).__init__()
        self.weapon = weapon
        self.custom_weapon = (isinstance(weapon, Weapon_custom))
        #
        layout_main = QtWidgets.QVBoxLayout(self)
        layout_1 = QtWidgets.QHBoxLayout()
        if self.custom_weapon:
            fields = (
                ['ATK', 'int', (1, 1999), self.weapon.atk[0]],
                ['Ascension stat', 'str', ['None'] + list(weapon.holder.scales_with), self.weapon.asc['stat']],
                ['-', 'double', (0, 999), self.weapon.asc[self.weapon.level]],
                [('' if self.weapon.asc['stat'] == 'None' else str(self.weapon.asc[self.level]) + ('%' if self.weapon.asc['stat'] not in ('EM', 'CV') else '')), 'text', None, None]
            )
        else:
            fields = (
                ['Level', 'str', ('70/70', '80/80', '90/90'), self.weapon.level],
                ['Refinement', 'int', (1, 5), self.weapon.refine],
                ['ATK', 'bold', None, str(self.weapon.atk[self.weapon.level])],
                ['Ascension stat', 'bold', None, self.weapon.asc['stat']],
                ['-', 'bold', None, ('' if self.weapon.asc['stat'] == 'None' else str(self.weapon.asc[self.weapon.level]) + ('%' if self.weapon.asc['stat'] not in ('EM', 'CV') else ''))]
            )
        self.widgets_stats_base = []
        for item in fields:
            self.widgets_stats_base.append(make_labled_box(self, *item, self.update_weapon))
        for item in self.widgets_stats_base:
                if item['label'] != None: layout_1.addWidget(item['label'])
                if item['box'] != None: layout_1.addWidget(item['box'])
        layout_1.addSpacerItem(QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        #
        layout_2 = QtWidgets.QHBoxLayout()
        label_psv = QtWidgets.QLabel('Passive:', self)
        widgets_to_add = [label_psv]
        if self.weapon.psv['type'] == 'bool':
            self.widget_psv = make_check_box(self, '', self.weapon.psv['active'], self.update_weapon)
            widgets_to_add = widgets_to_add + [self.widget_psv]
        elif self.weapon.psv['type'] == 'stacks':
            self.widget_psv = make_spin_box(self, (self.weapon.psv['range'][0], self.weapon.psv['range'][1]), self.weapon.psv['active'], self.update_weapon)
            label_passive_extra = QtWidgets.QLabel('stacks', self)
            widgets_to_add = widgets_to_add + [self.widget_psv, label_passive_extra]
        elif self.weapon.psv['type'] == 'perc':
            self.widget_psv = make_double_spin_box(self, (self.weapon.psv['range'][0], self.weapon.psv['range'][1]), self.weapon.psv['active'], self.update_weapon)
            label_passive_extra = QtWidgets.QLabel('% effective', self)
            widgets_to_add = widgets_to_add + [self.widget_psv, label_passive_extra]
        else:
            label_passive_extra = QtWidgets.QLabel(self.weapon.psv['type'], self)
            widgets_to_add = widgets_to_add + [label_passive_extra]
        for item in widgets_to_add: layout_2.addWidget(item)
        layout_2.addSpacerItem(QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        #
        layout_main.addLayout(layout_1)
        layout_main.addLayout(layout_2)
        layout_main.addSpacerItem(QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
        
    def update_weapon(self):
        if self.custom_weapon:
            self.weapon.atk[self.weapon.level] = self.widgets_stats_base[0]['box'].value()
            self.weapon.asc['stat'] = self.widgets_stats_base[1]['box'].currentText()
            self.weapon.asc[self.weapon.level] = self.widgets_stats_base[2]['box'].value()
        else:
            self.weapon.level = self.widgets_stats_base[0]['box'].currentText()
            self.weapon.refine = self.widgets_stats_base[1]['box'].value()
            self.widgets_stats_base[2]['box'].setText(str(self.weapon.atk[self.weapon.level]))
            self.widgets_stats_base[3]['box'].setText(('' if self.weapon.asc['stat'] == 'None' else str(self.weapon.asc[self.weapon.level])
                                                        + ('%' if self.weapon.asc['stat'] not in ('EM', 'CV') else '')))
            if self.weapon.psv['type'] == 'bool':
                self.weapon.psv['active'] = self.widget_psv.isChecked()
            elif self.weapon.psv['type'] == 'stacks':
                self.weapon.psv['active'] = self.widget_psv.value()
            elif self.weapon.psv['type'] == 'perc':
                self.weapon.psv['active'] = self.widget_psv.value()
            else:
                return            

class Widget_buffer(Widget_char_placeholder):
    def __init__(self, char_type=Char_buffer):
        super(Widget_buffer, self).__init__(char_type)
        layout = QtWidgets.QHBoxLayout(self)
        self.widgets_fields = []
        for item in self.character.fields:
            self.widgets_fields.append(make_labled_box(self, *item, self.update_fields))
        for item in self.widgets_fields: 
            if item['label'] != None: layout.addWidget(item['label'])
            if item['box'] != None: layout.addWidget(item['box'])
        layout.addSpacerItem(QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
            
    def update_fields(self):
        for item, widget in zip(self.character.fields, self.widgets_fields):
            if item[1] not in ['text', 'bold']: item[3] = getattr(widget['box'], {'bool': 'isChecked', 'str': 'currentText', 'int': 'value', 'double': 'value'}[item[1]])()

class Widget_resonator(Widget_char_placeholder):
    def __init__(self, element = 'Physical'):
        super(Widget_resonator, self).__init__(Char_buffer)
        self.character.name = 'Resonator: ' + element
        #
        label_element = QtWidgets.QLabel('Element:', self)
        self.box_element = make_combo_box(self, ('Physical', 'Anemo', 'Pyro', 'Hydro', 'Electro', 'Cryo', 'Geo', 'Dendro'), self.character.element, self.update_char)
        #
        layout = QtWidgets.QHBoxLayout(self)
        for item in (label_element, self.box_element): layout.addWidget(item)
        layout.addSpacerItem(QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        
    def update_char(self):
        self.character.element = self.box_element.currentText()
        self.character.name = 'Resonator: ' + self.character.element