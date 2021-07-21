# coding=utf-8
import Learning.config as config
import csv
import datetime
import hashlib
import json
import os
import re
import requests
import time
import unittest
import uuid
import urllib3
from classes.sql_service import MySqlClass
from lxml import etree

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ComplexEncoder(json.JSONEncoder):
    """
    重写json.dumps时候default方法，处理datetime为字符串格式
    """

    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(o, datetime.date):
            return o.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, o)


def csv_to_dict(filename, path):
    """
    csv 数据转化为 dict 数据
    :param filename:
    :param path:
    :return:
    """
    filename = filename if filename.endswith(".csv") else f"{filename}.csv"
    path = f"{path}{filename}" if path.endswith("/") else f"{path}/{filename}"

    with open(path, "r") as file:
        dict_reader = csv.DictReader(file)

        list_dict = list(map(lambda item: dict(item), list(dict_reader)))

        for value in list_dict:
            value["method"] = value["method"].strip()
            value["uri"] = value["uri"].strip()
            params = value["params"].strip()
            value["params"] = json.loads(params) if is_json(params) else {}
            response_key = value["response_key"].split(",") if value.get("response_key") else []
            value["response_key"] = list(map(lambda item: item.strip(), response_key))

        return list_dict


def mysql_to_dict(project_name, class_name, test_case_name):
    """
    从数据库获取数据
    :param project_name:
    :param class_name:
    :param test_case_name:
    :return:
    """
    sql = f"SELECT * FROM `test_data` WHERE `project_name` = '{project_name}' AND" \
          f" `class_name` = '{class_name}' AND `test_case_name` = '{test_case_name}';"
    database = config.my_sql
    database["database"] = "autotest"
    service = MySqlClass(database)
    result = service.exec(sql)

    for data in result:
        data["params"] = json_to_dict(data["params"])
        data["response_key"] = list(map(lambda item: item.strip(), data["response_key"].split(",")))

    return result


def mysql_to_dict2(sql_statement=None, data_base=None):
    """
    从数据库获取数据2
    :param sql_statement:
    :param data_base:
    :return:
    """
    sql = sql_statement
    database = config.my_sql
    if data_base is not None:
        database["database"] = data_base
    else:
        database["database"] = "autotest"
    service = MySqlClass(database)
    result = service.exec(sql)

    for data in result:
        data["params"] = json_to_dict(data["params"])
        data["response_key"] = list(map(lambda item: item.strip(), data["response_key"].split(",")))

    return result


def mysql_to_ddt_list(mysql_data):
    """
    数据库字典数据转ddt列表数据
    :param mysql_data:
    :return:
    """
    ddt_list = {}
    for data in mysql_data:
        data["params"] = json_to_dict(data["params"])
        data["response_key"] = list(map(lambda item: item.strip(), data["response_key"].split(",")))
        if data['test_case_name'] in ddt_list:
            ddt_list[data["test_case_name"]].append(data)
        else:
            ddt_list[data["test_case_name"]] = [data]

    return ddt_list


def json_to_dict(msg):
    """
    json字符串转为dict对象
    :param msg:
    :return:
    """
    return json.loads(msg)


def dict_to_json(dict_obj):
    """
    dict对象转为json字符串
    :param dict_obj:
    :return:
    """
    return json.dumps(dict_obj, ensure_ascii=False, cls=ComplexEncoder)


def is_json(msg):
    """
    判断字符串是否为json
    :param msg:
    :return:
    """
    try:
        json.loads(msg)
        return True
    except Exception:

        return False


def is_list(msg):
    """
    判断字符串是否为list
    :param msg:
    :return:
    """
    try:
        json.loads(msg)
        return True
    except Exception:
        return False


def get_timestamp(is_second=True):
    """
    获取时间戳
    :param is_second: 秒 还是 毫秒
    :return:
    """
    return int(time.time()) if is_second is True else int(time.time() * 1000)


def get_time(time_format="%Y-%m-%d %H:%M:%S", seconds=None):
    """
    获取时间戳
    :param time_format: 时间格式
    :param seconds: 时间戳，单位秒
    :return:
    """
    return time.strftime(time_format, time.localtime(seconds))


def check_dir_path(dir_path):
    """
    判断文件夹是否存在，不存在则创建
    :param dir_path:
    :return:
    """
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def get_suite_from_ddt(class_name, case_names=None):
    """
    构造使用ddt的单元测试类的suite
    :param class_name: 单元测试类的类名
    :param case_names: 测试用例方法名
    :return:
    """
    case_names = list(map(lambda item: item.strip(), case_names.split(","))) if case_names else [""]

    test_dict = class_name.__dict__
    test_list = []
    for case in case_names:
        tmp_cases = filter(
            lambda key, value=case: key.startswith("test_") and key.startswith(value) and callable(
                getattr(class_name, key)),
            test_dict
        )
        for tmp_case in tmp_cases:
            test_list.append(class_name(tmp_case))

    suite = unittest.TestSuite()
    suite.addTests(test_list)

    return suite


def unittest_assert(result, assert_code, response_key, check_data, assert_true, assert_equal, expected=None):
    """
    unittest 断言判断
    :param result: 响应结果
    :param assert_code: 目标code值
    :param response_key: 目标keys值
    :param check_data: 从结果获取keys的数据
    :param assert_true: unittest的 self.assertTrue
    :param assert_equal: unittest的 self.assertEqual
    :param expected: 对比某个值，数据格式为{"key": "data.data.msg", "value": "success"}
    :return:
    """
    json_bool = is_json(result)
    assert_true(json_bool, msg=f"响应结果不是json格式，结果为：{result}")
    if json_bool:
        result = json_to_dict(result)
        # 判断返回的code是否与目标值相等
        code = result["code"]
        assert_equal(assert_code, code, msg=f"{assert_code} != {code}")

        # 判断某个目标值是否和期望值一致
        if expected is not None:
            expected_data = json_to_dict(expected)
            expected_value = expected_data["value"]
            expected_key = '["' + '"]["'.join(expected_data["key"].split('.')) + '"]'
            expected_data = eval(f'result{expected_key}')
            assert_equal(expected_value, expected_data, msg=f"目标值不一致，{expected_value} != {expected_data}")

        # 判断返回的参数的key是否与目标值相等
        if response_key and check_data is not None and check_data != "":
            eval_data = eval(f'result{check_data}')

            if isinstance(eval_data, list):
                if eval_data:
                    if not isinstance(eval_data[0], dict):
                        keys = [""]
                    else:
                        keys = list(eval_data[0].keys())
                else:
                    # 如果eval_data is []，则设置
                    keys = [""]
                    response_key = [""]
            elif isinstance(eval_data, dict) and eval_data != {}:
                keys = list(eval_data.keys())
            else:
                keys = [""]
            keys.sort()
            response_key.sort()
            # assert_equal(response_key, keys, msg=f"{response_key} != {keys}")
            assert_true(not (set(response_key) - set(keys)), msg=f"{response_key} != {keys}")


def get_md5(string):
    """
    对字符串进行md5加密
    :param string:
    :return:
    """
    obj = hashlib.md5()
    obj.update(string.encode())
    return obj.hexdigest()


def get_uuid():
    """
    获取uuid
    :return:
    """
    return uuid.uuid4().__str__()


def get_secret_info(url):
    http = requests.session()

    try:
        resp = http.get(url=url, verify=False).content
        text = resp.decode()
        html = etree.HTML(text)

        script = html.xpath("head/script[1]/text()")[0]

        pattern = r"window, document, '([\S\s]*)'"
        result = re.findall(pattern=pattern, string=script)[0]
        result_list = result.split("', '")

        public = result_list[0].split(",")
        api_list = json.loads(result_list[1].replace("&quot;", "\""))

        return {
            "pubKey": public[0],
            "aesMethod": public[1],
            "passphrase": public[2],
            "pid": public[3],
            "apiList": api_list,
        }

    except Exception as e:
        return {
            "code": -1,
            "err": str(e)
        }

    finally:
        http.close()


def write_json(params, path, file_name, encoding=None):
    """
    写入json数据
    :param params:
    :param path:
    :param file_name:
    :param encoding:
    :return:
    """
    if not os.path.exists(path):
        os.makedirs(path)
    with open(f"{path}/{file_name}", "w", encoding=encoding) as write_obj:
        write_obj.write(json.dumps(params, indent=4, ensure_ascii=False))


def get_json(file_path, encoding=None):
    """
    读取json数据
    :param file_path:
    :param encoding:
    :return:
    """
    with open(file_path, "r", encoding=encoding) as read_obj:
        content = read_obj.read()
        data = {} if content == "" else json.loads(content)

        return data


def write_temp(key, value: dict, is_add=False):
    """
    写入或更新数据
    :param key:
    :param value:
    :param is_add:
    :return:
    """
    database = config.my_sql
    database["database"] = "autotest"
    service = MySqlClass(database)

    check_sql = f"SELECT `value` FROM `temp_data` WHERE `key` = '{key}';"
    check_result = service.find_one(check_sql)
    if check_result is None:
        value = dict_to_json(value)
        sql = f"INSERT INTO `temp_data` (`key`, `value`) VALUES ('{key}', '{value}');"
    else:
        if is_add is True:
            origin_value = json_to_dict(check_result[0])
            origin_value.update(value)
            origin_value = dict_to_json(origin_value)
        else:
            origin_value = dict_to_json(value)
        sql = f"UPDATE `temp_data` SET `value` = '{origin_value}' WHERE `key` = '{key}';"
    result = service.save_data(sql)

    return result


def read_temp(key):
    """
    读取数据
    :param key:
    :return:
    """
    sql = f"SELECT `value` FROM `temp_data` WHERE `key` = '{key}';"
    database = config.my_sql
    database["database"] = "autotest"
    service = MySqlClass(database)
    result = service.find_one(sql)

    if result is None:
        return "{}"

    return json_to_dict(result[0])
