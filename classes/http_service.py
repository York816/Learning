# coding=utf-8
import common
import config
import json
import time
import requests
import urllib3

from classes.log_service import Log
from urllib.parse import urlencode

LOG = Log.get_logger(__name__)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

api_dict = {}
node_host = config.node_host
mode = None
secret = None
nonce = None


class HttpService(object):
    __timeout = config.timeout
    __http = {}

    __cookie = None
    __headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/80.0.3987.149 Safari/537.36"
    }

    def __init__(self, host: str, port: int, protocol: str = "http", version: str = "", u_type: str = "default"):
        """
        初始化
        :param host:
        :param port:
        :param protocol:
        :param version:
        :param u_type:
        """
        if not isinstance(host, str) or host == "" or not isinstance(port, int) or not 0 < port < 65536:
            raise ValueError("host must be string, port must be greater than 0 and  less than 65536.")
        self.url = f"{protocol}://{host}:{port}{version}"
        self.version = version
        self.host = host
        if u_type not in self.__http:
            self.__http[u_type] = requests.session()
        LOG.info(self.url)
        self.node_server = NodeService(node_host, self.version)

    def login(self, uri: str, params: dict, u_type: str = "default"):
        """
        登录获取cookies
        :param uri:
        :param params:
        :param u_type:
        :return:
        """
        if not isinstance(uri, str) or uri == "" or not isinstance(params, dict) or params == {}:
            raise ValueError("login_uri must be not emtpy, login_params must be not emtpy.")

        LOG.info(f"login uri: {uri}, login params: {json.dumps(params)}")
        headers = self.__headers
        secret_params = None

        # 加密判断
        result = common.get_secret_info(url=self.url)
        try:
            if 'code' not in result:
                pub_key = result["pubKey"]
                aes_method = result["aesMethod"]
                pass_phrase = result["passphrase"]
                pid = result["pid"]
                global api_dict
                api_dict[self.host] = result["apiList"]["encryptRoutes"]
                # print("api_dict", api_dict)
                if "cl" in self.host:
                    api_dict[self.host].append({'methods': 'POST', 'path': '/v2/user/auth/signIn'})
                if api_dict[self.host]:
                    for path in api_dict[self.host]:
                        if f"{self.version}{uri}" == path["path"]:
                            secret_param = {
                                "pubKey": pub_key,
                                "aesMethod": aes_method,
                                "passphrase": pass_phrase,
                                "pid": pid,
                                "originParam": params  # 登录的账号密码参数
                            }
                            secret_rp = self.node_server.secret(secret_param)
                            ciphertext = secret_rp["ciphertext"]  # 登录的密文
                            # 后续接口使用的加解密信息
                            global mode
                            global secret
                            global nonce
                            mode = secret_rp["mode"]
                            secret = secret_rp["secret"]
                            nonce = secret_rp["nonce"]
                            secret_params = {"ciphertext": ciphertext}
                            break
                        else:
                            secret_params = params
                else:
                    secret_params = params
            else:
                secret_params = params

        except Exception as e:
            LOG.error(e)

        response = self.__http[u_type].post(url=f"{self.url}{uri}", json=secret_params, headers=headers,
                                            timeout=self.__timeout, verify=False)

        LOG.info(f"login response: {response.text}")

        if response.json().get("ciphertext") is not None or response.json().get("code") == 0:
            # 拼接cookie
            self.__cookie = requests.utils.dict_from_cookiejar(response.cookies)
            LOG.info(self.__cookie)

        return response.json()

    def call(self, method: str, uri: str, params: dict = None, u_type: str = "default", files: bytes = None):
        """
        接口请求
        :param method:
        :param uri:
        :param params:
        :param files:
        :param u_type:
        :return:
        """
        print(f"method: {method}")
        print(f"uri: {uri}")
        print(f"params: \n{json.dumps(params, ensure_ascii=False, indent=4)}")

        LOG.info(f"{method} | {uri} | {json.dumps(params)}")
        try:
            method = method.upper()
            if method not in ["GET", "POST", "PUT", "DELETE"]:
                raise ValueError("method must be GET or POST or PUT or DELETE.")

            if params is None or not isinstance(params, dict):
                params = {}

            # 请求头添加cookie
            headers = self.__headers

            # 加密判断
            if self.node_server.is_encryption(self.host, uri):
                print("加密接口")
                # print({"mode": mode, "key": secret, "iv": nonce})
                if params == {}:
                    params = '{}'
                en_rps = self.node_server.encryption(self.node_server.package(param=params))
                if en_rps['code'] == 0:
                    en_rps_params = {"ciphertext": en_rps['msg']}
                else:
                    en_rps_params = params
            else:
                en_rps_params = params

            # 请求
            if method == "POST":
                time.sleep(3)
                # 兼容文件上传格式请求
                if files:
                    response = self.__http[u_type].post(url=f"{self.url}{uri}", files=files, verify=False,
                                                        cookies=self.__cookie)
                else:
                    response = self.__http[u_type].post(url=f"{self.url}{uri}", json=en_rps_params, headers=headers,
                                                        timeout=self.__timeout, verify=False, cookies=self.__cookie)
            elif method == "PUT":
                response = self.__http[u_type].put(url=f"{self.url}{uri}", json=en_rps_params, headers=headers,
                                                   timeout=self.__timeout, verify=False, cookies=self.__cookie)

            elif method == "DELETE":
                params_str = urlencode(en_rps_params).replace("+", "%20").replace("%27", "%22")
                response = self.__http[u_type].delete(url=f"{self.url}{uri}?{params_str}", headers=headers,
                                                      timeout=self.__timeout, verify=False, cookies=self.__cookie)

            else:
                params_str = urlencode(en_rps_params).replace("+", "%20").replace("%27", "%22")
                response = self.__http[u_type].get(url=f"{self.url}{uri}?{params_str}", headers=headers,
                                                   timeout=self.__timeout, verify=False, cookies=self.__cookie)

            LOG.info(f"response: {response.text}")

            if response.status_code == requests.codes.ok:
                print(f"response_time: {response.elapsed.total_seconds()}")
                print(f"response: \n{response.json()}")
                if "ciphertext" in response.json():
                    # 解密结果
                    ciphertext = response.json()["ciphertext"]
                    decrypt_response = self.node_server.decryption(self.node_server.package(en_text=ciphertext))
                    print("明文response:", decrypt_response)
                    return decrypt_response
                else:
                    return response.text
            else:
                print("响应状态码:", response.status_code)
                return str(f"响应状态码:{response.status_code}")

        except Exception as e:
            LOG.error(e)

    def simple_call(self, method: str, uri: str, params: dict = None, u_type: str = "default", files: bytes = None):
        """
        精简接口请求
        :param method:
        :param uri:
        :param params:
        :param u_type:
        :return:
        """
        method = method.upper()
        if method not in ["GET", "POST", "PUT", "DELETE"]:
            raise ValueError("method must be GET or POST or PUT or DELETE.")

        if params is None or not isinstance(params, dict):
            params = {}

        # 请求头添加cookie
        headers = self.__headers

        # 加密判断
        if self.node_server.is_encryption(self.host, uri):
            if params == {}:
                params = '{}'
            en_rps = self.node_server.encryption(self.node_server.package(param=params))
            if en_rps['code'] == 0:
                en_rps_params = {"ciphertext": en_rps['msg']}
            else:
                en_rps_params = params
        else:
            en_rps_params = params

        # 请求
        if method == "POST":
            time.sleep(3)
            # 兼容文件上传格式请求
            if files:
                response = self.__http[u_type].post(url=f"{self.url}{uri}", files=files, verify=False,
                                                    cookies=self.__cookie)
            else:
                response = self.__http[u_type].post(url=f"{self.url}{uri}", json=en_rps_params, headers=headers,
                                                    timeout=self.__timeout, verify=False, cookies=self.__cookie)

        elif method == "PUT":
            response = self.__http[u_type].put(url=f"{self.url}{uri}", json=en_rps_params, headers=headers,
                                               timeout=self.__timeout, verify=False, cookies=self.__cookie)

        elif method == "DELETE":
            params_str = urlencode(en_rps_params).replace("+", "%20").replace("%27", "%22")
            response = self.__http[u_type].delete(url=f"{self.url}{uri}?{params_str}", headers=headers,
                                                  timeout=self.__timeout, verify=False, cookies=self.__cookie)

        else:
            params_str = urlencode(en_rps_params).replace("+", "%20").replace("%27", "%22")
            response = self.__http[u_type].get(url=f"{self.url}{uri}?{params_str}", headers=headers,
                                               timeout=self.__timeout, verify=False, cookies=self.__cookie)

        if response.status_code == requests.codes.ok:
            if "ciphertext" in response.json():
                # 解密结果
                ciphertext = response.json()["ciphertext"]
                decrypt_response = self.node_server.decryption(self.node_server.package(en_text=ciphertext))
                print("明文response:", decrypt_response)
                return decrypt_response
            else:
                return response.text
        else:
            return "{}"

    def sign_out(self, uri, u_type: str = "default"):
        """
        登出
        :param uri:
        :param u_type:
        :return:
        """
        headers = self.__headers
        self.__http[u_type].post(url=f"{self.url}{uri}", headers=headers, timeout=self.__timeout)


class NodeService(object):
    __timeout = config.timeout
    __http = requests.session()
    __headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/80.0.3987.149 Safari/537.36"
    }

    def __init__(self, host: str, version: str):
        """
        初始化
        :param host:
        """
        if not isinstance(host, str) or host == "":
            raise ValueError("host must be string, port must be greater than 0 and  less than 65536.")
        self.url = f"{host}"
        self.version = version
        self.__http = requests.session()
        LOG.info(self.url)

    def secret(self, params):
        """
        登录加密
        :param params:
        :return:
        """
        secret_rps = self.__http.post(url=f"{self.url}/secret", json=params, verify=False)
        return secret_rps.json()

    def encryption(self, params):
        """
        加密
        :param params:
        :return:
        """
        print("明文params:", params['params'])
        en_rps = self.__http.post(url=f"{self.url}/encryption", json=params, verify=False)
        return en_rps.json()

    def decryption(self, params):
        """
        解密
        :param params:
        :return:
        """
        de_rps = self.__http.post(url=f"{self.url}/decryption", json=params, verify=False).json()
        if de_rps['code'] == 0:
            return json.dumps(de_rps['msg'])
        else:
            return de_rps

    def is_encryption(self, host, uri):
        """
        判断是否加密uri
        """
        if api_dict:
            for path in api_dict[host]:
                if f"{self.version}{uri}" == path["path"]:
                    if path["path"] == f"{self.version}/user/auth/status":
                        return False
                    else:
                        return True
        return False

    @staticmethod
    def package(param=None, en_text=None):
        """
        封装加密请求数据
        :param param:
        :param en_text:
        """
        try:
            if param:
                if param == "{}":
                    param = {}
                params = {"mode": mode, "key": secret, "iv": nonce, "params": param}
                return params
            elif en_text:
                params = {"mode": mode, "key": secret, "iv": nonce, "enText": en_text}
                return params

        except Exception as e:
            print(e)
            print("登录接口未加密")


class BaseHttpService(object):
    __timeout = 20
    __headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/80.0.3987.149 Safari/537.36"
    }

    def __init__(self, host):
        self.__http = requests.session()
        self.url = f"{host}"

    def call(self, method: str, uri: str, params: dict = None):
        """
        接口请求
        :param method:
        :param uri:
        :param params:
        :param u_type:
        :return:
        """
        LOG.info(f"{method} | {uri} | {json.dumps(params)}")
        try:
            method = method.upper()
            if method not in ["GET", "POST"]:
                raise ValueError("method must be GET or POST.")

            if params is None or not isinstance(params, dict):
                params = {}

            # 请求
            if method == "POST":
                response = self.__http.post(url=f"{self.url}{uri}", json=params, headers=self.__headers,
                                            timeout=self.__timeout)
                time.sleep(3)
            else:
                params_str = urlencode(params).replace("+", "%20").replace("%27", "%22")
                response = self.__http.get(url=f"{self.url}{uri}?{params_str}", headers=self.__headers,
                                           timeout=self.__timeout)

            LOG.info(f"response: {response.text}")
            return response.content

        except Exception as e:
            LOG.error(e)
