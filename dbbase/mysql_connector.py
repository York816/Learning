import mysql.connector


class DbTest(object):
    """
    connect mysql
    """
    pass

    def __init__(self):
        mydb = mysql.connector.connect(
            host="192.168.30.98",
            user="crm_system_v5",
            passwd="gZxL6mjsru07mRuX"
        )
        mycursor = mydb.cursor()
        mycursor.execute("SHOW DATABASES")  # 输出所有数据库列表：
        for x in mycursor:
            print(x)
        pass

    pass

    def finddata(self):
        pass

    pass


if __name__ == '__main__':
    print(DbTest())
