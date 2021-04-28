import hashlib
import requests


class Sign(object):

    def __init__(self):
        # 私钥
        self.pay_prikey = 'aksjdhKWJf2348asjfhsdgsdgDAV'
        # 回调地址
        self.host = 'https://inte-cashier-dev.finpoints.tech/pay/union_notify/AdapterEpay'
        # self.host = 'https://inte-cashier-stg.finpoints.tech/pay/union_notify/AdapterEpay'
        # 回调demo
        self.data = {
            "PAYMENT_URL": "http://inte-cashier-dev.finpoints.tech/pay/synchronization/AdapterEpay/",
            # "PAYMENT_URL": "http://inte-cashier-stg.finpoints.tech/pay/synchronization/AdapterEpay/",
            "ORDER_NUM": "G201124161135025",
            "PAYEE_NAME": "ps tointe",
            "SUGGESTED_MEMO": "",
            "BAGGAGE_FIELDS": "",
            "PAYEE_ACCOUNT": "1000200",
            "V2_HASH2": "",
            "STATUS": "2",
            "PAYMENT_AMOUNT": "120.000000",
            "PAYER_ACCOUNT": "windson.chan@doo.hk",
            "PAYMENT_ID": "DP202104280229367075",
            "PAYMENT_UNITS": "USD",
            "TIMESTAMPGMT": "2021-04-27 17:45:30"
        }
        print(self.data)
        pass

    pass

    def md5(self):
        '''
            生成MD5加密字符串
            :param key:加密字符串
            :return:加密字符串结果
            '''
        # 格式化json为字典
        sss = dict(self.data)
        # 获取需加密拼接字符串
        key = sss['PAYMENT_ID'] + ':' + sss['ORDER_NUM'] + ':' + sss['PAYEE_ACCOUNT'] + ':' + sss[
            'PAYMENT_AMOUNT'] + ':' + sss['PAYMENT_UNITS'] + ':' + sss['PAYER_ACCOUNT'] + ':' + sss['STATUS'] + ':' + \
              sss['TIMESTAMPGMT'] + ':' + self.pay_prikey
        get_hash = hashlib.md5()
        get_hash.update(key.encode("utf-8"))

        return get_hash.hexdigest()

        pass

    pass

    def recall(self):
        body = self.data
        body['V2_HASH2'] = Sign().md5()
        callcrm = requests.post(url=self.host, data=body)
        return callcrm.json()
        pass

    pass


if __name__ == '__main__':
    # print(Sign().md5())
    print(Sign().recall())
