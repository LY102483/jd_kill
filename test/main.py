import datetime
import time

from selenium.webdriver.common.by import By

from method.JdDependent import buy
from utils.cookieUtil import checkCookie, jobName, saveCookie, readCookie
from utils.depend import chrome

'''
京东购物车模式抢购脚本
'''

# 抢购时间(格式化时间：2022, 9, 10, 17, 33, 10 )
buyTime = datetime.datetime(2022, 9, 10, 21, 36, 30)
# 抢购执行次数
cnt = 5
# 初次使用需要扫码登录，此处设置为扫码登录的时间，单位秒
loginTime = 15

# 判断是否有本地的cookie
cookieIsExists = checkCookie(jobName)

# 打开网页
chrome.get("https://www.jd.com")
# 设置窗口最大化
chrome.maximize_window()

# 没有cookie则进行登陆操作
if not cookieIsExists:
    chrome.find_element(By.LINK_TEXT, '你好，请登录').click()
    print('请扫描二维码')
    time.sleep(loginTime)  # 扫码登录等待时间
    # 保存登录的cookie
    saveCookie(jobName, chrome.get_cookies())
else:
    cookieList = readCookie(jobName)
    # 将本地cookie加载到浏览器
    for cookie in cookieList:
        chrome.add_cookie(cookie)
    time.sleep(3)
    chrome.refresh()
    # 保存最新的cookie
    saveCookie(jobName, chrome.get_cookies())

# 判断是否到达抢购时间
localTime = datetime.datetime.today()
timeDifference = (buyTime - localTime).seconds
while timeDifference > 0:
    time.sleep(0.5)
    localTime = datetime.datetime.today()
    timeDifference = (buyTime - localTime).seconds
    print('倒计时:' + str(timeDifference) + '秒')
    # 定时刷新网页，防止会话过期
    if timeDifference % 150 == 0 and timeDifference >= 20:
        chrome.refresh()
        time.sleep(2)
        saveCookie(jobName, chrome.get_cookies())
        print("执行了一次网页刷新操作")
buy(cnt)
