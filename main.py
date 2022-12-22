import sys
import time

from PyQt5 import QtCore, QtGui, QtWidgets

from ui.register_window import Register_Window


class PyQT_Register(QtWidgets.QWidget, Register_Window):
    def __init__(self):
        super(PyQT_Register, self).__init__()
        self.setupUi(self)



if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    register_window = PyQT_Register()
    register_window.show()
    sys.exit(app.exec_())


