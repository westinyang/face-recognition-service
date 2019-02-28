#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
import face_recognition
from flask import Flask, jsonify, request, redirect, render_template
from flask_cors import CORS

# 读取配置文件
port = 5000
tolerance = 0.6
allowed_extension = ['png', 'jpg', 'jpeg']
try:
    cf = configparser.ConfigParser()
    cf.read("./config.ini", encoding='utf-8')
    port = cf.get("config", "port")
    tolerance = float(cf.get("config", "tolerance"))
    allowed_extension = cf.get("config", "allowed_extension").split(",")
except Exception as e:
    print("读取配置文件异常：%s" % (e))

# Flask
app = Flask(__name__)
CORS(app, resources=r'/*')


# 首页面板
@app.route('/', methods=['GET', 'POST'])
def index():
    return"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <meta name="viewport" content="maximum-scale=1.0,minimum-scale=1.0,user-scalable=0,width=device-width,initial-scale=1.0"/>
    <title>人脸识别服务</title>
    <style type="text/css">
        body { background-color: #fff; color: #000; font-size:14px; }
    </style>
</head>
<body>
    <div>
        =============================================<br/>
        <strong>人脸识别服务接口文档</strong><br/>
        =============================================<br/>
        * POST URL       : http://<script>document.write(window.location.host?window.location.host:'0.0.0.0');</script>/face/compare<br/>
        * Request params : file1, file2<br/>
        * Response exam  : {'code':0,'data':{'recognition_result':1},'message':''}<br/>
        * Return code desc<br/>
        &nbsp;&nbsp;&nbsp;- 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; : 正常<br/>
        &nbsp;&nbsp;&nbsp;- 1010 : 请求参数错误<br/>
        &nbsp;&nbsp;&nbsp;- 1020 : 存在格式不正确的文件<br/>
        &nbsp;&nbsp;&nbsp;- 1030 : 存在未识别到人脸的图像<br/>
        * Return data desc<br/>
        &nbsp;&nbsp;&nbsp;- recognition_result : 人脸识别结果（1=识别通过 0=识别不通过）<br/>
        =============================================<br/>
    </div>
</body>
</html>
"""


# 人脸识别接口
@app.route('/face/compare', methods=['POST'])
def face_compare():
    print_split_line()

    # 校验请求参数
    if 'file1' not in request.files or 'file2' not in request.files:
        return build_api_result(1010, "请求参数错误", {})
    
    # 获取请求参数
    file1 = request.files['file1']
    file2 = request.files['file2']
    print("Reqest params: {'file1': '%s', 'file2': '%s'}" % (file1.filename, file2.filename))

    # 检查文件扩展名
    if not allowed_file(file1.filename) or not allowed_file(file2.filename):
        return build_api_result(1020, "存在格式不正确的文件", {})

    # 加载图片
    img1 = face_recognition.load_image_file(file1)
    img2 = face_recognition.load_image_file(file2)

    # 获取人脸编码
    code1 = face_recognition.face_encodings(img1)
    code2 = face_recognition.face_encodings(img2)

    # 校验是否识别到人脸
    if len(code1) == 0 or len(code2) == 0:
        return build_api_result(1030, "存在未识别到人脸的图像", {})

    # 匹配
    match_results = face_recognition.compare_faces([code2[0]], code1[0], tolerance=tolerance)
    recognition_result = 1 if match_results[0] else 0

    # 返回结果
    return build_api_result(0, "", {"recognition_result": recognition_result})


# 检查文件扩展名
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extension


# 构建接口返回结果
def build_api_result(code, message, data):
    result = {
        "code": code,
        "message": message,
        "data": data
    }
    print("Response data:", result)
    return jsonify(result)


# 打印分割线
def print_split_line():
    print("=" * 80)


if __name__ == "__main__":
    print_split_line()
    print(" * POST URL       : http://0.0.0.0:%s/face/compare" % (port))
    print(" * Request params : file1, file2")
    print(" * Response exam  : {'code':0,'data':{'recognition_result':1},'message':''}")
    print(" * Return code desc")
    print("   - 0    : 正常")
    print("   - 1010 : 请求参数错误")
    print("   - 1020 : 存在格式不正确的文件")
    print("   - 1030 : 存在未识别到人脸的图像")
    print(" * Return data desc")
    print("   - recognition_result : 人脸识别结果（1=识别通过 0=识别不通过）")
    print_split_line()
    # Run
    app.config['JSON_AS_ASCII'] = False
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
