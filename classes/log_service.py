import Learning.common as common
import Learning.config as config
import logging


class Log(object):

    @staticmethod
    def get_logger(logger_name=None):
        """
        创建logger
        :param logger_name:
        :return:
        """
        level = config.log_level
        log_path = config.log_path
        common.check_dir_path(log_path)
        log_file = f"{log_path}/{common.get_time('%Y%m%d')}.log"

        logger = logging.getLogger(logger_name)
        # 设置日志等级
        logger.setLevel(level)
        fhandler = logging.FileHandler(log_file, encoding='utf8')
        fhandler.setLevel(level)
        chandler = logging.StreamHandler()
        chandler.setLevel(level)
        formatter = logging.Formatter("%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s")
        chandler.setFormatter(formatter)
        fhandler.setFormatter(formatter)
        logger.addHandler(chandler)
        logger.addHandler(fhandler)

        return logger
