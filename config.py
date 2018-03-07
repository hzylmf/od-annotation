# -*- coding: UTF-8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))

# Flask
DEBUG = True

# 日志配置
LOG_DIR = os.path.join(basedir, 'logs')
LOG_FORMAT = '%(asctime)s %(levelname)s: %(message)s [in %(module)s.%(funcName)s:%(lineno)d]'
LOG_LEVEL = 'info'

# 节点配置
PID_FILE = 'od-annotation.pid'
SERVER_PORT = 5000


