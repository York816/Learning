class D(object):
    def eat(self):
        print("D中的eat")
        pass

class B(D):
    def eat(self):
        print("B中的eat")

class C(D):
    def eat(self):
        print("C中的eat")

class A(B,C):
    pass
a=A()
a.eat()
print(A.__mro__) #可显示类的依次继承关系
# 先在A类中找，找不到就去B类中找，B类中没有，就去C类中找，C类中没有，再到D类中找，D类中没有，就到超类中找，超类没有就报错。