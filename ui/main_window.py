import datetime

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QWidget

import time
from selenium.webdriver.common.by import By

import utils.depend
# from utils.depend import chrome
from utils.cookieUtil import checkCookie, jobName, saveCookie, readCookie

# 主窗口
class Main_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(868, 376)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 341, 81))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.JdTime = QtWidgets.QLabel(self.gridLayoutWidget)
        self.JdTime.setStyleSheet("color:red")
        self.JdTime.setObjectName("JdTime")
        self.gridLayout_2.addWidget(self.JdTime, 1, 1, 1, 1)
        self.loginButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.loginButton.setStyleSheet("background-color: rgb(81, 142, 255);\n"
                                       "color: rgb(255, 255, 255);")
        self.loginButton.setObjectName("loginButton")
        self.gridLayout_2.addWidget(self.loginButton, 0, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 1, 0, 1, 1)
        self.timeButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.timeButton.setObjectName("timeButton")
        self.gridLayout_2.addWidget(self.timeButton, 1, 2, 1, 1)
        self.username = QtWidgets.QLabel(self.gridLayoutWidget)
        self.username.setStyleSheet("color:red")
        self.username.setObjectName("username")
        self.gridLayout_2.addWidget(self.username, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setMaximumSize(QtCore.QSize(108, 16777215))
        self.label.setStyleSheet("")
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.formLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 100, 341, 184))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.sku = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.sku.setObjectName("sku")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.sku)
        self.label_4 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.areaId = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.areaId.setToolTip("")
        self.areaId.setWhatsThis("")
        self.areaId.setObjectName("areaId")
        self.horizontalLayout_2.addWidget(self.areaId)
        self.formLayout.setLayout(1, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.label_5 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.address = QtWidgets.QTextEdit(self.formLayoutWidget)
        self.address.setMaximumSize(QtCore.QSize(16777215, 87))
        self.address.setReadOnly(True)
        self.address.setObjectName("address")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.address)
        self.label_6 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.buyTime = QtWidgets.QDateTimeEdit(self.formLayoutWidget)
        self.buyTime.setMinimumDateTime(QtCore.QDateTime(QtCore.QDate(1752, 9, 14), QtCore.QTime(0, 0, 1)))
        self.buyTime.setObjectName("buyTime")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.buyTime)
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 330, 341, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.refreshAddressButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.refreshAddressButton.setStyleSheet("background-color: rgb(81, 142, 255);\n"
                                                "color: rgb(255, 255, 255);")
        self.refreshAddressButton.setObjectName("refreshAddressButton")
        self.horizontalLayout.addWidget(self.refreshAddressButton)
        self.BuyOnTime = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.BuyOnTime.setStyleSheet("background-color: rgb(239,54,63);\n"
                                     "color:white;")
        self.BuyOnTime.setObjectName("BuyOnTime")
        self.horizontalLayout.addWidget(self.BuyOnTime)
        self.goodsOKButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.goodsOKButton.setStyleSheet("background-color: rgb(81, 142, 255);\n"
                                         "color: rgb(255, 255, 255);")
        self.goodsOKButton.setObjectName("goodsOKButton")
        self.horizontalLayout.addWidget(self.goodsOKButton)
        self.stopButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.stopButton.setStyleSheet("background-color: rgb(239,54,63);\n"
                                      "color:white;")
        self.stopButton.setCheckable(False)
        self.stopButton.setObjectName("stopButton")
        self.horizontalLayout.addWidget(self.stopButton)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 290, 341, 31))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_7 = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_3.addWidget(self.label_7)
        self.payPassword = QtWidgets.QLineEdit(self.horizontalLayoutWidget_2)
        self.payPassword.setText("")
        self.payPassword.setMaxLength(6)
        self.payPassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.payPassword.setObjectName("payPassword")
        self.horizontalLayout_3.addWidget(self.payPassword)
        self.label_10 = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_3.addWidget(self.label_10)
        self.buyCnt = QtWidgets.QSpinBox(self.horizontalLayoutWidget_2)
        self.buyCnt.setObjectName("buyCnt")
        self.horizontalLayout_3.addWidget(self.buyCnt)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(350, 0, 16, 371))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.infoPrint = QtWidgets.QTextBrowser(self.centralwidget)
        self.infoPrint.setGeometry(QtCore.QRect(360, 10, 501, 361))
        self.infoPrint.setStyleSheet("color: rgb(255, 255, 255);\n"
                                     "background-color: rgb(0, 0, 0);")
        self.infoPrint.setObjectName("infoPrint")
        MainWindow.setCentralWidget(self.centralwidget)

        # 京东登录按钮绑定
        self.loginButton.clicked.connect(self.loginJd)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "京东抢购软件         Email：1024839103ly@gmail.com"))
        self.JdTime.setText(_translate("MainWindow", "获取失败"))
        self.loginButton.setText(_translate("MainWindow", "登录"))
        self.label_3.setText(_translate("MainWindow", "京东时间："))
        self.timeButton.setText(_translate("MainWindow", "时间校正"))
        self.username.setText(_translate("MainWindow", "未登录"))
        self.label.setText(_translate("MainWindow", "当前登录："))
        self.label_2.setText(_translate("MainWindow", "商品编号："))
        self.label_4.setText(_translate("MainWindow", "地区代码："))
        self.areaId.setPlaceholderText(_translate("MainWindow", "使用有货下单时不能为空"))
        self.label_5.setText(_translate("MainWindow", "收货地址："))
        self.label_6.setText(_translate("MainWindow", "抢购时间："))
        self.buyTime.setDisplayFormat(_translate("MainWindow", "yyyy/M/d HH:mm:ss"))
        self.refreshAddressButton.setText(_translate("MainWindow", "刷新地址"))
        self.BuyOnTime.setText(_translate("MainWindow", "定时抢购"))
        self.goodsOKButton.setText(_translate("MainWindow", "有货下单"))
        self.stopButton.setText(_translate("MainWindow", "停止"))
        self.label_7.setText(_translate("MainWindow", "支付密码："))
        self.payPassword.setPlaceholderText(_translate("MainWindow", "可为空"))
        self.label_10.setText(_translate("MainWindow", "购买数量："))

    # 控制台打印
    def printf(self, mypstr):
        '''
        自定义类print函数,借用c语言 printf
        Mypstr：是待显示的字符串
        '''
        localTime = str(datetime.datetime.today())
        self.infoPrint.append('[' + localTime + '] ' + mypstr)  # 在指定的区域显示提示信息
        self.cursor = self.infoPrint.textCursor()
        self.infoPrint.moveCursor(self.cursor.End)  # 光标移到最后，这样就会自动显示出来
        QtWidgets.QApplication.processEvents()  # 一定加上这个功能，不然有卡顿

    # 登录成功确认框
    def closeEvent(self):
        reply = QMessageBox.question(self, 'Login Message', '是否已手动完成了登陆?',
                                     QMessageBox.No | QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            return True
        else:
            return False

    # 京东登录方法
    def loginJd(self):
        chrome=utils.depend.ChromeBrowser().chrome
        # 判断是否有本地的cookie
        cookieIsExists = checkCookie(jobName)
        #假如没有本地cookie
        if not cookieIsExists:
            self.printf("请在打开的浏览器窗口中进行登录")
            chrome.get("https://m.jd.com")
            time.sleep(5)  # 进入网页后有京东开屏广告，等待自动关闭
            try:
                chrome.find_element(By.ID, 'msShortcutLogin').click()
                # 是否完成登陆操作确认
                isLogin = self.closeEvent()
                if isLogin:
                    self.printf("登陆成功")
                    # 保存登录的cookie
                    saveCookie(jobName, chrome.get_cookies())
                    chrome.close()
                else:
                    self.printf("登陆失败，请重试")
            except:
                self.printf("发生无法避免的错误，请联系开发人员")
        # 假如有本地cookie
        else:
            chrome = utils.depend.ChromeBrowser().chrome
            chrome.get("https://m.jd.com")
            cookieList = readCookie(jobName)
            # 将本地cookie加载到浏览器
            for cookie in cookieList:
                chrome.add_cookie(cookie)
            print("cookie添加完成")
            time.sleep(3)
            chrome.refresh()
            # 保存最新的cookie
            saveCookie(jobName, chrome.get_cookies())