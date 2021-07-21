import logging
import os
import json
import uuid

# 项目的绝对路径
project_path = os.path.dirname(os.path.dirname(__file__))

# 测试数据文件夹绝对路径
data_path = f"{project_path}/data"
# 测试用例文件夹绝对路径
test_cases_path = f"{project_path}/test_cases"
# 报告文件夹相对路径
report_path = "./report"
# 测试图片文件夹绝对路径
image_path = f"{project_path}/data/image"
# 日志文件夹绝对路径
log_path = f"{project_path}/log"
# 日志等级
log_level = logging.INFO

# 超时时间
timeout = 1000
# 测试环境
test_environment = os.getenv("TEST_ENVIRONMENT", "stg")
# 加密地址
node_host = os.getenv("NODE_HOST", "http://192.168.30.126:7001")
# 执行id
operation_id = uuid.uuid1().__str__()
# 环境变量
environment = os.getenv("ENVIRONMENT", "local")

crm = {
    "protocol": os.getenv("PROTOCOL", "https"),
    "admin_host": os.getenv("ADMIN_HOST", "crm-saas-admin-dev.songmao.tech"),
    "client_host": os.getenv("CLIENT_HOST", "crm-saas-client-dev.songmao.tech"),
    "sales_host": os.getenv("SALES_HOST", "crm-saas-admin-dev.songmao.tech"),
    "port": int(os.getenv("PORT", 443)),
    "version": os.getenv("VERSION", "/v2")
}

crm_pre = {
    "protocol": os.getenv("PROTOCOL", "https"),
    "admin_host": os.getenv("ADMIN_HOST", "crm-saas-admin-stg.songmao.tech"),
    "client_host": os.getenv("CLIENT_HOST", "crm-saas-client-stg.songmao.tech"),
    "sales_host": os.getenv("SALES_HOST", "crm-saas-admin-stg.songmao.tech"),
    "port": int(os.getenv("PORT", 443)),
    "version": os.getenv("VERSION", "/v2")
}

crm_vip = {
    "protocol": os.getenv("PROTOCOL", "https"),
    "admin_host": os.getenv("ADMIN_HOST", "v5-crm-admin-dev.songmao.tech"),
    "sales_host": os.getenv("SALES_HOST", "v5-crm-sales-dev.songmao.tech"),
    "client_host": os.getenv("CLIENT_HOST", "v5-crm-client-dev.songmao.tech"),
    "admin_params": json.loads(os.getenv("ADMIN_PARAMS", '{"email":"0005@qa.test","password":"qatest1*"}')),
    "admin_uuid": os.getenv("ADMIN_UUID", 'R1507248'),
    "sales_params": json.loads(os.getenv("SALES_PARAMS", '{"email":"q3@qq.com","password":"qatest1*"}')),
    "sales_uuid": os.getenv("SALES_UUID", 'Q3194570'),
    "client_params": json.loads(os.getenv("CLIENT_PARAMS", '{"email":"q3@qq.com","password":"qatest1*"}')),
    "client_uuid": os.getenv("CLIENT_UUID", 'F5897146'),
    "port": int(os.getenv("PORT", 443))
}

crm_v5_pre = {
    "protocol": os.getenv("PROTOCOL", "https"),
    "admin_host": os.getenv("ADMIN_HOST", "v5-crm-admin-stg.songmao.tech"),
    "client_host": os.getenv("CLIENT_HOST", "v5-crm-client-stg.songmao.tech"),
    "sales_host": os.getenv("SALES_HOST", "v5-crm-sales-stg.songmao.tech"),
    "port": int(os.getenv("PORT", 443)),
    "version": os.getenv("VERSION", "/v2"),
    # "admin_params": json.loads(os.getenv("ADMIN_PARAMS", '{"email":"test@admin.com","password":"abc123"}')),
    "server_id": os.getenv("SERVER_ID", "cedb-64d22c11e"),
}

ou_trade = {
    "protocol": os.getenv("PROTOCOL", "http"),
    "client_host": os.getenv("CLIENT_HOST", "appb28f2603a25d-social-sz-ct.songmao.tech"),
    "client_params": json.loads(os.getenv("CLIENT_PARAMS", '{"uemail":"99@qq.com","upassword":"a123456"}')),
    "trade_account": json.loads(os.getenv("TRADE_ACCOUNT", "2089111428")),
    "trade_account_pwd": os.getenv("TRADE_ACCOUNT_PWD", "a123456"),
    "port": int(os.getenv("PORT", 80))
}
"""
新增intrade接口配置
"""

in_trade = {
    "protocol": os.getenv("IN_TRADE_PROTOCOL", "https"),
    "host": os.getenv("IN_TRADE_HOST", "intrade-app-node-stg.songmao.tech"),
    "port": int(os.getenv("IN_TRADE_PORT", 443)),
    "email": os.getenv("IN_TRADE_EMAIL", "t1@t1.com"),    #Sam账号
    "password": os.getenv("IN_TRADE_PASSWORD", "!a1b2c3!d45e6f!"),  # Sam密码
    # "email": os.getenv("IN_TRADE_EMAIL", "testuser1@qq.com"),  # Luffi账号
    # "password": os.getenv("IN_TRADE_PASSWORD", "renzhejianren1@"),  # Luffi密码
    "phone": os.getenv("IN_TRADE_PHONE", "1234"),
    "phone_code": os.getenv("IN_TRADE_PHONE_CODE", "+1"),
    "version": os.getenv("IN_TRADE_API_VERSION", "/v1"),
    "device_id": os.getenv("IN_TRADE_DEVICE_ID", "19e5c9b9f6104d6"),
}

my_sql = {
    "host": os.getenv("SQL_HOST", "192.168.30.98"),
    "port": int(os.getenv("SQL_PORT", 3306)),
    "user": os.getenv("SQL_USER", "crm_system_v4"),
    "password": os.getenv("SQL_PASSWORD", "gZxL6mjsru07mRuX"),
    "database": "autotest"
}

email = {
    "host": os.getenv("EMAIL_HOST", "smtp.office365.com"),
    "port": int(os.getenv("EMAIL__PORT", 587)),
    "user": os.getenv("EMAIL__USER", "notice@songmao.tech"),
    "token": os.getenv("EMAIL__TOKEN", "Rob42993"),
    "receiver": os.getenv("RECEIVER", "luffi.yang@songmao.tech")  # 调试
}

__all__ = [
    "project_path",
    "data_path",
    "test_cases_path",
    "report_path",
    "log_path",
    "log_level",
    "timeout",
    "crm",
    "my_sql",
    "email",
]

version = "v2"
