"""
代码待调试
"""
import rsa
import base64

__pem_begin = '-----BEGIN RSA PRIVATE KEY-----\n'
__pem_end = '\n-----END RSA PRIVATE KEY-----'

key = f"""-----BEGIN PRIVATE KEY-----
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


def sign(content, private_key, sign_type):
    """签名

    :param content: 签名内容
    :type content: str

    :param private_key: 私钥字符串，PKCS#1
    :type private_key: str

    :param sign_type: 签名类型，'RSA', 'RSA2'二选一
    :type sign_type: str

    :return: 返回签名内容
    :rtype: str
    """
    if sign_type.upper() == 'RSA':
        return rsa_sign(content, private_key, 'SHA-1')
    elif sign_type.upper() == 'RSA2':
        return rsa_sign(content, private_key, 'SHA-256')
    else:
        raise Exception('sign_type错误')


def rsa_sign(content, private_key, _hash):
    """SHAWithRSA

    :param content: 签名内容
    :type content: str

    :param private_key: 私钥
    :type private_key: str

    :param _hash: hash算法，如：SHA-1,SHA-256
    :type _hash: str

    :return: 签名内容
    :rtype: str
    """
    private_key = _format_private_key(private_key)
    pri_key = rsa.PrivateKey.load_pkcs1(private_key.encode('utf-8'))
    sign_result = rsa.sign(content, pri_key, _hash)
    return base64.b64encode(sign_result)


def _format_private_key(private_key):
    """对私进行格式化，缺少"-----BEGIN RSA PRIVATE KEY-----"和"-----END RSA PRIVATE KEY-----"部分需要加上

    :param private_key: 私钥
    :return: pem私钥字符串
    :rtype: str
    """
    if not private_key.startswith(__pem_begin):
        private_key = __pem_begin + private_key
    if not private_key.endswith(__pem_end):
        private_key = private_key + __pem_end
    return private_key


if __name__ == '__main__':
    sign(content="abcd", private_key=key, sign_type="RSA2")
