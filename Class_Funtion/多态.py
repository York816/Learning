'''
多肽：顾名思义就是多种状态、形态，就是同一种行为；对于不同的子类【对象】有不同的行为表现
***要想实现多肽，需满足两个前提条件
1、继承：多肽必须发生在父类和子类之间
2、重写：子类重写父类的方法

多肽的作用；
增加程序的灵活性；增加程序的可扩展性
'''

"""
鸭子类型（duck typing）
在程序设计中，鸭子类型（英语：duck typing）是动态类型的一种风格。在这种风格中，一个对象有效的语义不是由继承自特定的类或者实现
特定的接口，而是由当前方法和属性的集合决定的。“鸭子测试”可以这表表述：“当看到一只鸟走起来像鸭子、游泳起来像鸭子、叫起来也像鸭子，
那么这只鸟就可以被称为鸭子。在鸭子类型中，关注的不是对象的类型本身，而是它是如何使用的”
"""


class Animal(object):
    '''
    父类【基类】
    '''

    def say_who(self):
        print("我是一个动物...")
        pass

    pass


class Duck(Animal):
    '''
    鸭子类——子类【派生类】
    '''

    def say_who(self):
        print("这是一只漂亮的鸭子...")
        pass

    pass


class Dog(Animal):
    '''
      小狗类——子类【派生类】
    '''

    def say_who(self):
        print("这是一只勇敢的狗...")
        pass

    pass


class Cat(Animal):
    '''
      小猫类——子类【派生类】
    '''

    def say_who(self):
        print("这是一只可爱小猫咪...")
        pass

    pass


# duck1 = Duck()
# duck1.say_who()
#
# dog1 = Dog()
# dog1.say_who()
#
# cat1 = Cat()
# cat1.say_who()

class Bird(Animal):
    def say_who(self):
        print("我是一只黄鹂鸟")
        pass

    pass


# 新增一个新的基类
class People():
    def say_who(self):
        pass

    pass


# 继承基类的派生类
class student(People):
    def say_who(self):
        print("我是人类")
        pass

    pass


def commonInvoke(obj):
    '''
    统一调用的方法
    :param obj:对象的实例
    :return:
    '''
    obj.say_who()


listobj = [Duck(), Dog(), Cat(), Bird(), student()]
for item in listobj:
    '''
    循环调用函数
    '''
    commonInvoke(item)
    pass
pass
