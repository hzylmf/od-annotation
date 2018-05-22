# -*- coding: UTF-8 -*-
import codecs
import hashlib
import traceback
import os
import json
import random

import config
from logger_manager import controller_logger as logger
from utils.db_helper import DBHelper
from  utils import xml2dict


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


# 非daemon方式启动服务端
def start_service(func, pid_file):
    pid = os.getpid()
    # saved PID
    logger.info('controller process started at PID: ' + str(pid))
    save_pid(pid_file, pid)
    func()


# daemon方式启动服务端
def start_daemon_service(func, pid_file):
    pid = os.fork()
    if pid == 0:
        func()
    else:
        # saved PID of child process
        logger.info('controller process started at PID: ' + str(pid))
        save_pid(pid_file, pid)


# 关闭服务进程
def shutdown_service(pid_path):
    command = 'kill -9 `cat ' + pid_path + '`;rm -f ' + pid_path
    os.system(command)


def get_labels():
    label_file = codecs.open('annotation/label_config.txt', mode='r', encoding='utf-8')
    lines = label_file.readlines()
    label_file.close()
    labels = []
    for line in lines:
        if line.startswith('#'): continue
        values = line.strip().split(':')
        label_name = values[0].strip()
        label_desc = values[1].strip()
        label = dict()
        label['name'] = label_name
        label['desc'] = label_desc
        labels.append(label)
    return labels


def convert_to_voc2007(file_path='annotation/annotation.txt'):
    """转换标注数据为VOC2007格式"""
    with codecs.open(file_path,mode='r', encoding='utf-8') as file:
        lines = file.readlines()
    annotations = dict()
    for line in lines:
        if line.strip()=='':continue
        values = line.strip().split(',')
        name = values[0]
        type = values[5]
        object = dict()
        object['name'] = type
        object['pose'] = 'Unspecified'
        object['truncated'] = 0
        object['difficult'] = 0
        object['bndbox'] = dict()
        object['bndbox']['xmin'] = values[1]
        object['bndbox']['ymin'] = values[2]
        object['bndbox']['xmax'] = values[3]
        object['bndbox']['ymax'] = values[4]
        if name not in annotations:
            annotation = dict()
            annotation['folder'] = 'VOC2007'
            annotation['filename'] = name
            annotation['size'] = dict()
            annotation['size']['width'] = 1000  # 若样本未统一尺寸，请根据实际情况获取
            annotation['size']['height'] = 600  # 若样本未统一尺寸，请根据实际情况获取
            annotation['size']['depth'] = 3
            annotation['segmented'] = 0
            annotation['object'] = [object]
            annotations[name] = annotation
        else:
            annotation = annotations[name]
            annotation['object'].append(object)
    names = []
    path = 'annotation/VOC2007/'
    if not os.path.exists(path+'Annotations'):
        os.mkdir(path+'Annotations')
    for annotation in annotations.items():
        filename = annotation[0].split('.')[0]
        names.append(filename)
        dic = {'annotation':annotation[1]}
        convertedXml = xml2dict.unparse(dic)
        xml_nohead = convertedXml.split('\n')[1]
        file = codecs.open(path + 'Annotations/'+filename + '.xml', mode='w', encoding='utf-8')
        file.write(xml_nohead)
        file.close()
    random.shuffle(names)
    if not os.path.exists(path+'ImageSets'):
        os.mkdir(path+'ImageSets')
    if not os.path.exists(path+'ImageSets/Main'):
        os.mkdir(path+'ImageSets/Main')
    file_train = codecs.open(path+'ImageSets/Main/train.txt',mode='w',encoding='utf-8')
    file_test = codecs.open(path + 'ImageSets/Main/test.txt', mode='w', encoding='utf-8')
    file_train_val = codecs.open(path + 'ImageSets/Main/trainval.txt', mode='w', encoding='utf-8')
    file_val = codecs.open(path + 'ImageSets/Main/val.txt', mode='w', encoding='utf-8')
    count = len(names)
    count_1 = 0.25 * count
    count_2 = 0.5 * count
    for i in range(count):
        if i < count_1:
            file_train_val.write(names[i]+'\n')
            file_train.write(names[i] + '\n')
        elif count_1 <= i <count_2:
            file_train_val.write(names[i] + '\n')
            file_val.write(names[i] + '\n')
        else:
            file_test.write(names[i] + '\n')
    file_train.close()
    file_test.close()
    file_train_val.close()
    file_val.close()
