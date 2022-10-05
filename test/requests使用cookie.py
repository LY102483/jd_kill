
import requests
from selenium import webdriver
import time

# 使用selenium打开网址,然后让用户完成手工登录,再获取cookie
url = 'https://passport.jd.com/new/login.aspx'
driver = webdriver.Chrome()
driver.get(url=url)
time.sleep(30)
driver.refresh()
c = driver.get_cookies()
print(c)
cookies = {}
# 获取cookie中的name和value,转化成requests可以使用的形式
for cookie in c:
    cookies[cookie['name']] = cookie['value']

print(cookies)
driver.quit()
time.sleep(5)

headers = {
    'authority': 'www.jd.com',
    'method': 'GET',
    'path': '/',
    'scheme': 'https',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',

}
# 使用该cookie完成请求
response = requests.get(url='https://cart.jd.com/cart.action', headers=headers, cookies=cookies)
print(response.text)