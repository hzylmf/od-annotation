# 目标检测数据集标注工具

采用python-flask框架开发，基于B/S方式交互，支持多人同时标注。

## 特点
* B/S方式交互
* 支持多人同时标注（可分配不同标注人员的标注范围，或不同人员标注不同类别）
* 类别采用选择方式，免去手工输入类别工作
* 支持拖拽方式修正标注区域
* 支持键盘方向键切换标注样本


## 使用方法
1. 根据requirements.txt安装环境依赖
2. 重命名标注样本，采用前导0方式编号，共6位(000001-0000xx)，样本为JPG格式
3. 拷贝样本到static/dataset目录
4. 启动标注工具：`python3 app.py --start|stop|restart`

## 说明
* 依赖python3
* 标注数据在static/dataset/annotation.txt文件中，每行一条标注数据，格式为`filename,x1,y1,x2,y2,classname`，x1,y1,x2,y2分别表示左上角和右下角坐标

## 后续支持
* 标注类别配置
* 标注格式支持VOC2007格式