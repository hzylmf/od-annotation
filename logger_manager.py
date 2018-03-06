# -*- coding: UTF-8 -*-


import logging
import config
import os

if not os.path.exists(config.LOG_DIR):
    os.makedirs(config.LOG_DIR)

__formatter = logging.Formatter(config.LOG_FORMAT)
__level = logging._nameToLevel[config.LOG_LEVEL.upper()]

# 主节点日志
__mynahc_log_file = os.path.join(config.LOG_DIR, 'mynah_controller.log')
__mynahc_handler = logging.FileHandler(__mynahc_log_file)
__mynahc_handler.setFormatter(__formatter)

controller_logger = logging.getLogger('mynah_controller')
controller_logger.addHandler(__mynahc_handler)
controller_logger.setLevel(__level)

# 计算节点日志
__mynahd_log_file = os.path.join(config.LOG_DIR, 'mynah_daemon.log')
__mynahd_handler = logging.FileHandler(__mynahd_log_file)
__mynahd_handler.setFormatter(__formatter)

daemon_logger = logging.getLogger('mynah_daemon')
daemon_logger.addHandler(__mynahd_handler)
daemon_logger.setLevel(__level)


# 系统日志
__sys_log_file = os.path.join(config.LOG_DIR, 'sys.log')
__sys_handler = logging.FileHandler(__sys_log_file)
__sys_handler.setFormatter(__formatter)
# flask 日志
__default = logging.getLogger('werkzeug')
__default.addHandler(__sys_handler)
__default.setLevel(__level)
# requests 日志
__requests = logging.getLogger('requests')
__requests.addHandler(__sys_handler)
__requests.setLevel(__level)
