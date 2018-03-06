# -*- coding: UTF-8 -*-
import codecs
import hashlib
import traceback
import os

import config
from logger_manager import controller_logger as logger
from utils.db_helper import DBHelper


def validate_request(ip, url):
    return True


def validate_user(username, password):
    """ 
    @summary: 校验用户名和密码
    @param username: 用户名
    @param password: 密码
    @return: True/False
    """
    db = None
    count = 0
    try:
        db = DBHelper()
        sql = "select count(*) from user_list where username=%s and password=%s"
        data = db.query_one(sql, (username, hashlib.sha256(str(password).encode('utf-8')).hexdigest()))
        count = data[0]
    except Exception as e:
        logger.debug('validate user failure:' + str(e) + '. ' + traceback.format_exc())
        raise
    finally:
        if db:
            db.release()
    return count == 1


def check_user(username):
    """ 
    @summary: 校验用户名和密码
    @param username: 用户名
    @return: True/False
    """
    db = None
    count = 0
    try:
        db = DBHelper()
        sql = "select count(*) from user_list where username=%s"
        data = db.query_one(sql, username)
        count = data[0]
    except Exception as e:
        logger.debug('check user failure:' + str(e) + '. ' + traceback.format_exc())
        raise
    finally:
        if db:
            db.release()

    return count == 1


# 保存进程PID到PID文件
def save_pid(path, pid):
    with open(path, 'w') as fp:
        fp.write(str(pid))


# 启动服务进程
def start_service(func, pid_file):

    pid = os.fork()
    if pid == 0:
        func()
    else:
        # saved PID of child process
        logger.info('controller process started at PID: ' + str(pid))
        save_pid(pid_file, pid)


# 关闭服务进程
def shutdown_service(pid_path):
    command = 'kill -9 `cat '+pid_path+'`;rm -f '+pid_path
    os.system(command)
