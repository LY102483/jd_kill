import json
import time

import requests


cookies = {
    # 放Cookie
}
# sku
sku = '10033799596506'
# 数量
cnt = '1'

#毫秒级时间戳
buyTime = '2022-11-12 00:00:00'
buyTime = int(round(time.mktime(time.strptime(buyTime, "%Y-%m-%d %H:%M:%S")) * 1000000))
print("购买时间"+str(buyTime))


while True:
    nowTime=int(round(time.time() * 1000000))
    print("倒计时:" + str(buyTime-nowTime))
    if nowTime>buyTime:
        break
    else:
        time.sleep(0.002)


# 设置请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Linux; U; Android 9; zh-cn; V1938CT Build/PPR1.180610.011) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/10.1 Mobile Safari/537.36",
    "Connection": "keep-alive",
    'Host': 'wq.jd.com'
}

headers['Referer'] = "https://wq.jd.com/deal/minfo/orderinfo"
session = requests.Session()
data={
"appCode":"ms0ca95114",
"callback":"orderinfoCbA",
"r":"0.08917363780771337",
"action":"1",
"type":"0",
"useaddr":"0",
"addressid":"",
"dpid":"",
"addrType":"1",
"paytype":"0",
"firstin":"1",
"scan_orig":"",
"sceneval":"2",
"reg":"1",
"encryptversion":"1",
"commlist":sku+",,"+cnt+","+sku+",1,0,0",
"cmdyop":"0",
"locationid":"",
"clearbeancard":"1",
"wqref":"https://item.m.jd.com/product/"+sku+".html?pps=reclike.FO4O605:FOFO00495BC3DF3O13O6:FOFO0F10416O843O1FO3O643O7FFF5021813FO7O17495BC3DF61C1D885ACF71EF2",
"g_tk":"5381",
"g_ty":"ls"
}
url="https://wq.jd.com/deal/minfo/orderinfo"
resp=session.post(url,headers=headers,cookies=cookies,data=data,verify=False)
print(resp.text)
# print(resp.text)
resp = resp.text.replace("orderinfoCbA(", "")
resp = resp.replace(")", "")
resp = json.loads(resp)
token2 = resp["token2"]
traceid=resp["traceId"]


data={
'paytype':'0',
'paychannel':'1',
'action':'1',
'reg':'1',
'type':'0',
'token2':token2,
'dpid':'',
'skulist':sku,
'scan_orig':'',
'gpolicy':'',
'platprice':'0',
'ship':'',
'pick':'',
'savepayship':'0',
'valuableskus':sku+','+cnt+',71800,700',
'commlist':sku+',,'+cnt+','+cnt+',1,0,0',
'pwd':'b59c67bf196a4758191e42f76670ceba',
'sceneval':'2',
'setdefcoupon':'0',
'r':'0.3146251378894271',
'callback':'confirmCbA',
'traceid':traceid,
'g_pt_tk':'394982073',
'g_ty':'ls',
'appCode':'ms0ca95114'
}
headers['Referer'] = "https://wq.jd.com/deal/confirmorder/main?sceneval=2&bid=&wdref=https://item.m.jd.com/product/"+sku+".html?sceneval=2&jxsid=16426172376700795005&scene=jd&isCanEdit=1&EncryptInfo=&Token=&commlist="+sku+",,"+cnt+","+sku+",1,0,0&locationid=&type=0&lg=0&supm=0"
url='https://wq.jd.com/deal/msubmit/confirm'
resp=session.post(url,data=data,headers=headers,cookies=cookies,verify=False)
print(resp.text)
resp=json.loads(resp.text.split("(")[1].split(")")[0])
if len(resp["dealId"])!=0:
    print("下单成功")
else:
    print("下单失败，请检查账户自行下单是否需要输入支付密码")
