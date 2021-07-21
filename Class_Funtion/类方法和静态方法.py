'''
类方法、实例方法、静态方法对比
1.类方法的第一个参数是类对象是类对象 cls进而去引用类对象的属性和方法，必须用装饰器@classmethod来修饰
2.实例方法的第一个参数必须是self，通过这个self可以去引用类属性和实例属性，若存在相同名称实例属性和类属性的话，实例属性的优化最高
3.静态方法不需要定义额外的参数，若是要引用属性的话则可以通过类对象或者是实例对象去引用即可，必须用装饰器@staticmethod来修饰
'''


# 普通类及实例方法
class Person(object):
    # 类属性
    name = '小花'

    # 此时叫"实例方法"
    def __init__(self, age):
        print(age)
        pass

    pass


# 实例类，得到一个对象p
r = Person(18)


# class类和类方法
class People(object):
    # 类属性
    country = 'China'

    @classmethod  # 类方法用classmethod进行修饰,第一个参数一般为cls
    # 此时叫"类方法"
    def get_country(cls):
        return cls.country  # 访问类属性
        pass

    # 通过类方法修改类属性（实例对象是不能修改类属性的，类属性只能由对象或者类方法进行更改）
    @classmethod
    # 类方法
    def change_country(cls, newcountry):  # 类方法修改类属性
        cls.country = newcountry
        return cls.country

    pass

    # 静态方法
    @staticmethod  # 类对象所拥有的的方法，需要用@staticmethod来表示静态方法，静态方法默认不需要任何参数（也可以传）
    def get_data():
        '''
        静态方法主要用来存放逻辑性代码，本身和类以及实例对象没有交互，
        也就是说，在静态方法中，不会涉及到类中方法和属性的操作，数据资源可以得到有效的充分利用
        :return:
        '''
        return People.country
        pass

    pass


print("静态方法输出↓↓↓")
print(People.get_data())
jt = People()
print(jt.get_data())

# 通过类对象去引用
print("通过类对象去引用↓↓↓")
print(People.get_country())  # 通过类对象去引用

print("通过实例对象去访问↓↓↓")
# 通过实例对象去访问
p = People()
print("实例对象访问 %s" % p.get_country())

print("***修改类属性***")
People.change_country('俄罗斯')
print(People.get_country())
print(People.country)

import time


class TimeTest():
    def __init__(self, hour, min, second):
        self.hour = hour
        self.min = min
        self.second = second

    @staticmethod
    def showTime():
        return time.strftime("%H:%M:%S", time.localtime())
        pass

    pass


# 对象访问
print(TimeTest.showTime())

# 实例化访问
t = TimeTest(2, 10, 15)
print(t.showTime())  # 没有必要通过实例化方式来访问静态方法，因为静态方法一般不会涉及到类中方法和属性的操作
