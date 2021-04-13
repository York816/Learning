"""
Python3 字典
字典是另一种可变容器模型，且可存储任意类型对象。

字典的每个键值 key=>value 对用冒号 : 分割，每个对之间用逗号(,)分割，整个字典包括在花括号 {} 中 ,格式如下所示：
d = {key1 : value1, key2 : value2, key3 : value3 }
键必须是唯一的，但值则不必。

值可以取任何数据类型，但键必须是不可变的，如字符串，数字。
dict = {'name': 'runoob', 'likes': 123, 'url': 'www.runoob.com'}

1   创建字典：
dict1 = { 'abc': 456 }
dict2 = { 'abc': 123, 98.6: 37 }

2   访问字典里的值
把相应的键放入到方括号中，如下实例:

实例
#!/usr/bin/python3

dict = {'Name': 'Runoob', 'Age': 7, 'Class': 'First'}

print ("dict['Name']: ", dict['Name'])
print ("dict['Age']: ", dict['Age'])
以上实例输出结果：

dict['Name']:  Runoob
dict['Age']:  7

3   修改字典
向字典添加新内容的方法是增加新的键/值对，修改或删除已有键/值对如下实例:
dict = {'Name': 'Runoob', 'Age': 7, 'Class': 'First'}

dict['Age'] = 8               # 更新 Age
dict['School'] = "菜鸟教程"  # 添加信息

print ("dict['Age']: ", dict['Age'])
print ("dict['School']: ", dict['School'])
以上实例输出结果：
dict['Age']:  8
dict['School']:  菜鸟教程


"""