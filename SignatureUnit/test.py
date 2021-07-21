# pip install pycryptodome 安装
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5 as Sig_pk
from Crypto.PublicKey import RSA
import base64

PRIVATE = f"""-----BEGIN PRIVATE KEY-----
MIICdwIBADANBgkqhkiG9w0BAQEFAASCAmEwggJdAgEAAoGBALDFGo3G5REcR9t6
VFlpFpVt1Z0j8qeh8xe/GY/6q80XwVO+WSnFmRoi2qQttBU7x7h/mkyx5Ye5856Q
FWvVUKDhHx4CbTB21fIQkqhrsQH0DXW8EPhJ1XeygLsDmtIk7y4Q3vNvCU/g0e85
PzM1BD5KnbQOTw0HaeQmVuMuPglPAgMBAAECgYEAqdGxYOLizT1OCxvKTNsYRxXt
UblnNIPw9a8w75Dx22Ym5DzJi8e4/dLeGTuO9Zcol6Z+pY+B4pJR6NKiwaV8fnio
1NOv5ugP21TeWeFXeg4Knstq2DuyxAGXaFRMQZDoj3yN2dmUxyUdL8B0KDkO8qWA
mgQuPxcM4cBdYh35AYECQQDeMBISubPz3V+qdy8R60DH9jaxz92AzmN2gz6s5VAd
vAWnlzE15Ceen9DPaQIpXrpoh6Lb8b3hCbJOr9mz18qTAkEAy6uoWRMTzV5wB4o0
2MIx9X0jfw7M80UlEQGLQRdlJ3341WqJydaAC6kGBs3DkMoYQq7SyZa9yma6zIf+
oeiv1QJADbeOBhXs5CtQkqeVAlgxwaaTrdqVZDRZs6FapzXpAkzvVG9jHF6fi412
SLfE6GTuwTFOfqGoBVKh7XWxzQaPfQJAI7EwbnO+a6YaIeghfL8DfE7y0ohoeFVs
un83xS9xZatY2SWzgfCaPfDgAn86v3v7Jmx2uic1mWvJXqCSihM6BQJBAMsA19y/
3FrP+XS+cR1Q+JJf9jdANglOVV3Ac9+35ixuxSV0RGn5R/JW+k5jvLBrONSlfBnb
EFS5pOOIcIsTca8=
-----END PRIVATE KEY-----
"""
PUBLIC = f"""-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDGQ1SNV2jbD0TDvWRtK2QgJnDC
gG7OClLYz5NgyYxgqAZ4iZe/+RpXdkPePqtU++MSiuVEOTwYASipH61+ivjudZXc
xsgHyA5ExQsRgjrT84CTUZ+mLJqGHKzLD7bW/zaX3A0rHdMZbRmxva1PhMwVJbXP
UAFFMTHDfb3Mm4RzJQIDAQAB
-----END PUBLIC KEY-----
"""


def sign_str(parm):
    """
    参数排序
    """
    str_parm = ''
    for p in sorted(parm):
        print(p)
        if p in ['sign', 'signType'] or not parm[p]:
            continue
        elif isinstance(parm[p], dict):
            str_parm += str(p) + "=" + "{" + sign_str(parm[p]) + "}" + "&"
        else:
            str_parm += str(p) + "=" + str(parm[p]) + "&"
    return str_parm[:-1]


def sign_by_private_key(sortData, private_key):
    """
    ras2签名
    """
    # 获取私钥
    # key = base64.b64decode(private_key)
    missing_padding = 4 - len(private_key) % 4
    print(missing_padding)
    key = base64.b64decode(private_key + '=' * missing_padding)
    print(len(private_key) % 4)
    print(key)

    rsakey = RSA.importKey(key)
    # 根据sha算法处理签名内容  (此处的hash算法不一定是sha,看开发)
    data = SHA256.new(sortData.encode())

    # 私钥进行签名
    sig_pk = Sig_pk.new(rsakey)
    signer = sig_pk.sign(data)
    # 将签名后的内容，转换为base64编码
    result = base64.b64encode(signer)
    # 签名结果转换成字符串
    data = result.decode()
    return data


if __name__ == '__main__':
    print(sign_by_private_key(sortData="abcd", private_key=PUBLIC))
    pass
