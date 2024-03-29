from PyQt5 import QtWidgets
from giho_utility import *
from giho_hypercarries import HC_TYPES
from giho_buffers import BUFFER_TYPES
from giho_ui_widgets import *
from giho_ui_optimizers import *

class Widget_genshin_buff_opt_main(QtWidgets.QWidget):
    def __init__(self):
        super(Widget_genshin_buff_opt_main, self).__init__()
        # Alternative, no-preload way to pick enabled hypercarries and buffers - by names
        self.hc_widgets = dict()
        for item in HC_TYPES.keys(): self.hc_widgets[item] = Widget_char_placeholder()
        # These arcane runes mean 'get first key and value from a dictionary' because even ordered since 3.7, they don't support indexing
        self.hc_widgets[tuple(HC_TYPES.keys())[0]] = Widget_hypercarry(tuple(HC_TYPES.values())[0])
        self.buffer_widgets = dict()
        for item in BUFFER_TYPES.keys(): self.buffer_widgets[item] = Widget_char_placeholder()
        buffer_names = tuple(BUFFER_TYPES.keys())
        self.placeholder_buffer_widgets = (Widget_char_placeholder(), Widget_char_placeholder(), Widget_char_placeholder()) # These are for the fields, not for preloads
        self.enemy_res = 10
        #
        layout_main = QtWidgets.QVBoxLayout(self)
        # Hypercarry
        layout_hc_s = QtWidgets.QHBoxLayout()
        label_hc = QtWidgets.QLabel('Hypercarry:', self)
        self.box_hc = make_combo_box(self, tuple(self.hc_widgets.keys()), tuple(HC_TYPES.keys())[0], self.switch_hypercarry)
        label_res = QtWidgets.QLabel('Enemy elemental resistance:', self)
        self.box_res = make_spin_box(self, (-100, 999), self.enemy_res, self.update_enemy_res)
        for item in (label_hc, self.box_hc, label_res, self.box_res): layout_hc_s.addWidget(item)
        layout_hc_s.addSpacerItem(QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        self.layout_hc = QtWidgets.QStackedLayout()
        for item in self.hc_widgets.values(): self.layout_hc.addWidget(item) # Populate with the default and placeholder widgets to avoid preloading hypercarries
        frame_hc = make_basic_frame(self.layout_hc)
        # Buffers
        self.layouts_buffers = (QtWidgets.QVBoxLayout(), QtWidgets.QVBoxLayout(), QtWidgets.QVBoxLayout()) # I need to keep those named to be able to reference them to switch out buffers
        self.boxes_buffers = (QtWidgets.QComboBox(self), QtWidgets.QComboBox(self), QtWidgets.QComboBox(self))
        for i in range(3):
            layout_buffer = QtWidgets.QHBoxLayout()
            label_buffer = QtWidgets.QLabel('Buffer ' + str(i+1) + ':', self)
            self.boxes_buffers[i].addItems(buffer_names)
            self.boxes_buffers[i].activated.connect(self.switch_buffers)
            layout_buffer.addWidget(label_buffer)
            layout_buffer.addWidget(self.boxes_buffers[i])
            layout_buffer.addSpacerItem(QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
            self.layouts_buffers[i].addLayout(layout_buffer)
            self.layouts_buffers[i].addWidget(self.placeholder_buffer_widgets[i])
            self.layouts_buffers[i].addSpacerItem(QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
            del label_buffer
            del layout_buffer
        # Buttons
        layout_buttons = QtWidgets.QVBoxLayout()
        button_calculate = QtWidgets.QPushButton('Calculate damage output for the current setup', self)
        button_calculate.clicked.connect(self.calculate_setup)
        self.label_calc_result = QtWidgets.QLabel('Current configuration output is:', self)
        self.label_stats_result = QtWidgets.QLabel('Effective stats:', self)
        layout_buttons.addWidget(button_calculate)
        layout_buttons.addWidget(self.label_calc_result)
        layout_buttons.addWidget(self.label_stats_result)
        # Optimizers
        layout_opt_s = QtWidgets.QHBoxLayout()
        self.button_opt_build = QtWidgets.QPushButton('Build', self)
        self.button_opt_build.clicked.connect(self.switch_optimizer)
        self.button_opt_buffers = QtWidgets.QPushButton('Buffers', self)
        self.button_opt_buffers.clicked.connect(self.switch_optimizer)
        layout_opt_s.addWidget(self.button_opt_build)
        layout_opt_s.addWidget(self.button_opt_buffers)
        layout_opt_s.addSpacerItem(QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        widget_opt_build = Widget_optimize_build(self.box_res, self.layout_hc, self.layouts_buffers)
        widget_opt_buffers = Widget_optimize_buffers(self.box_res, self.layout_hc, self.get_buffer_widget)
        self.layout_optimizers = QtWidgets.QStackedLayout()
        for item in (widget_opt_build, widget_opt_buffers): self.layout_optimizers.addWidget(item)
        frame_opt = make_basic_frame(self.layout_optimizers)
        #
        for item in (layout_hc_s, frame_hc, self.layouts_buffers[0], self.layouts_buffers[1], self.layouts_buffers[2], layout_buttons, layout_opt_s, frame_opt):
            if type(item) in (QtWidgets.QHBoxLayout, QtWidgets.QVBoxLayout, QtWidgets.QGridLayout, QtWidgets.QStackedLayout): layout_main.addLayout(item)
            else: layout_main.addWidget(item)
        layout_main.addSpacerItem(QtWidgets.QSpacerItem(750, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
        
    # Note: 'hypercarry' and 'buffer' may be used interchangeably as name strings or character objects in different functions, pay attention
        
    def update_enemy_res(self):
        self.enemy_res = float(self.box_res.text())
    
    def get_hc_widget(self, hc_name):
        # Check if this hypercarry widget has already been made, make it and insert it into the hypercarry QStackedLayout if not, return it
        if self.hc_widgets[hc_name].character.name == 'None':
            old_w = self.hc_widgets[hc_name]
            self.hc_widgets[hc_name] = Widget_hypercarry(HC_TYPES[hc_name])
            self.layout_hc.replaceWidget(old_w, self.hc_widgets[hc_name])
            old_w.deleteLater()
            old_w = None
        return self.hc_widgets[hc_name]

    def switch_hypercarry(self):
        hc_name = self.box_hc.currentText()
        if hc_name != self.layout_hc.currentWidget().character.name: # Checking that the user actually picked someone new
            self.get_hc_widget(hc_name)
            self.layout_hc.setCurrentIndex(tuple(self.hc_widgets.keys()).index(hc_name))
    
    def get_buffer_widget(self, buffer_name):
        # If the buffer in question is a resonator, just make a new one
        if 'Resonator:' in buffer_name: return Widget_resonator(buffer_name.replace('Resonator: ', ''))
        # Check if this buffer widget has already been made, make it if not, return it if yes
        if self.buffer_widgets[buffer_name].character.name == 'None':
            self.buffer_widgets[buffer_name] = Widget_buffer(BUFFER_TYPES[buffer_name])
        return self.buffer_widgets[buffer_name]
        
    def switch_buffers(self):
        num_changed = self.boxes_buffers.index(self.sender()) # Looks stupid, but apparently it's not possible to send an argument with a connect() without anonymous functions
        buffer_names = (self.boxes_buffers[0].currentText(), self.boxes_buffers[1].currentText(), self.boxes_buffers[2].currentText())
        # I can't figure out a way to selectively disable and reenable elements in a QComboBox at my current Qt level, so here's a workaround
        # You selected the same buffer twice? Change nothing, reset selection in the box you just tried to change to what it was
        if buffer_names.count(buffer_names[num_changed]) > 1 and buffer_names[num_changed] not in ('None', 'Resonance provider'):
            previous_buffer_name = (self.layouts_buffers[num_changed]).itemAt(1).widget().character.name
            (self.boxes_buffers[num_changed]).setCurrentText(previous_buffer_name)
        elif buffer_names[num_changed] != (self.layouts_buffers[num_changed]).itemAt(1).widget().character.name:
            # Now, I need to replace whichever buffer widget happens to currently be in the slot with the new one - if the new one is a new one
            old_w = (self.layouts_buffers[num_changed]).itemAt(1).widget()
            if buffer_names[num_changed] == 'None':
                new_w = self.placeholder_buffer_widgets[num_changed] # Getting the correct buffer 'None' placeholder widget for this buffer slot
            elif buffer_names[num_changed] == 'Resonance provider': # Resonator character.name depends on their element, but here it is just the box text
                new_w = Widget_resonator() # Make a new one since we don't need to keep track of them at all
            else:
                new_w = self.get_buffer_widget(buffer_names[num_changed])
            old_w.hide()
            (self.layouts_buffers[num_changed]).replaceWidget(old_w, new_w) # Resonator widget should be lost now. I can delete it explicitly too I think, but there's no need
            new_w.show()
            
    # Note: resonator widgets and buffer slot placeholder widgets are processed separately even though their functionality is the same - we don't need to keep track of them beyond there being enough
    # It would be slicker to handle both like the resonator, but I'll leave it as-is as a showcase

    def switch_optimizer(self):
        opt_index = (self.button_opt_build, self.button_opt_buffers).index(self.sender())
        self.layout_optimizers.setCurrentIndex(opt_index)

    def get_current_buffers(self):
        # Return a tuple of currently selected widget_buffer.character's
        # These arcane runes send the character objects placed within the widgets put in the frames by buffer selectors to the hypercarry object. If there is no buffer, the placeholder sends a 'None'
        return (self.layouts_buffers[0].itemAt(1).widget().character, self.layouts_buffers[1].itemAt(1).widget().character, self.layouts_buffers[2].itemAt(1).widget().character)

    def calculate_setup(self):
        output, stats = calculate_output(self.enemy_res, self.layout_hc.currentWidget().character, buffers = self.get_current_buffers())
        self.label_calc_result.setText('Current configuration output is: ' + "{:.1f}".format(output))
        stats_formatted = format_stats(stats)
        self.label_stats_result.setText('Effective stats: ' + stats_formatted)