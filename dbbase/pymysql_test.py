import pymysql

# 打开数据库连接
db = pymysql.connect(host="192.168.30.98",
                     user="crm_system_v5",
                     password="gZxL6mjsru07mRuX",
                     db="crm_v5_api_fund",
                     port=3306)
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
cursor.execute("SHOW DATABASES")  # 输出所有数据库列表：
for x in cursor:
    print(x)
pass
# 关闭数据库连接
db.close()
