import hashlib
import hmac
import base64
from hashlib import sha256
import json


class SecretFun(object):
    def md5(self, content):
        """
        md5加密
        :param content:代签名字符串
        :return:16进制，32bit
        """
        # get_hash = hashlib.md5()
        # get_hash.update(content.encode("utf-8"))
        # return get_hash.hexdigest()
        hashstring = hashlib.md5(content.encode("utf-8")).hexdigest()
        return hashstring

    pass

    pass

    def sha(self, content, digestmod):
        """
        sha1、sha256加密,16进制，32bit
        :param content: 待加密字符串
        :param digestmod: sha1、sha256
        :return: 加密字符串结果
        """
        if digestmod.upper() == "SHA1":
            try:
                hashstring = hashlib.sha1(content.encode("utf-8")).hexdigest()
                return hashstring
            except BaseException as Error:
                return Error
        if digestmod.upper() == "SHA256":
            try:
                hashstring = hashlib.sha256(content.encode("utf-8")).hexdigest()
                return hashstring
            except BaseException as Error:
                return Error
        else:
            raise Exception('digestmod错误')
        pass

    pass

    def hmacsha(self, sal, content, digestmod):
        """
        hmacsha1、hmacsha256加密,16进制，32bit
        :param sal: 盐值
        :param content: 待加密字符串
        :param digestmod: sha1、sha256
        :return: 加密字符串结果
        """
        if digestmod.upper() == "SHA1":
            try:
                hashstring = hmac.new(sal.encode("utf-8"), content.encode("utf-8"), digestmod=digestmod).hexdigest()
                # signature = base64.b64encode(hmac.new(appsecret, data, digestmod="sha256").digest()) # 2进制
                return hashstring
            except BaseException as Error:
                return Error
        if digestmod.upper() == "SHA256":
            try:
                hashstring = hmac.new(sal.encode("utf-8"), content.encode("utf-8"), digestmod=digestmod).hexdigest()
                return hashstring
            except BaseException as Error:
                return Error
        else:
            raise Exception('digestmod错误')
        pass

    pass


if __name__ == '__main__':
    # print(SecretFun().md5(json.dumps(a)))
    # print(SecretFun().sha(content="123", digestmod="sha256"))
    print(SecretFun().hmacsha(sal="123", content="abc", digestmod="sha256"))
    print(SecretFun().hmacsha256(sal="123", data="abc"))
