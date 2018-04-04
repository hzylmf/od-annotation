# 目标检测数据集标注工具

采用python-flask框架开发，基于B/S方式交互，支持多人同时标注。

## 特点
* B/S方式交互
* 支持多人同时标注（可分配不同标注人员的标注范围，或不同人员标注不同类别）
* 类别采用选择方式，免去手工输入类别工作
* 支持拖拽方式修正标注区域
* 支持键盘方向键切换标注样本
* 支持多类别多目标标注


## 使用方法
1. 根据`requirements.txt`安装环境依赖
```buildoutcfg
$ cd od-annotation
$ pip3 install -r requirements.txt
```
2. 重命名标注样本，采用前导0方式编号，共6位(000001-0000xx)，注意保持样本编号连续。
3. 编辑`annotation/label_config.txt`文件，根据格式配置标签
```buildoutcfg
# 标签名称:标签描述
dog:狗
```
4. 编辑`config.py`,根据样本实际情况修改：
```buildoutcfg
SAMPLE_FILE_TYPE = 'jpg'  # 样本图片格式
SAMPLE_FILE_PATH = 'your samples directory path'  # 样本图片存放目录
```
4. 启动/停止/重启标注工具：
```buildoutcfg
$ cd od-annotation
$ python3 app.py --start|stop|restart
```
5. 访问`http://localhost:5000`开始标注。先选定待标注类别，然后按住鼠标左键并拖拽鼠标在目标区域绘制矩形框进行标注，松开鼠标完成标注。可拖动矩形框以修正坐标，右击某矩形框可取消该标注。每次新绘制矩形框、拖动已有矩形框或右击取消矩形框时，会在下方的`当前样本标注状态`文本框中同步更新该样本的标注结果。
6. 点击左右方向按钮或通过键盘方向键切换标注样本。切换时自动提交标注结果，同时在`所有样本标注状态`文本框中更新当前样本的标注结果。或手动点击`保存`按钮提交标注结果。
7. 所有样本标注完成后，若需要转换成VOC2007格式，执行：
```buildoutcfg
$ cd od-annotation
$ python3 app.py --convert2voc
```
查看`annotation/VOC2007`目录下相关文件夹是否生成对应文件

## 说明
* 依赖python3
* 标注数据在`annotation/annotation.txt`文件中，每行一条标注数据，格式为`filename,x1,y1,x2,y2,classname`，x1,y1,x2,y2分别表示左上角和右下角坐标


## 已知Bug
* 绘制区域再选择对应类别，然后切换样本时会导致类别单选框状态跟着切换（临时解决方法：通过点击页面空白区域来取消单选框焦点以避免bug）
