import datetime
import json

import requests
import selenium
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QWidget

import time
from selenium.webdriver.common.by import By

import utils.depend
from utils.cookieUtil import checkCookie, jobName, saveCookie, readCookie, deleteCookie


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
        # 有货抢购按钮绑定
        self.goodsOKButton.clicked.connect(self.goodsOkBuy)
        #定时抢购按钮绑定
        self.BuyOnTime.clicked.connect(self.buyOnTime)
        #更新地址按钮绑定
        self.refreshAddressButton.clicked.connect(self.loginJd)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        # 有本地cookie则自动登陆
        if checkCookie(jobName):
            self.loginJd()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "京东抢购软件         Email：jdkill2022@outlook.com"))
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
        self.buyTime.setDisplayFormat(_translate("MainWindow", "yyyy-MM-dd HH:mm:ss"))
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
        try:
            chrome = utils.depend.ChromeBrowser().chrome
            chrome.get("https://m.jd.com")
            # 判断是否有本地的cookie
            cookieIsExists = checkCookie(jobName)
            # 存放cookie中的数据用于登录检查
            jxsid = ''
            # 假如没有本地cookie
            if not cookieIsExists:
                self.printf("请在打开的浏览器窗口中进行登录")
                time.sleep(5)  # 进入网页后有京东开屏广告，等待自动关闭
                try:
                    chrome.find_element(By.ID, 'msShortcutLogin').click()
                    # 是否完成登陆操作确认
                    isLogin = self.closeEvent()
                    if isLogin:
                        self.printf("手动登陆完成，开始检查cookie是否有效！")
                        self.checkCookies(chrome, jxsid)
                        chrome.close()
                        chrome.quit()
                    else:
                        self.printf("登陆失败，请重试")
                except Exception as errorInfo:
                    self.printf("发生无法避免的错误，请按照标准流程重试，如仍发生错误，请联系开发人员.")
            # 假如有本地cookie
            else:
                self.printf("检测到本地cookie，开始使用本地cookie进行登录")
                cookieList = readCookie(jobName)
                chrome.get("https://m.jd.com")
                # 将本地cookie加载到浏览器
                try:
                    for cookie in cookieList:
                        chrome.add_cookie(cookie)
                        if (cookie['name'] == 'jxsid'):
                            jxsid = cookie['value']
                except :
                    self.printf("cookie加载出现问题，登陆可能失效,正在进行检查")
                time.sleep(1)
                chrome.refresh()
                print("cookie已加载进浏览器并进行了刷新")
                self.checkCookies(chrome,jxsid)
        except selenium.common.exceptions.WebDriverException:
            self.printf("无法连接到京东服务器")
        except Exception as errorInfo:
            self.printf("发生无法避免的错误，请按照标准流程重试，如仍发生错误，请联系开发人员.")

    # 京东的注销方法
    def exitJd(self):
        print("进入了京东的注销方法")
        deleteCookie(jobName)
        self.printf("已退出京东登陆并删除本地cookie")
        self.loginButton.setText("登陆")
        self.loginButton.setStyleSheet("background-color: rgb(81, 142, 255);\n"
                                       "color: rgb(255, 255, 255);")
        self.loginButton.setObjectName("loginButton")
        self.username.setText("未登录")
        self.address.setText("")
        # 更换绑定
        try:
            self.loginButton.clicked.disconnect(self.exitJd)
        except Exception:
            pass
        try:
            self.loginButton.clicked.connect(self.loginJd)
        except Exception:
            pass



    # 检查cookie有效性,获取用户名，默认收货地址
    def checkCookies(self,chrome,jxsid):
        username=''
        address=''
        appCode=''
        print("开始检查cookie")
        chrome.get(
            'https://trade.m.jd.com/order/orderlist_jdm.shtml?sceneval=2&jxsid=' + jxsid + '&orderType=all&ptag=7155.1.11') # 全部订单页面的请求地址
        if '我的订单' in chrome.page_source:
            self.printf("cookie有效，登陆成功")
            self.loginButton.setText("注销")
            self.loginButton.setStyleSheet("background-color: rgb(239,54,63);\n"
                                           "color:white;")
            self.loginButton.setObjectName("exitButton")
            self.loginButton.clicked.disconnect(self.loginJd)
            self.loginButton.clicked.connect(self.exitJd)
            # 收货地址请求页面url:https://wqs.jd.com/my/my_address.shtml?sceneval=2&sid=&source=4&jxsid=16652542868603284611&appCode=ms0ca95114
            # xpath:/html/body/div[2]/div[3]/div[2]/div[1]/ul/li[2]
            # 获取用户名并设置(用户名存储在了cookie中)
            saveCookie(jobName, chrome.get_cookies())
            cookieList = readCookie(jobName)
            for cookie in cookieList:
                chrome.add_cookie(cookie)
                if (cookie['name'] == 'pwdt_id'):
                    username = cookie['value']
                if (cookie['name'] == 'appCode'):
                    appCode = cookie['value']
            chrome.get('https://wqs.jd.com/my/my_address.shtml?sceneval=2&sid=&source=4&jxsid='+jxsid+'&appCode='+appCode)
            address=chrome.find_element(By.XPATH,"/html/body/div[2]/div[3]/div[2]/div[1]/ul/li[2]").text[3:]
            self.address.setText(address)
            self.username.setText(username if username!='' else '未能成功获取到用户名')
            return True
        else:
            self.printf("cookie失效，请重新登陆")
            self.exitJd()
            return False

    # 检查是否拥有库存
    def checkStock(self, sku, areaId):
        # 请求地址：https://item-soa.jd.com/getWareBusiness?skuId=100012043978&area=22_2022_2028_43722
        getUrl = 'https://item-soa.jd.com/getWareBusiness?skuId=' + sku + '&area=' + areaId
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
        }
        try:
            resp_json = requests.post(url=getUrl, headers=headers, timeout=10).text
            resp_json = json.loads(resp_json)
            stock_info = resp_json.get('stockInfo')
            stock_state = stock_info.get('stockState')  # 商品库存状态：33 -- 现货  0,34 -- 无货  36 -- 采购中  40 -- 可配货
            if stock_state in (33, 40):
                return 1
            else:
                return 0
        except requests.exceptions.Timeout:
            # 查询库存超时
            return 408
        except requests.exceptions.RequestException as request_exception:
            # 网络异常
            return 404
        except json.decoder.JSONDecodeError:
            # 请求参数不合法
            return 417
        except Exception as errorInfo:
            self.printf("发生未知异常，请联系开发者，异常原因：" + str(errorInfo))
            return 500


    # 库存抢购模式
    def goodsOkBuy(self):
        self.printf("进入有货下单模式")
        sku = self.sku.text()
        areaId = self.areaId.text()
        stockState = -1  # 用于判断是否继续进行库存监控
        if (sku == "") or (areaId == ""):
            self.printf("商品编号和地区代码不能为空")
        else:
            self.printf('商品sku：' + sku)
            self.printf('监控地区代码：' + areaId)
            while (True):
                stockState = self.checkStock(sku, areaId)
                if stockState == 1:
                    self.printf("检测到库存")
                elif stockState == 0:
                    self.printf("无库存")
                elif stockState == 408:
                    self.printf("请求超时")
                elif stockState == 404:
                    self.printf("网络异常")
                elif stockState == 417:
                    self.printf("商品编号或地区代码不正确")
                elif stockState == 500:
                    break


    #定时抢购
    def buyOnTime(self):
        self.printf("进入定时抢购模式")

        # 获取设置的抢购时间并转换为时间戳
        buyTime=self.buyTime.text()
        # "yyyy-MM-dd HH:mm:ss"
        buyTime=time.mktime(time.strptime(buyTime, '%Y-%m-%d %H:%M:%S'))
        buyTime=int(round(buyTime * 1000))#毫秒级时间戳

        while True:
            localTime = int(round(time.time() * 1000))
            if localTime >= buyTime:
                self.printf("到达抢购时间，开始执行")
                break
            else:
                time.sleep(0.05)