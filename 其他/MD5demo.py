import hashlib


def md5vale(key):
    '''
    MD5版本号加密对照函数
    :param key:加密密钥
    :return:
    '''
    sign0 = 'ed869855e10c7dd3372ebaa83993e67e'
    input_name = hashlib.md5()
    input_name.update(key.encode("utf-8"))
    if input_name.hexdigest() == sign0:
        return ("版本号加密正确:", input_name.hexdigest())
        # print("版本号加密正确:", input_name.hexdigest())
    else:
        return ('版本号有误',input_name.hexdigest())
        # print('版本号有误')


access_key = '9543'+'&'+'1619343837'
print(access_key)
print(md5vale(access_key))


# curl -X GET -H "content-type:application/json" -H "access_key:8cf142882375e1c149fdc8f8220d4ba1" -H "app_id:96461567" http://merchant-api.bitake.io/api/recharge/convert/v1?timestamp=1619343837&p1=9543&p2=CNY&p3=695
