from selenium import webdriver

from utils.cookieUtil import checkCookie, mainPath, jobName

# 模拟浏览器代理
# headers = {
#     'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'}

# 设置Chrome浏览器
chrome_options = webdriver.ChromeOptions()

# 选择让谷歌模拟的设备
mobileEmulation = {"deviceName": "iPhone XR"}
chrome_options.add_experimental_option("mobileEmulation", mobileEmulation)
# 隐身访问
# chrome_options.add_argument('--incognito')

# 不加载图片, 提升速度
# chrome_options.add_argument('--blink-settings=imagesEnabled=false')
# 改进：如果存在cookie，则说明无需验证登录，则可以设置为不加载图片以提升速度
if checkCookie(jobName):
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    chrome_options.add_argument("headless")

# 不打开浏览器窗口
# chrome_options.add_argument("headless")
# 隐藏正受到自动测试软件的控制。
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])

# 告诉编译器chromedriver在哪个位置并注册(如更换驱动版本则需要进行修改)
chrome = webdriver.Chrome(mainPath + "/utils/chromedriver",
                          chrome_options=chrome_options)

# 设置窗口大小和位置
chrome.set_window_size(500,962)
chrome.set_window_position(0,0)