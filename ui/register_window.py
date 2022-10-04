from PyQt5 import QtCore, QtGui, QtWidgets, Qt

from jd_utils.register_util import register
import pymysql

class Register_Window(object):
    def setupUi(self, register_window):
        register_window.setObjectName("register_window")
        register_window.setEnabled(True)
        register_window.resize(640, 254)
        self.formLayoutWidget = QtWidgets.QWidget(register_window)
        self.formLayoutWidget.setGeometry(QtCore.QRect(60, 60, 521, 51))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout_2 = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.formLayout_2.setObjectName("formLayout_2")
        self.id = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.id.setFont(font)
        self.id.setObjectName("id")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.id)
        self.MachineCode = QtWidgets.QLineEdit(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.MachineCode.setFont(font)
        self.MachineCode.setDragEnabled(False)
        self.MachineCode.setReadOnly(True)
        self.MachineCode.setObjectName("MachineCode")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.MachineCode)
        self.registerButton = QtWidgets.QPushButton(register_window)
        self.registerButton.setGeometry(QtCore.QRect(230, 140, 171, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.registerButton.setFont(font)
        self.registerButton.setObjectName("registerButton")
        # 绑定注册事件
        self.registerButton.clicked.connect(self.login)
        self.error = QtWidgets.QLabel(register_window)
        self.error.setGeometry(QtCore.QRect(60, 200, 521, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.error.setFont(font)
        self.error.setStyleSheet("color: rgb(255, 0, 0);")
        self.error.setAlignment(QtCore.Qt.AlignCenter)
        self.error.setObjectName("error")
        self.retranslateUi(register_window)
        QtCore.QMetaObject.connectSlotsByName(register_window)

    def retranslateUi(self, register_window):
        _translate = QtCore.QCoreApplication.translate
        register_window.setWindowTitle(_translate("register_window", "京东抢购软件-注册激活(Email：1024839103ly@gmail.com)"))
        self.id.setText(_translate("register_window", "注册码:"))
        self.registerButton.setText(_translate("register_window", "注册"))
        self.MachineCode.setText(register().getCombinNumber())



    #数据库校验
    def login(self):
        db = pymysql.connect(host='8.136.87.180', port=3306, user='jd_kill', passwd='jd_kill', db='jd_kill', charset='utf8')
        cursor = db.cursor()
        sql = " select * from account where MachineCode ='"+ self.MachineCode.text()+"' limit 1"
        cursor.execute(sql)
        data = cursor.fetchone()
        if data!=None:
            print("校验通过")
        else:
            db.close()
            self.error.setText("注册失败，请邮件联系：1024839103ly@gmail.com")