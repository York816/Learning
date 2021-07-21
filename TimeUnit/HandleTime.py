import time


class TimeMethod(object):
    def __init__(self):
        pass

    pass

    def time_stamp(self, level):
        t = time.time()
        if level == 't':  # 原始时间戳
            return t
        if level == 's':  # 秒级时间戳
            return int(t)
        if level == 'ms':  # 毫秒级时间戳
            return int(round(t * 1000))
        if level == 'us':
            return int(round(t * 1000000))  # 微秒级时间戳
        if level == "localtime":
            return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        else:
            return "Level Error"
        pass

    pass


if __name__ == '__main__':
    print(TimeMethod().time_stamp(level="t"))
    print(TimeMethod().time_stamp(level="s"))
    print(TimeMethod().time_stamp(level="us"))
    print(TimeMethod().time_stamp(level="localtime"))
    print(TimeMethod().time_stamp(level="xxx"))
