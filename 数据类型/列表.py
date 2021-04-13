"""
Python3 列表
序列是 Python 中最基本的数据结构。

序列中的每个值都有对应的位置值，称之为索引，第一个索引是 0，第二个索引是 1，依此类推。

Python 有 6 个序列的内置类型，但最常见的是列表和元组。

列表都可以进行的操作包括索引，切片，加，乘，检查成员。

此外，Python 已经内置确定序列的长度以及确定最大和最小的元素的方法。

列表是最常用的 Python 数据类型，它可以作为一个方括号内的逗号分隔值出现。

列表的数据项不需要具有相同的类型

创建一个列表，只要把逗号分隔的不同的数据项使用方括号括起来即可。如下所示：

list1 = ['Google', 'Runoob', 1997, 2000]
list2 = [1, 2, 3, 4, 5 ]
list3 = ["a", "b", "c", "d"]
list4 = ['red', 'green', 'blue', 'yellow', 'white', 'black']
"""

'''
Python列表函数&方法
Python包含以下函数:

序号	函数
1	len(list)列表元素个数
2	max(list)返回列表元素最大值
3	min(list)返回列表元素最小值
4	list(seq)将元组转换为列表
Python包含以下方法:
序号	方法
1	list.append(obj)在列表末尾添加新的对象
2	list.count(obj)统计某个元素在列表中出现的次数
3	list.extend(seq)在列表末尾一次性追加另一个序列中的多个值（用新列表扩展原来的列表）
4	list.index(obj)从列表中找出某个值第一个匹配项的索引位置
5	list.insert(index, obj)将对象插入列表
6	list.pop([index=-1])移除列表中的一个元素（默认最后一个元素），并且返回该元素的值
7	list.remove(obj)移除列表中某个值的第一个匹配项
8	list.reverse()反向列表中元素
9	list.sort( key=None, reverse=False)对原列表进行排序
10	list.clear()清空列表
11	list.copy()复制列表
'''


'''
list = ['Google', 'Runoob', 1997, 2000]
1   更新列表：list[2] = 2001  其它方式 append() 方法
2   删除列表元素:del list[2]  其它方式 remove()、	list.pop([index=-1]) 方法
'''