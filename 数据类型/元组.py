"""
Python3 元组
Python 的元组与列表类似，不同之处在于元组的元素不能修改。

元组使用小括号 ( )，列表使用方括号 [ ]。

元组创建很简单，只需要在括号中添加元素，并使用逗号隔开即可。
"""
'''
1   访问元组:元组可以使用下标索引来访问元组中的值
tup1 = ('Google', 'Runoob', 1997, 2000)
tup2 = (1, 2, 3, 4, 5, 6, 7 )

print ("tup1[0]: ", tup1[0])
print ("tup2[1:5]: ", tup2[1:5])

2   修改元组:元组中的元素值是不允许修改的，但我们可以对元组进行连接组合，如下实例:
tup1 = (12, 34.56)
tup2 = ('abc', 'xyz')

# 以下修改元组元素操作是非法的。
# tup1[0] = 100

# 创建一个新的元组
tup3 = tup1 + tup2
print (tup3)

3   删除元组:元组中的元素值是不允许删除的，但我们可以使用del语句来删除整个元组，如下实例:
#!/usr/bin/python3

tup = ('Google', 'Runoob', 1997, 2000)

print (tup)
del tup
print ("删除后的元组 tup : ")
print (tup)

元组内置函数
Python元组包含了以下内置函数

序号	方法及描述	实例
1	len(tuple)
计算元组元素个数。
>>> tuple1 = ('Google', 'Runoob', 'Taobao')
>>> len(tuple1)  3
>>>
2	max(tuple)
返回元组中元素最大值。
>>> tuple2 = ('5', '4', '8')
>>> max(tuple2) '8'
>>>
3	min(tuple)
返回元组中元素最小值。
>>> tuple2 = ('5', '4', '8')
>>> min(tuple2) '4'
>>>
4	tuple(iterable)
将可迭代系列转换为元组。
>>> list1= ['Google', 'Taobao', 'Runoob', 'Baidu']
>>> tuple1=tuple(list1)
>>> tuple1
('Google', 'Taobao', 'Runoob', 'Baidu')
'''