from selenium import webdriver

from utils.cookieUtil import checkCookie, mainPath, jobName


class ChromeBrowser:
    def __init__(self):
        # 模拟浏览器代理

        # 设置Chrome浏览器
        chrome_options = webdriver.ChromeOptions()

        # 设置UA
        chrome_options.add_argument(
            'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1')
        # 选择让谷歌模拟的设备
        # mobileEmulation = {"deviceName": "iPhone XR"}
        # chrome_options.add_experimental_option("mobileEmulation", mobileEmulation)

        if checkCookie(jobName):
            # 隐身访问
            chrome_options.add_argument('--incognito')
            # 不加载图片, 提升速度
            chrome_options.add_argument('--blink-settings=imagesEnabled=false')
            # 不打开浏览器窗口
            chrome_options.add_argument("headless")

        # chrome_options.add_argument("headless")
        # 隐藏正受到自动测试软件的控制。
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])

        # 告诉编译器chromedriver在哪个位置并注册(如更换驱动版本则需要进行修改)
        self.chrome = webdriver.Chrome(mainPath + "/utils/chromedriver",
                                       chrome_options=chrome_options)

        # 设置窗口大小和位置
        self.chrome.set_window_size(390, 884)
        self.chrome.set_window_position(0, 0)


