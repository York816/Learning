import random
import re
import os
from classes.temp import Temp
import config


def random_str(num: int):
    """
    生成一个随机字符串
    :param num: 字符串个数
    :return: 随机字符串
    """

    str_value = "qa_test" + ''.join(random.sample(['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n',
                                                   'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f', 'e', 'd', 'c', 'b', 'a'],
                                                  num))

    return str_value


def random_phone():
    """ 生成随机手机号 """

    phone = "131" + str(random.randint(100000000, 999999999))[1:]

    return phone


def replace_data(replace_str: str):
    """
    :param replace_str: 需要替换的字符串
    :return: 替换后的字符串
    """
    expression = r"#(.+?)#"
    # 根据是否匹配到要替换的数据，来决定要不要进入循环
    while re.search(expression, replace_str):
        # 匹配一个需要替换的内容
        res = re.search(expression, replace_str)
        # 获取待替换的内容
        data = res.group()
        # 获取需要替换的字段
        key = res.group(1)

        # try:
        #     # 配置文件找可以调换的内容
        #     replace_str = replace_str.replace(data, config.test_data[key])
        # except KeyError:
        #     # 如果配置文件中找不到，报错了，则去Temp的属性中找对应的值进行替换
        replace_str = replace_str.replace(data, getattr(Temp, key))

    return replace_str
