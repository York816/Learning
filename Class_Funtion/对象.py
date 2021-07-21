class Animals(object):
    def __init__(self,name):
        self.name=name
        pass

    def __str__(self):
        return "你的名字是%s"%(self.name)
    pass
A=Animals("小明")
print(A)
