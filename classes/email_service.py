import os
import smtplib
from classes.log_service import Log
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

LOG = Log.get_logger(__name__)


class EmailService(object):

    def __init__(self, host, port, user, token, enable_tls=True):
        """
        初始化
        :param host: 发信服务器 host
        :param port: 发信服务器 port
        :param user: 发信人账户
        :param token: 发信人账户对应授权码
        :param enable_tls: 是否启用tls协议
        """
        self.send_email = smtplib.SMTP(host, port)
        self.send_email.set_debuglevel(0)
        if enable_tls is True:
            self.send_email.starttls()  # 加密协议: TLS
        self.user = user
        self.send_email.login(self.user, token)

    def send(self, receivers, title, content, file_paths=None):
        """
        发送邮件
        :param receivers:
        :param title:
        :param content:
        :param file_paths:
        :return:
        """
        # 创建带附件的实例
        message = MIMEMultipart()
        message["from"] = self.user
        message["to"] = receivers
        message["subject"] = title

        # 邮件正文
        message.attach(MIMEText(content, "plain", "UTF-8"))

        # 若存在附件，则带上附件
        if file_paths is not None:
            file_paths = file_paths.replace("/", "\\")
            file_paths = list(map(lambda item: item.strip(), file_paths.split(",")))
            for file_path in file_paths:
                # 判断文件是否存在
                if not os.path.exists(file_path):
                    raise FileNotFoundError(f"can not found {file_path}")

                # 获取文件名
                file_path_name = file_path.split("\\")[-1]

                # 邮件添加附件
                with open(file_path, "rb") as file:
                    file_base64 = file.read()
                    att = MIMEText(file_base64, "base64", "UTF-8")
                    att["Content-Type"] = "application/octet-stream"
                    att.add_header("Content-Disposition", "attachment", filename=("GBK", "", file_path_name))

                    message.attach(att)
        try:
            LOG.info("发送邮件")
            self.send_email.sendmail(self.user, receivers.replace(" ", "").split(","), message.as_string())
        except Exception as e:
            LOG.error(e)
        finally:
            LOG.info("释放邮件对象")
            self.send_email.quit()
