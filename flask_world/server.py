# -*- coding: utf-8 -*-
import os

from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)

# 上传目录
app.config['UPLOAD_FOLDER'] = 'static/uploads'
# 支持格式
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}


# 判断上传格式
def allowed_file(filename):
    return '.' in filename and filename.split('.')[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def hello_world():
    return render_template('index.html')


# 获取用户名密码
@app.route('/register', methods=['POST'])
def register():
    print(request.headers)
    # print(request.stream.read())
    print(request.form)
    print(request.form['name'])
    print(request.form.get('name'))
    print(request.form.getlist('name'))
    print(request.form.get('nickname', default='little apple'))
    return 'welcome'


# 返回json
@app.route('/add', methods=['POST'])
def add():
    print(request.headers)
    print(request.json)
    print(type(request.json))
    result = {'sum': request.json['a'] + request.json['b']}
    return jsonify(result)


# 获取上传文件
@app.route('/upload', methods=['POST'])
def upload():
    upload_file = request.files['image']
    # 判断是否上传文件且是否合规
    if upload_file and allowed_file(upload_file.filename):
        filename = secure_filename(upload_file.filename)
        print('====' + secure_filename(upload_file.filename) + '====')
        # 保存至相应目录
        upload_file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename))
        return 'info is ' + request.form.get('name', '') + '. success!'
    else:
        return 'failed'


if __name__ == '__main__':
    app.run(port=5000, debug=True)
