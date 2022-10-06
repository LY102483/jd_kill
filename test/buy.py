import time

from selenium.webdriver.common.by import By

from utils.depend import chrome

'''
抢购操作核心函数
'''


def buy(cnt):
    # 当重复次数用尽，则自动退出
    if cnt < 0:
        print('抢购失败')
        chrome.close()
        exit(0)
    chrome.get("https://cart.jd.com/cart_index")  # 进入购物车页面
    time.sleep(0.3)
    # 购物车商品列表全选按钮定位
    checkAllBtn = chrome.find_element(By.XPATH, "/html/body/div[4]/div[2]/div[3]/div[1]/div/input")
    # 判断购物车商品列表全选按钮是否被选中
    is_selected = checkAllBtn.is_selected()
    if not is_selected:
        checkAllBtn.click()
    # 开始进行结算
    chrome.find_element(By.LINK_TEXT, '去结算').click()  # 进入结算页面
    time.sleep(0.3)
    # 提交订单
    chrome.find_element(By.XPATH,
                        '/html/body/div[15]/div/div[11]/div[8]/div/div[2]/div[1]/button[1]').click()  # 点击提交订单
    # 判断是否提交成功
    info = "提交成功"
    if info in chrome.page_source:
        print("购买成功")
        exit()
    else:
        cnt -= 1
        print("抢购失败，正在重试！")
        buy(cnt)



"""
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def submit_order(self):
        """提交订单
        重要：
        1.该方法只适用于普通商品的提交订单（即可以加入购物车，然后结算提交订单的商品）
        2.提交订单时，会对购物车中勾选✓的商品进行结算（如果勾选了多个商品，将会提交成一个订单）
        :return: True/False 订单提交结果
        """
        url = 'https://trade.jd.com/shopping/order/submitOrder.action'
        # js function of submit order is included in https://trade.jd.com/shopping/misc/js/order.js?r=2018070403091

        data = {
            'overseaPurchaseCookies': '',
            'vendorRemarks': '[]',
            'submitOrderParam.sopNotPutInvoice': 'false',
            'submitOrderParam.trackID': 'TestTrackId',
            'submitOrderParam.ignorePriceChange': '0',
            'submitOrderParam.btSupport': '0',
            'riskControl': self.risk_control,
            'submitOrderParam.isBestCoupon': 1,
            'submitOrderParam.jxj': 1,
            'submitOrderParam.trackId': self.track_id,  # Todo: need to get trackId
            'submitOrderParam.eid': self.eid,
            'submitOrderParam.fp': self.fp,
            'submitOrderParam.needCheck': 1,
        }

        # add payment password when necessary
        payment_pwd = global_config.get('account', 'payment_pwd')
        if payment_pwd:
            data['submitOrderParam.payPassword'] = encrypt_payment_pwd(payment_pwd)

        headers = {
            'User-Agent': self.user_agent,
            'Host': 'trade.jd.com',
            'Referer': 'http://trade.jd.com/shopping/order/getOrderInfo.action',
        }

        try:
            resp = self.sess.post(url=url, data=data, headers=headers)
            resp_json = json.loads(resp.text)

            # 返回信息示例：
            # 下单失败
            # {'overSea': False, 'orderXml': None, 'cartXml': None, 'noStockSkuIds': '', 'reqInfo': None, 'hasJxj': False, 'addedServiceList': None, 'sign': None, 'pin': 'xxx', 'needCheckCode': False, 'success': False, 'resultCode': 60123, 'orderId': 0, 'submitSkuNum': 0, 'deductMoneyFlag': 0, 'goJumpOrderCenter': False, 'payInfo': None, 'scaleSkuInfoListVO': None, 'purchaseSkuInfoListVO': None, 'noSupportHomeServiceSkuList': None, 'msgMobile': None, 'addressVO': None, 'msgUuid': None, 'message': '请输入支付密码！'}
            # {'overSea': False, 'cartXml': None, 'noStockSkuIds': '', 'reqInfo': None, 'hasJxj': False, 'addedServiceList': None, 'orderXml': None, 'sign': None, 'pin': 'xxx', 'needCheckCode': False, 'success': False, 'resultCode': 60017, 'orderId': 0, 'submitSkuNum': 0, 'deductMoneyFlag': 0, 'goJumpOrderCenter': False, 'payInfo': None, 'scaleSkuInfoListVO': None, 'purchaseSkuInfoListVO': None, 'noSupportHomeServiceSkuList': None, 'msgMobile': None, 'addressVO': None, 'msgUuid': None, 'message': '您多次提交过快，请稍后再试'}
            # {'overSea': False, 'orderXml': None, 'cartXml': None, 'noStockSkuIds': '', 'reqInfo': None, 'hasJxj': False, 'addedServiceList': None, 'sign': None, 'pin': 'xxx', 'needCheckCode': False, 'success': False, 'resultCode': 60077, 'orderId': 0, 'submitSkuNum': 0, 'deductMoneyFlag': 0, 'goJumpOrderCenter': False, 'payInfo': None, 'scaleSkuInfoListVO': None, 'purchaseSkuInfoListVO': None, 'noSupportHomeServiceSkuList': None, 'msgMobile': None, 'addressVO': None, 'msgUuid': None, 'message': '获取用户订单信息失败'}
            # {"cartXml":null,"noStockSkuIds":"xxx","reqInfo":null,"hasJxj":false,"addedServiceList":null,"overSea":false,"orderXml":null,"sign":null,"pin":"xxx","needCheckCode":false,"success":false,"resultCode":600157,"orderId":0,"submitSkuNum":0,"deductMoneyFlag":0,"goJumpOrderCenter":false,"payInfo":null,"scaleSkuInfoListVO":null,"purchaseSkuInfoListVO":null,"noSupportHomeServiceSkuList":null,"msgMobile":null,"addressVO":{"pin":"xxx","areaName":"","provinceId":xx,"cityId":xx,"countyId":xx,"townId":xx,"paymentId":0,"selected":false,"addressDetail":"xx","mobile":"xx","idCard":"","phone":null,"email":null,"selfPickMobile":null,"selfPickPhone":null,"provinceName":null,"cityName":null,"countyName":null,"townName":null,"giftSenderConsigneeName":null,"giftSenderConsigneeMobile":null,"gcLat":0.0,"gcLng":0.0,"coord_type":0,"longitude":0.0,"latitude":0.0,"selfPickOptimize":0,"consigneeId":0,"selectedAddressType":0,"siteType":0,"helpMessage":null,"tipInfo":null,"cabinetAvailable":true,"limitKeyword":0,"specialRemark":null,"siteProvinceId":0,"siteCityId":0,"siteCountyId":0,"siteTownId":0,"skuSupported":false,"addressSupported":0,"isCod":0,"consigneeName":null,"pickVOname":null,"shipmentType":0,"retTag":0,"tagSource":0,"userDefinedTag":null,"newProvinceId":0,"newCityId":0,"newCountyId":0,"newTownId":0,"newProvinceName":null,"newCityName":null,"newCountyName":null,"newTownName":null,"checkLevel":0,"optimizePickID":0,"pickType":0,"dataSign":0,"overseas":0,"areaCode":null,"nameCode":null,"appSelfPickAddress":0,"associatePickId":0,"associateAddressId":0,"appId":null,"encryptText":null,"certNum":null,"used":false,"oldAddress":false,"mapping":false,"addressType":0,"fullAddress":"xxxx","postCode":null,"addressDefault":false,"addressName":null,"selfPickAddressShuntFlag":0,"pickId":0,"pickName":null,"pickVOselected":false,"mapUrl":null,"branchId":0,"canSelected":false,"address":null,"name":"xxx","message":null,"id":0},"msgUuid":null,"message":"xxxxxx商品无货"}
            # {'orderXml': None, 'overSea': False, 'noStockSkuIds': 'xxx', 'reqInfo': None, 'hasJxj': False, 'addedServiceList': None, 'cartXml': None, 'sign': None, 'pin': 'xxx', 'needCheckCode': False, 'success': False, 'resultCode': 600158, 'orderId': 0, 'submitSkuNum': 0, 'deductMoneyFlag': 0, 'goJumpOrderCenter': False, 'payInfo': None, 'scaleSkuInfoListVO': None, 'purchaseSkuInfoListVO': None, 'noSupportHomeServiceSkuList': None, 'msgMobile': None, 'addressVO': {'oldAddress': False, 'mapping': False, 'pin': 'xxx', 'areaName': '', 'provinceId': xx, 'cityId': xx, 'countyId': xx, 'townId': xx, 'paymentId': 0, 'selected': False, 'addressDetail': 'xxxx', 'mobile': 'xxxx', 'idCard': '', 'phone': None, 'email': None, 'selfPickMobile': None, 'selfPickPhone': None, 'provinceName': None, 'cityName': None, 'countyName': None, 'townName': None, 'giftSenderConsigneeName': None, 'giftSenderConsigneeMobile': None, 'gcLat': 0.0, 'gcLng': 0.0, 'coord_type': 0, 'longitude': 0.0, 'latitude': 0.0, 'selfPickOptimize': 0, 'consigneeId': 0, 'selectedAddressType': 0, 'newCityName': None, 'newCountyName': None, 'newTownName': None, 'checkLevel': 0, 'optimizePickID': 0, 'pickType': 0, 'dataSign': 0, 'overseas': 0, 'areaCode': None, 'nameCode': None, 'appSelfPickAddress': 0, 'associatePickId': 0, 'associateAddressId': 0, 'appId': None, 'encryptText': None, 'certNum': None, 'addressType': 0, 'fullAddress': 'xxxx', 'postCode': None, 'addressDefault': False, 'addressName': None, 'selfPickAddressShuntFlag': 0, 'pickId': 0, 'pickName': None, 'pickVOselected': False, 'mapUrl': None, 'branchId': 0, 'canSelected': False, 'siteType': 0, 'helpMessage': None, 'tipInfo': None, 'cabinetAvailable': True, 'limitKeyword': 0, 'specialRemark': None, 'siteProvinceId': 0, 'siteCityId': 0, 'siteCountyId': 0, 'siteTownId': 0, 'skuSupported': False, 'addressSupported': 0, 'isCod': 0, 'consigneeName': None, 'pickVOname': None, 'shipmentType': 0, 'retTag': 0, 'tagSource': 0, 'userDefinedTag': None, 'newProvinceId': 0, 'newCityId': 0, 'newCountyId': 0, 'newTownId': 0, 'newProvinceName': None, 'used': False, 'address': None, 'name': 'xx', 'message': None, 'id': 0}, 'msgUuid': None, 'message': 'xxxxxx商品无货'}
            # 下单成功
            # {'overSea': False, 'orderXml': None, 'cartXml': None, 'noStockSkuIds': '', 'reqInfo': None, 'hasJxj': False, 'addedServiceList': None, 'sign': None, 'pin': 'xxx', 'needCheckCode': False, 'success': True, 'resultCode': 0, 'orderId': 8740xxxxx, 'submitSkuNum': 1, 'deductMoneyFlag': 0, 'goJumpOrderCenter': False, 'payInfo': None, 'scaleSkuInfoListVO': None, 'purchaseSkuInfoListVO': None, 'noSupportHomeServiceSkuList': None, 'msgMobile': None, 'addressVO': None, 'msgUuid': None, 'message': None}

            if resp_json.get('success'):
                order_id = resp_json.get('orderId')
                logger.info('订单提交成功! 订单号：%s', order_id)
                if self.send_message:
                    self.messenger.send(text='jd-assistant 订单提交成功', desp='订单号：%s' % order_id)
                return True
            else:
                message, result_code = resp_json.get('message'), resp_json.get('resultCode')
                if result_code == 0:
                    self._save_invoice()
                    message = message + '(下单商品可能为第三方商品，将切换为普通发票进行尝试)'
                elif result_code == 60077:
                    message = message + '(可能是购物车为空 或 未勾选购物车中商品)'
                elif result_code == 60123:
                    message = message + '(需要在config.ini文件中配置支付密码)'
                logger.info('订单提交失败, 错误码：%s, 返回信息：%s', result_code, message)
                logger.info(resp_json)
                return False
        except Exception as e:
            logger.error(e)
            return False

    @check_login
    def submit_order_with_retry(self, retry=3, interval=4):
        """提交订单，并且带有重试功能
        :param retry: 重试次数
        :param interval: 重试间隔
        :return: 订单提交结果 True/False
        """
        for i in range(1, retry + 1):
            logger.info('第[%s/%s]次尝试提交订单', i, retry)
            self.get_checkout_page_detail()
            if self.submit_order():
                logger.info('第%s次提交订单成功', i)
                return True
            else:
                if i < retry:
                    logger.info('第%s次提交失败，%ss后重试', i, interval)
                    time.sleep(interval)
        else:
            logger.info('重试提交%s次结束', retry)
            return False

    @check_login
    def submit_order_by_time(self, buy_time, retry=4, interval=5):
        """定时提交商品订单
        重要：该方法只适用于普通商品的提交订单，事先需要先将商品加入购物车并勾选✓。
        :param buy_time: 下单时间，例如：'2018-09-28 22:45:50.000'
        :param retry: 下单重复执行次数，可选参数，默认4次
        :param interval: 下单执行间隔，可选参数，默认5秒
        :return:
        """
        t = Timer(buy_time=buy_time)
        t.start()

        for count in range(1, retry + 1):
            logger.info('第[%s/%s]次尝试提交订单', count, retry)
            if self.submit_order():
                break
            logger.info('休息%ss', interval)
            time.sleep(interval)
        else:
            logger.info('执行结束，提交订单失败！')
            
            
"""