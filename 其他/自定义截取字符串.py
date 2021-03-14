def phonehash(phonenum):
    '''
    截取指定字符/长度
    :param phonenum:需要校验字符串
    :return:
    Python提供index 函数，检测字符串中是否包含子字符串,通常表现为 某些特定字符，特定单词；a.index(b, begin, end),a为需要校验字符串，
    b为字符串,begin 为开始截取的字符的下标（默认为0），end结束字符下标（默认为字符长度）
    '''
    str1 = phonenum
    str2 = '@'
    re = str1.index(str2)
    print(re)
    print(str1.index(str2, 2, 10))  # 从下标2位开始找,10结束
    print(str1[:str1.index(str2)])  # 获取 "@"之前的字符(不包含@)  结果 bigemail
    print(str1[str1.index(str2):])  # 获取 "@"之后的字符(包含@)  结果 @linshiyouxiang.net


phonehash('bigemail@linshiyouxiang.net')
