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
        return ('版本号有误')
        # print('版本号有误')


print(md5vale('kRVaXGVk$QYn$OyB'))
