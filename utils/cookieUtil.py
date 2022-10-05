import json
import os
#任务路径(无需修改)
mainPath=os.path.abspath(os.getcwd())
# 任务名称
jobName = 'jd'
cookiesPath = mainPath + "/cookies/"


# 检查cookie是否存在
def checkCookie(name):
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    path = cookiesPath + name + ".json"
    isExists = os.path.exists(path)
    # 判断结果
    if isExists:
        return True
    else:
        return False


# 读取cookie
def readCookie(name):
    # 以 utf-8 的编码格式打开指定文件
    cookie_file = open(cookiesPath + name + ".json", mode='r')
    # 输出读取到的数据
    cookie = json.loads(cookie_file.read())
    # 关闭文件
    cookie_file.close()
    return cookie


# 存储cookie
def saveCookie(name, cookie):
    jsonCookies=json.dumps(cookie)
    cookie_file = open(cookiesPath + name + ".json", mode='w')
    # 写入cookie
    cookie_file.write(jsonCookies)
    # 关闭文件
    cookie_file.close()
