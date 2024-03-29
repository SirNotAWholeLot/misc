# To adapt Qt4 code: QtGui -> QtWidgets
from PyQt5 import QtWidgets, QtCore
from giho_ui_main import Widget_genshin_buff_opt_main

class This_main_window(QtWidgets.QMainWindow):
    def __init__(self):
        super(This_main_window, self).__init__()
        main_widget = Widget_genshin_buff_opt_main()
        self.setCentralWidget(main_widget)
        self.setWindowTitle("GI Hypercarry Optimizer")
        self.setGeometry(50, 100, 750, 600)    
    
if __name__ == '__main__':
    import sys
    # Modified version of the runner code for Jupyter compatibility - might work outside it too
    app = QtCore.QCoreApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
    window = This_main_window()
    window.show()
    app.exec_()
    del app
# End of __main__ section