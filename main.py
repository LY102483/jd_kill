import sys

from PyQt5 import QtCore, QtGui, QtWidgets

from jd_utils.register_util import register
from ui.register_window import Register_Window


class PyQT_Register(QtWidgets.QWidget, Register_Window):
    def __init__(self):
        super(PyQT_Register, self).__init__()
        self.setupUi(self)



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    my_pyqt_form = PyQT_Register()
    my_pyqt_form.show()
    sys.exit(app.exec_())

