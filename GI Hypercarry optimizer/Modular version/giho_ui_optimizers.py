from PyQt5 import QtWidgets
from itertools import product, combinations
from giho_utility import *
from giho_calculators import *
from giho_buffers import BUFFER_TYPES

class Widget_optimize_build(QtWidgets.QWidget):
    '''Optimizer of the hypercarry build with a given set of buffers - artifact main stats, artifact sets, weapon selection.'''
    def __init__(self, res_container, hc_container, buffers_container):
        super(Widget_optimize_build, self).__init__()
        self.res_container = res_container
        self.hc_container = hc_container # Giving the optimizer containers from the main widget so they can get the current thing from them
        self.buffers_container = buffers_container
        #
        layout_main = QtWidgets.QVBoxLayout(self)
        layout_checks = QtWidgets.QHBoxLayout()
        self.box_opt_weapon = make_check_box(self, 'Weapon', True)
        self.box_opt_sands = make_check_box(self, 'Sands', True)
        self.box_opt_goblet = make_check_box(self, 'Goblet', True)
        self.box_opt_circlet = make_check_box(self, 'Circlet', True)
        for item in (self.box_opt_weapon, self.box_opt_sands, self.box_opt_goblet, self.box_opt_circlet): layout_checks.addWidget(item)
        layout_checks.addSpacerItem(QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        layout_main.addLayout(layout_checks)
        button_optimize = QtWidgets.QPushButton('Optimize', self)
        button_optimize.clicked.connect(self.optimize_build)
        self.label_result = QtWidgets.QLabel('Best configuration is:', self)
        for item in (button_optimize, self.label_result): layout_main.addWidget(item)
        layout_main.addSpacerItem(QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
        
    def optimize_build(self):
        '''Calculate output for weapon and artifact (main stats only) setup variations with the current buffer configuration'''
        hypercarry = self.hc_container.currentWidget().character
        buffers = (self.buffers_container[0].itemAt(1).widget().character, self.buffers_container[1].itemAt(1).widget().character, self.buffers_container[2].itemAt(1).widget().character)
        #
        if self.box_opt_weapon.isChecked(): weapon_types = list(hypercarry.weapon_types.keys())
        else: weapon_types = (hypercarry.weapon.name,)
        if self.box_opt_sands.isChecked(): sands_types = hypercarry.artifact_types['Sands']
        else: sands_types = (hypercarry.artifacts['Sands'],)
        if self.box_opt_goblet.isChecked(): goblet_types = hypercarry.artifact_types['Goblet']
        else: goblet_types = (hypercarry.artifacts['Goblet'],)
        if self.box_opt_circlet.isChecked(): circlet_types = hypercarry.artifact_types['Circlet']
        else: circlet_types = (hypercarry.artifacts['Circlet'],)
        outputs = list()
        for weapon, sands, goblet, circlet in product(weapon_types, sands_types, goblet_types, circlet_types):
            output, stats = calculate_output(self.res_container.value(), hypercarry, hypercarry.weapon_types[weapon], (sands, goblet, circlet), buffers)
            outputs.append([output, (weapon, sands, goblet, circlet)])
        best = max(outputs) # Should automatially give the pair with highest output number
        self.label_result.setText('Best configuration is: ' + str(best[1]) + " with the output of " + "{:.1f}".format(best[0]))
    
class Widget_optimize_buffers(QtWidgets.QWidget):
    '''Optimizer of the buffer selection for a given hypercarry build.'''
    def __init__(self, res_container, hc_container, get_buffer_widget):
        super(Widget_optimize_buffers, self).__init__()
        self.res_container = res_container
        self.hc_container = hc_container
        self.get_buffer_widget = get_buffer_widget
        #
        layout_main = QtWidgets.QVBoxLayout(self)
        layout_options = QtWidgets.QHBoxLayout()
        layout_num_buffers = QtWidgets.QVBoxLayout()
        label_num_buffers = QtWidgets.QLabel('Number of buffers:', self)
        self.box_num_buffers = make_spin_box(self, (1, 3), 1) # Doesn't need to be connected as we are only looking at it with methods
        layout_num_buffers.addWidget(label_num_buffers)
        layout_num_buffers.addWidget(self.box_num_buffers)
        layout_num_buffers.addSpacerItem(QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
        layout_available = QtWidgets.QVBoxLayout()
        container_available = QtWidgets.QWidget()
        container_available.setLayout(layout_available)
        self.boxes_available = dict()
        buffer_names = list(BUFFER_TYPES.keys())
        buffer_names.pop()
        buffer_names.pop(0)
        for name in buffer_names:
            self.boxes_available[name] = make_check_box(self, name, True)
            layout_available.addWidget(self.boxes_available[name])
        scroll_available = QtWidgets.QScrollArea()
        scroll_available.setWidget(container_available)
        scroll_available.setWidgetResizable(True)
        scroll_available.setFixedHeight(80)
        layout_options.addLayout(layout_num_buffers)
        layout_options.addWidget(scroll_available)
        button_optimize = QtWidgets.QPushButton('Optimize', self)
        button_optimize.clicked.connect(self.optimize_buffers)
        self.label_result = QtWidgets.QLabel('Best configuration is:', self)
        layout_main.addLayout(layout_options)
        for item in (button_optimize, self.label_result): layout_main.addWidget(item)
        layout_main.addSpacerItem(QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))

    def is_resonance_relevant(self, hypercarry, buffer_names, element):
        if element == 'Anemo' and False: return True # Resonance technically exists, but is never relevant
        if element == 'Pyro' and 'ATK' in hypercarry.scales_with: return True
        if element == 'Hydro' and 'HP' in hypercarry.scales_with: return True
        if element == 'Electro' and False: return True
        if element == 'Cryo' and 'CV' in hypercarry.scales_with: return True
        if element == 'Geo' and ('DMG' in hypercarry.scales_with or hypercarry.element == 'Geo'): return True
        if element == 'Dendro' and ('EM' in hypercarry.scales_with or 'Kaedehara Kazuha' in buffer_names): return True
        return False

    def optimize_buffers(self):
        '''Calculate output for buffers setup variations and update the result label with the best.'''
        # Ideally, the list of buffers should contain resonators relevant the HC's scalings, then buffers relevant to HC's scalings
        hypercarry = self.hc_container.currentWidget().character
        #
        buffer_names = list()
        for key, value in self.boxes_available.items():
            if value.isChecked() and self.get_buffer_widget(key).character.is_relevant(hypercarry): buffer_names.append(key)
        for element in ('Physical', 'Anemo', 'Pyro', 'Hydro', 'Electro', 'Cryo', 'Geo', 'Dendro'):
            if self.is_resonance_relevant(hypercarry, buffer_names, element):
                buffer_names.append('Resonator: ' + element)
                if hypercarry.element != element: buffer_names.append('Resonator: ' + element)
        outputs = list()
        for buffer_combo in combinations(buffer_names, self.box_num_buffers.value()):
            buffers = list()
            for name in buffer_combo:
                buffers.append(self.get_buffer_widget(name).character) # Combine by names, send character objects - I think this function is unavoidably main widget's because the buffers are stored there
            output, stats = calculate_output(self.res_container.value(), hypercarry, buffers = buffers)
            outputs.append([output, buffer_combo])
        if len(outputs) == 0: self.label_result.setText('No combinations available')            
        else:
            best = max(outputs)
            self.label_result.setText('Best buffers are: ' + str(best[1]) + " with the output of " + "{:.1f}".format(best[0]))