from PyQt5 import QtWidgets

class Char_placeholder():
    def __init__(self, name='None', element='None'):
        self.name = name
        self.element = element
        
class Widget_char_placeholder(QtWidgets.QWidget):
    def __init__(self, char_type=Char_placeholder):
        super(Widget_char_placeholder, self).__init__()
        self.character = char_type()
        
def make_basic_frame(layout):
    frame = QtWidgets.QFrame()
    frame.setLayout(layout)
    frame.setFrameStyle(QtWidgets.QFrame.StyledPanel)
    frame.setLineWidth(3)
    return frame

def make_check_box(caller, options, default_v, c_func=None):
    box = QtWidgets.QCheckBox(options, caller)
    box.setChecked(default_v)
    if c_func: box.stateChanged.connect(c_func)
    return box

def make_combo_box(caller, options, default_v, c_func=None):
    box = QtWidgets.QComboBox(caller)
    box.addItems(options)
    box.setCurrentText(default_v)
    if c_func: box.activated.connect(c_func)
    return box
        
def make_spin_box(caller, options, default_v, c_func=None):
    box = QtWidgets.QSpinBox(caller)
    box.setMinimum(options[0])
    box.setMaximum(options[1])
    box.setValue(default_v)
    if c_func: box.valueChanged.connect(c_func)
    return box

def make_double_spin_box(caller, options, default_v, c_func=None):
    box = QtWidgets.QDoubleSpinBox(caller)
    box.setMinimum(options[0])
    box.setMaximum(options[1])
    box.setValue(default_v)
    if c_func: box.valueChanged.connect(c_func)
    return box

def make_bold_label(caller, options, default_v, c_func=None):
    box = QtWidgets.QLabel(default_v, caller)
    box.setStyleSheet("font-weight: bold")
    return box

def make_labled_box(caller, name, type, options, default_v, c_func=None):
    label = QtWidgets.QLabel(name + ':' if name != '-' and type != 'text' else name, caller) if name != None else None
    box = {'bool': make_check_box, 'str': make_combo_box, 'int': make_spin_box, 'double': make_double_spin_box, 'bold': make_bold_label}[type](caller, options, default_v, c_func) if type != 'text' else None
    return {'label': label, 'box': box}