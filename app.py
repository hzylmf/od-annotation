import codecs
import hashlib
import json
import threading
import time
import os
import argparse
import traceback
import requests
from flask import Flask, render_template, jsonify, send_file
from flask import request

import config as sys_config
import utils.tool as tool
from logger_manager import controller_logger as logger

app = Flask(__name__)
app.config.from_object('config')

mu = threading.Lock()  # 创建一个锁


# Route to any template
@app.route('/')
def index():
    names = [name for name in os.listdir(sys_config.SAMPLE_FILE_PATH) \
             if name.split('.')[-1].lower() in sys_config.SAMPLE_TYPE_SET]
    return render_template('index.html', \
                           ticket_count=len(names), \
                           sample_type=sys_config.SAMPLE_FILE_TYPE)


@app.route('/<template>')
def route_template(template):
    return render_template(template)


# 读取类别标签
@app.route('/api/annotation/labels', methods=['GET'])
def get_sample():
    label_json = tool.get_labels()
    result = dict()
    result['message'] = 'success'
    result['data'] = label_json
    return jsonify(result)


# 读取标注样本
@app.route('/api/annotation/sample', methods=['GET'])
def get_labels():
    if 'index' in request.args:
        img_name = request.args['index'] + '.' + sys_config.SAMPLE_FILE_TYPE
        img_path = os.path.join(sys_config.SAMPLE_FILE_PATH, img_name)

        return send_file(img_path, mimetype='application/octet-stream',
                         as_attachment=True, attachment_filename=img_name)
    else:
        result = dict()
        result['message'] = 'failure'
        return jsonify(result)


# 标注接口
@app.route('/api/annotation/save', methods=['POST'])
def save_annotation():
    pic_id = request.form['pic_id']
    region_loc = request.form['region_loc']
    region_class = request.form['region_class']
    path_annotation = 'annotation/annotation.txt'
    try:
        if mu.acquire(True):
            if not os.path.exists(path_annotation):
                file = codecs.open(path_annotation, mode='a+', encoding='utf-8')
                file.close()
            file = codecs.open(path_annotation, mode='r+', encoding='utf-8')
            lines = file.readlines()
            file.seek(0, 0)
            pic_name = pic_id + '.' + sys_config.SAMPLE_FILE_TYPE
            content = pic_name + ',' + region_loc + ',' + region_class
            find = False
            for line in lines:
                line = line.strip()
                line_new = line
                values = line.split(',')
                if values[0] + values[-1] == pic_name + region_class:
                    line_new = content
                    find = True
                if not line_new.endswith('\n'):
                    line_new += '\n'
                file.write(line_new)
            if not find:
                file.write(content + '\n')
            file.close()
            mu.release()
    except Exception as e:
        print(e)
    result = dict()
    result['message'] = 'success'
    return jsonify(result)


# Errors
@app.errorhandler(403)
def not_found_error(error):
    return render_template('page_403.html'), 403


@app.errorhandler(404)
def not_found_error(error):
    return render_template('page_404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('page_500.html'), 500


def run():
    app.run(debug=sys_config.DEBUG, host='0.0.0.0', port=sys_config.SERVER_PORT, threaded=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Object detection annotation service.')
    parser.add_argument('--start', action='store_true', help='running background')
    parser.add_argument('--stop', action='store_true', help='shutdown process')
    parser.add_argument('--restart', action='store_true', help='restart process')
    parser.add_argument('--convert2voc', action='store_true', help='restart process')

    FLAGS = parser.parse_args()
    if FLAGS.start:
        tool.start_service(run, sys_config.PID_FILE)
    elif FLAGS.stop:
        tool.shutdown_service(sys_config.PID_FILE)
    elif FLAGS.restart:
        tool.shutdown_service(sys_config.PID_FILE)
        tool.start_service(run, sys_config.PID_FILE)
    elif FLAGS.convert2voc:
        tool.convert_to_voc2007()
