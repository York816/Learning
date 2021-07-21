# -*- coding: utf-8 -*-
import re
import time
import pymysql
import config


class ReportAnalysis(object):
    def __init__(self, success_count, tests_run, failure_count, skipped, result_list, project):
        """
        初始化
        :param success_count:运行成功的数目
        :param tests_run:运行测试用例的总数
        :param failure_count:运行失败的数目
        :param skipped:运行跳过的数目
        :param result_list:运行数据
        :param project:项目名称
        """
        self.success_count = success_count
        self.tests_run = tests_run
        self.failure_count = failure_count
        self.skipped = skipped
        self.result_list = result_list
        self.project = project
        self.response_time_list = []
        self.database = config.my_sql
        # 打开数据库连接
        self.db = pymysql.connect(host=self.database['host'], user=self.database['user'],
                                  password=self.database['password'],
                                  database=self.database['database'], port=self.database['port'])

        # 使用cursor()方法获取操作游标
        self.cursor = self.db.cursor()

    def success_rate(self):
        """
        成功率分析
        """
        print("接口调用成功率:%.2f" % float((self.tests_run - (self.failure_count + self.skipped)) / self.tests_run * 100))
        return "%.2f" % float((self.tests_run - (self.failure_count + self.skipped)) / self.tests_run * 100)

    def coverage_rate(self):
        """
        覆盖率分析
        """
        sql = """SELECT COUNT(DISTINCT(uri)) FROM test_data WHERE project_name='%s';""" % self.project
        self.cursor.execute(sql)
        num = self.cursor.fetchall()
        print("单元测试覆盖率:%.2f" % float(num[0][0] / 609 * 100))
        return "%.2f" % float(num[0][0] / 609 * 100)

    def truncate_table(self):
        """
        清空临时数据库
        """
        sql = """DELETE FROM test_api_rt WHERE id IS NOT NULL;"""
        self.cursor.execute(sql)
        self.db.commit()

    def response_time_cleaning(self):
        """
        接口数据处理&写入数据库
        """
        # 清空数据库
        self.truncate_table()

        sql = """INSERT INTO test_api_rt (project_name,class_name,test_case_name,method,uri,rt)""" \
              """VALUES (%s,%s,%s,%s,%s,%s);"""

        # 数据格式：
        data_info = []

        # 正则表达式
        res_t = r'response_time: ([\d+\.]+)'
        res_u = r"'uri: (.*?)', '"
        res_m = r"'method: (.*?)', '"

        for case in self.result_list:
            if case[4] == "成功":
                rt_list = re.findall(res_t, str(case[5]), re.S | re.M)
                uri_list = re.findall(res_u, str(case[5]), re.S | re.M)
                method_list = re.findall(res_m, str(case[5]), re.S | re.M)
                if rt_list and uri_list:
                    rt = "%.2f" % (float(rt_list[-1]))
                    if method_list[-1] == "POST":
                        # print("POST1", (self.project, case[0], case[1][:-2], "POST", uri_list[-1], rt))
                        data_info.append((self.project, case[0], case[1][:-2], "POST", uri_list[-1], rt))
                    elif method_list[-1] == "GET":
                        # print("GET1", (self.project, case[0], case[1][:-2], "GET", uri_list[-1], rt))
                        data_info.append((self.project, case[0], case[1][:-2], "GET", uri_list[-1], rt))
                else:
                    print("正则匹配不到:", case[5])

        # 批量插入使用executement
        try:
            self.cursor.executemany(sql, data_info)
        except Exception as e:
            self.db.rollback()
            print("执行MySQL: %s 时出错：%s" % (sql, e))

        print("已经插入完成")
        # 统一提交
        self.db.commit()

    def response_time_analysis(self):
        """
        接口分组延迟情况分析
        """
        sql1 = """SELECT uri,method,rt FROM test_api_rt WHERE rt>=1 AND rt<=2 group by uri,method ORDER BY rt ASC;"""
        sql2 = """SELECT uri,method,rt FROM test_api_rt WHERE rt>=2 AND rt<=3 group by uri,method ORDER BY rt ASC;"""
        sql3 = """SELECT uri,method,rt FROM test_api_rt WHERE rt>3 group by uri,method ORDER BY rt ASC;"""
        sql_list = [sql1, sql2, sql3]
        for sql in sql_list:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            self.response_time_list.append(list(results))

        rt_str = ""
        for rt in range(len(self.response_time_list)):
            for url in self.response_time_list[rt]:
                if rt == 0:
                    rt_str += f"{str(url[2]).ljust(4, '0')}s\t{str(url[1]).ljust(4, ' ')}\t{url[0]}\n                "
                elif rt == 1:
                    rt_str += f"{str(url[2]).ljust(4, '0')}s\t{str(url[1]).ljust(4, ' ')}\t{url[0]}\n                "
                elif rt == 2:
                    rt_str += f"{str(url[2]).ljust(4, '0')}s\t{str(url[1]).ljust(4, ' ')}\t{url[0]}\n                "
        print(rt_str)
        return self.response_time_list, rt_str

    def report_analysis(self):
        """
        报告数据分析&数据存档
        """
        success_rate = self.success_rate()
        coverage_rate = self.coverage_rate()
        self.response_time_cleaning()
        rt_rate, rt_str = self.response_time_analysis()

        sql = """INSERT INTO test_report_analysis (project_name,testsrun_count,success_count,failure_count,
                skipped_count,success_rate,coverage_rate,rt_rate)""" \
              """VALUES ("%s","%s","%s","%s","%s","%s","%s","%s");""" % (
                  self.project, self.tests_run, self.success_count, self.failure_count, self.skipped, success_rate,
                  coverage_rate, rt_rate)
        self.cursor.execute(sql)
        self.db.commit()
        # 关闭游标
        self.cursor.close()
        # 关闭数据库连接
        self.db.close()
        return success_rate, coverage_rate, rt_str


if __name__ == '__main__':
    ...