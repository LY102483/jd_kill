import time

from selenium.webdriver.common.by import By

from utils.depend import chrome


class jd_dependent(object):
    # 库存查询的方法
    def selectNum(self):
        #请求地址：https://item-soa.jd.com/getWareBusiness?skuId=100012043978&area=22_2022_2028_43722


        pass
    def loginJd(self):
        chrome.get("https://m.jd.com")
        # main_window.printf(self,"程序将在5S中后进行登录操作")
        try:
            chrome.find_element(By.ID, 'msShortcutLogin').click()
        except:

            time.sleep(5)
        try:
            chrome.find_element(By.ID, 'msShortcutLogin').click()
        except:
            print("没有登陆按钮2")

