import pymysql


class MySqlClass(object):

    def __init__(self, database):
        """
        初始化
        :param database:
        """
        self.db = pymysql.connect(
            host=database["host"],
            port=database["port"],
            user=database["user"],
            password=database["password"],
            database=database["database"],
            charset="utf8"
        )
        self.cursor = self.db.cursor()

    def exec(self, sql):
        """
        :param sql:
        :return:
        """
        try:
            self.cursor.execute(sql)
            fields = self.cursor.description
            all_result = self.cursor.fetchall()

            fields = list(map(lambda item: item[0], fields))

            data = list()
            for result in list(all_result):
                data.append(dict(zip(fields, result)))

            return data
        except Exception as e:
            raise e
        finally:
            self.close()

    def find_one(self, sql):
        """
        获取查询出来的第一条数据
        :param sql: 查询sql语句
        :return: 查询到的第一条数据
        """
        try:
            self.cursor.execute(sql)
            data = self.cursor.fetchone()
            return data
        except Exception as e:
            raise e
        finally:
            self.close()

    def save_data(self, sql):
        """
        保存数据
        :param sql:
        :return:
        """
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            raise e
        finally:
            self.close()

    def insert_data(self, insert_sql, data):
        """
        批量添加数据
        :param insert_sql: 批量添加数据的伪sql语句，如：
        "INSERT INTO test_report (case_id,result,start_time,duration,operation_id) VALUES (%s,%s,%s,%s,%s)"
        :param data: 待添加的数据，格式如:

        :return:
        """
        try:
            self.cursor.executemany(insert_sql, data)
            self.db.commit()
        except Exception as e:
            raise e
        finally:
            self.close()

    def close(self):
        """
        断开游标与数据库连接
        :return:
        """
        self.cursor.close()
        self.db.close()
