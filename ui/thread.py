import datetime
import json
import random

import pymysql
import requests
import selenium
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDateTime
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QWidget
from PyQt5.QtCore import QThread, pyqtSignal
import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import wait
from selenium.webdriver.support.wait import WebDriverWait

import utils.depend
# from jd_utils import register_util   #Mac开发临时关闭
from utils.cookieUtil import checkCookie, jobName, saveCookie, readCookie, deleteCookie
from selenium.webdriver.support import expected_conditions as EC

# 定义一个线程类
class New_Thread(QThread):
    # 自定义信号声明
    # 使用自定义信号和UI主线程通讯，参数是发送信号时附带参数的数据类型，可以是str、int、list等
    finishSignal = pyqtSignal(str)
    succesLogin = pyqtSignal(str,str,str)
    exitLogin = pyqtSignal(str)

    def __init__(self, code,  sku, cnt, areaId, payPassword,buyTime='',parent=None):

        super(New_Thread, self).__init__(parent)
        # code=0 定时抢购
        # code=1 有货抢购
        self.code = code
        self.sku = sku
        self.cnt = cnt
        self.areaId = areaId
        self.buyTime = buyTime
        self.payPassword=payPassword

    # run函数是子线程中的操作，线程启动后开始执行
    def run(self):
        # 检查有不有本地cookie
        if checkCookie("jd") == False:
            self.finishSignal.emit("请进行登录操作！")
        else:
            if self.code == 0:
                self.buyOnTime()
                pass
            elif self.code == 1:
                self.goodsOkBuy()
                pass
        # code=0 定时抢购
        # code=1 有货抢购
    # 检查是否拥有库存
    def checkStock(self, sku, areaId):

        # 官方请求地址：https://item-soa.jd.com/getWareBusiness?skuId=100012043978&area=22_2022_2028_43722
        # 第三方请求地址：https://c0.3.cn/stocks?type=batchstocks&skuIds=100021103403&area=1_72_2799_0
        # getUrl = 'https://item-soa.jd.com/getWareBusiness?skuId=' + sku + '&area=' + areaId  # 原官方
        getUrl = 'https://c0.3.cn/stocks?type=batchstocks&skuIds=' + sku + '&area=' + areaId  # 第三方接口
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
        }
        try:
            resp_json = requests.get(url=getUrl, headers=headers, timeout=10).text
            resp_json = json.loads(resp_json)
            stock_info = resp_json.get(sku)
            stock_state = stock_info.get('StockState')  # 商品库存状态：33 -- 现货  0,34 -- 无货  36 -- 采购中  40 -- 可配货
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
            # 返回参数不合法
            return 417
        except Exception as errorInfo:
            self.finishSignal.emit("发生未知异常，请联系开发者，异常原因：" + str(errorInfo))
            return 500

    # 库存抢购模式
    def goodsOkBuy(self):
        self.finishSignal.emit("进入有货下单模式")
        chrome = utils.depend.ChromeBrowser().chrome
        # 检查登录状态
        if self.loginByCookie(chrome) and self.loginCheck():
            sku = self.sku.text()
            areaId = self.areaId.text()
            buyCnt = self.cnt
            stockState = -1  # 用于判断是否继续进行库存监控(该功能初步构想是通过回调函数实现,暂时还未完成开发)
            cookies = {}
            # 获取cookie中的name和value,转化成requests可以使用的形式
            # seleniumCookie = chrome.get_cookies()
            # for cookie in seleniumCookie:
            #     cookies[cookie['name']] = cookie['value']
            if (sku == "") or (areaId == ""):
                self.finishSignal.emit("商品编号和地区代码不能为空")
            else:
                self.finishSignal.emit('商品sku：' + sku)
                self.finishSignal.emit('监控地区代码：' + areaId)
                # 请求地址：https://item-soa.jd.com/getWareBusiness?skuId=100012043978&area=22_2022_2028_43722
                url = "https://wqs.jd.com/order/m.confirm.shtml?sceneval=2&bid=&wdref=https://item.m.jd.com/product/" + sku + ".html?sceneval=2&scene=jd&isCanEdit=1&EncryptInfo=&Token=&commlist=" + sku + ",," + str(
                    buyCnt) + "," + sku + ",1,1,1&type=0&lg=0&supm=0"
                cnt = 0  # 记录购买操作次数
                while (True):
                    stockState = self.checkStock(sku, areaId)
                    if stockState == 1:
                        self.finishSignal.emit("检测到库存,开始执行自动下单！")
                        buyState = self.bugMethod(chrome, url)
                        if buyState == 200:
                            self.finishSignal.emit("下单成功")
                            break
                        elif buyState == 201:
                            self.finishSignal.emit("下单失败，正在重试")
                        elif buyState == 404:
                            self.finishSignal.emit("商品无法购买")
                        elif buyState == 405:
                            self.finishSignal.emit("商品无法提交订单，正在重试")
                        cnt += 1
                        if cnt == 5:
                            self.finishSignal.emit("多次重试下单均失败，任务暂停")
                            break
                    elif stockState == 0:
                        self.finishSignal.emit("无库存")
                        pass
                    elif stockState == 408:
                        self.finishSignal.emit("请求超时")
                        pass
                    elif stockState == 404:
                        self.finishSignal.emit("网络异常")
                        pass
                    elif stockState == 417:
                        self.finishSignal.emit("商品编号或地区代码不正确")
                        pass
                    elif stockState == 500:
                        break
                    time.sleep(1)
                payState = self.inputPw(chrome)
                if payState == 0:
                    self.finishSignal.emit("没有获取到支付密码，请自行支付")
                elif payState == 1:
                    self.finishSignal.emit("支付成功")
                elif payState == 404:
                    self.finishSignal.emit("无法进入付款页面")
                elif payState == 405:
                    self.finishSignal.emit("无法输入密码")
                elif payState == 2:
                    self.finishSignal.emit("支付失败")
        else:
            self.finishSignal.emit("账户已过期，请联系开发人员重新开通")

    # 定时抢购
    def buyOnTime(self):
        self.finishSignal.emit("进入定时抢购模式")
        chrome = utils.depend.ChromeBrowser().chrome
        self.loginByCookie(chrome)
        sku = self.sku
        # 获取设置的抢购时间并转换为时间戳
        buyTime = self.buyTime
        # "yyyy-MM-dd HH:mm:ss"
        buyTime = time.mktime(time.strptime(buyTime, '%Y-%m-%d %H:%M:%S'))
        buyTime = int(round(buyTime * 1000))  # 毫秒级时间戳
        buyCnt = self.cnt  # 购买的数量
        cnt = 0  # 记录购买操作次数



        url = "https://wqs.jd.com/order/m.confirm.shtml?sceneval=2&bid=&wdref=https://item.m.jd.com/product/" + sku + ".html?sceneval=2&scene=jd&isCanEdit=1&EncryptInfo=&Token=&commlist=" + sku + ",," + str(
            buyCnt) + "," + sku + ",1,1,1&type=0&lg=0&supm=0"
        while True:
            localTime = int(round(time.time() * 1000)) + 15
            if localTime >= buyTime:
                # self.finishSignal.emit("到达抢购时间，开始执行")
                buyState = self.bugMethod(chrome, url)
                if buyState == 200:
                    self.finishSignal.emit("下单成功")
                    payState = self.inputPw(chrome)
                    if payState == 0:
                        self.finishSignal.emit("没有获取到支付密码，请自行支付")
                    elif payState == 1:
                        self.finishSignal.emit("支付成功")
                    elif payState == 404:
                        self.finishSignal.emit("无法进入付款页面")
                    elif payState == 405:
                        self.finishSignal.emit("无法输入密码")
                    elif payState == 2:
                        self.finishSignal.emit("支付失败")
                    break
                elif buyState == 201:
                    self.finishSignal.emit("下单失败，正在重试")
                elif buyState == 404:
                    self.finishSignal.emit("商品无法购买")
                elif buyState == 405:
                    self.finishSignal.emit("商品无法提交订单，正在重试")
                cnt += 1
                if cnt == 5:
                    self.finishSignal.emit("多次重试下单均失败，任务暂停")
                    break
            else:
                continue

    # 下单具体方法
    def bugMethod(self, chrome, url):
        # 测试样本：
        # sku:  100008153202
        # sku:  5059594
        # areaId:   22_2022_2028_43722
        # https://wqs.jd.com/order/m.confirm.shtml?sceneval=2&bid=&wdref=https://item.m.jd.com/product/100008153202.html?sceneval=2&scene=jd&isCanEdit=1&EncryptInfo=&Token=&commlist=100008153202,,1,100008153202,1,1,1&type=0&lg=0&supm=0
        try:
            chrome.get(url)
        except:
            return 404
        try:
            confirmOrder = WebDriverWait(chrome, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'Submit_index__submit__35PK0')))
            confirmOrder.click()
        except Exception as errorInfo:
            return 405
        try:
            # 自动跳到收银台
            WebDriverWait(chrome, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'Header')))
            return 200
        except:
            # 没有自动跳到收银台
            try:
                payButton = WebDriverWait(chrome, 10).until(
                    EC.text_to_be_present_in_element((By.TAG_NAME, 'html'), "去支付")(chrome))
                return 200
            except:
                pass
            return 201

    # 输入密码
    def inputPw(self, chrome):
        password = self.payPassword
        if password == "":
            return 0  # 没有密码
        else:
            try:
                # 点击立即付款
                payBtn = WebDriverWait(chrome, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'payBtn')))
                payBtn.click()
            except:
                return 404  # 无法进入付款页面

            # 获取密码键盘并进行输入
            try:
                passwordKeyBoard = WebDriverWait(chrome, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'sys-area')))
                chrome.find_element(By.XPATH, '//*[@data-key="' + password[0] + '"]').click()
                chrome.find_element(By.XPATH, '//*[@data-key="' + password[1] + '"]').click()
                chrome.find_element(By.XPATH, '//*[@data-key="' + password[2] + '"]').click()
                chrome.find_element(By.XPATH, '//*[@data-key="' + password[3] + '"]').click()
                chrome.find_element(By.XPATH, '//*[@data-key="' + password[4] + '"]').click()
                chrome.find_element(By.XPATH, '//*[@data-key="' + password[5] + '"]').click()
            except:
                return 405  # 输入密码失败
            try:
                WebDriverWait(chrome, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'key')))
                if '收款方' in chrome.page_source:
                    return 1
                else:
                    return 2
            except:
                return 2  # 付款失败

    # 从本地cookie进行登录
    def loginByCookie(self, chrome):
        self.finishSignal.emit("检测到本地cookie，开始使用本地cookie进行登录")
        cookieList = readCookie(jobName)
        chrome.get("https://m.jd.com")
        jxsid = ''
        # 将本地cookie加载到浏览器
        try:
            for cookie in cookieList:
                chrome.add_cookie(cookie)
                if (cookie['name'] == 'jxsid'):
                    jxsid = cookie['value']
        except:
            self.finishSignal.emit("cookie加载出现问题，登陆可能失效,正在进行检查")
        time.sleep(1)
        chrome.refresh()
        if self.checkCookies(chrome, jxsid):
            return True
        else:
            return False

    # 检查cookie有效性,获取用户名，默认收货地址
    def checkCookies(self, chrome, jxsid):
        username = ''
        address = ''
        appCode = ''
        chrome.get(
            'https://trade.m.jd.com/order/orderlist_jdm.shtml?sceneval=2&jxsid=' + jxsid + '&orderType=all&ptag=7155.1.11')  # 全部订单页面的请求地址
        if '我的订单' in chrome.page_source:


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
            try:
                chrome.get(
                    'https://wqs.jd.com/my/my_address.shtml?sceneval=2&sid=&source=4&jxsid=' + jxsid + '&appCode=' + appCode)
                address = chrome.find_element(By.XPATH, "/html/body/div[2]/div[3]/div[2]/div[1]/ul/li[2]").text[3:]
            except:
                self.finishSignal.emit("未能成功获取到收货地址")
            self.succesLogin.emit("True",username,address)
            return True
        else:
            self.finishSignal.emit("cookie失效，请重新登陆")
            self.exitJd()
            return False

        # 京东的注销方法

    def exitJd(self):
        deleteCookie(jobName)
        self.finishSignal.emit("已退出京东登陆并删除本地cookie")

        # 更换绑定
        self.exitLogin.emit("False")

    # 授权是否过期
    def loginCheck(self):
        # code=register_util.register.getCombinNumber()# Mac开发临时关闭
        code = '1024'
        try:
            db = pymysql.connect(host='8.136.87.180', port=3306, user='jd_kill', passwd='jd_kill', db='jd_kill',
                                 charset='utf8')
            cursor = db.cursor()
            sql = " select * from account where MachineCode ='" + code + "' limit 1"
            cursor.execute(sql)
            data = cursor.fetchone()
            db.close()
            if data != None:
                return True
            else:
                return False
        except Exception as e:
            self.finishSignal.emit("网络发生错误，请检查网络。")
            return False

    #关闭Chrome浏览器
    def closeChrome(self,chrome):
        pass