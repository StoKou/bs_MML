import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS  # 导入 CORS
import os
from PIL import Image
import io
import base64


from model_func.shoesPredict import predictImage,predictImage_test
import uuid
import random
import string
app = Flask(__name__)
import json
CORS(app)  # 启用 CORS

# 设置上传文件的保存目录
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):  # 如果目录不存在
    os.makedirs(UPLOAD_FOLDER)  # 创建目录

# 用户信息存储文件
LOGIN_FILE_PATH = os.path.join('user', 'login.json')

# 一些函数（后续可以放在utils下）
def generate_token():
    """生成一个随机的 token"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=32))
def load_users():
    """加载用户数据"""
    try:
        with open(LOGIN_FILE_PATH, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
def save_users(users):
    """保存用户数据"""
    with open(LOGIN_FILE_PATH, 'w') as file:
        json.dump(users, file, indent=4)
def load_users():
    """加载用户数据"""
    try:
        with open(LOGIN_FILE_PATH, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
def get_user_by_username(username):
    """根据用户名获取用户数据"""
    users = load_users()
    return users.get(username, None)

@app.route('/upload', methods=['POST'])
def upload_file():
    # 检查是否有文件上传
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    # 检查是否选择了文件
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # 保存文件到 uploads 目录
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    return jsonify({
        'message': 'File uploaded successfully',
        'file_path': file_path,
    }), 200
@app.route('/predict', methods=['POST'])
def predict():
    # 验证 token
    token = request.form.get('token')
    if not token:
        return jsonify({
            'code': 1,
            'message': 'Missing token in header',
            'data': {}
        }), 401

    # 读取 login.json 文件
    users = load_users()

    # 验证 token
    username = None
    for user_name, info in users.items():
        if info.get('token') == token:
            username = user_name
            break

    if not username:
        return jsonify({
            'code': 2,
            'message': 'Invalid token',
            'data': {}
        }), 403
    # 检查是否有文件上传
    if 'image' not in request.files:
        return jsonify({'error': 'No image file'}), 400
    # 获取图片文件
    image_file = request.files['image']
    image_name = image_file.filename
    description = request.form.get('description', '')
    dataset = request.form.get('dataset', '')
    model = request.form.get('model', '')
    # 打开图片
    image = Image.open(image_file.stream)  # 使用 stream 来支持流式上传

    # 将描述存储到uploads文件夹下的txt文件中
    uploads_folder = 'uploads'
    if not os.path.exists(uploads_folder):
        os.makedirs(uploads_folder)  # 如果uploads文件夹不存在，则创建

    # 生成描述文件的名称，可以使用时间戳或其他方式来确保唯一性
    description_file_name = f"description_{uuid.uuid4().hex}.txt"
    description_file_path = os.path.join(uploads_folder, description_file_name)

    # 将描述写入文件
    with open(description_file_path, 'w', encoding='utf-8') as desc_file:
        desc_file.write(description)

    # 封装成字典
    parameters = {
        "image_file": request.files['image'],
        "image_name": image_file.filename,
        "description": request.form.get('description', ''),
        "dataset": request.form.get('dataset', ''),
        "model": request.form.get('model', ''),
        "test_txt_name":description_file_name
    }
    # 调用 predictImage 函数处理图片
    output_image = predictImage(parameters)

    # 将输出图片转换为 Base64
    buffered = io.BytesIO()
    output_image.save(buffered,format='JPEG')
    output_image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
    # 生成历史记录
    history = {
        'request_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'username': username,
        'dataset': dataset,
        'model': model,
        'image_name': image_name,
        'description':description
    }
    # 添加历史记录到用户信息
    add_history(users, username, history)
    # 删除文件
    if os.path.exists(description_file_path):
        os.remove(description_file_path)
    else:
        print(f"文件 {description_file_path} 不存在，无需删除。")
    # 返回三元组
    return jsonify({
        'inputImage': 'input_image_placeholder',  # 如果需要返回输入图片的 Base64，可以类似处理
        'description': description,
        'outputImage': output_image_base64,
    })

@app.route('/api/login', methods=['POST'])
def login():
    # 从请求中获取账号和密码
    username = request.json.get('username')
    password = request.json.get('password')
    
    # 检查账号和密码是否都提供了
    if not username or not password:
        return jsonify({'error': 'Missing username or password'}), 400

    # 读取 login.json 文件
    users = load_users()
    if not users:
        users = {}

    # 比较存储的用户名和密码与请求中的用户名和密码
    if username in users and users[username]['password'] == password:
        # 生成随机的用户 ID 和 token
        user_id = users[username].get('id', uuid.uuid4().int)
        new_token = generate_token()
        
        # 更新用户的 token
        users[username]['token'] = new_token
        
        # 保存更新后的用户数据
        save_users(users)
                    
        # 返回成功的响应
        return jsonify({
            'code': 0,
            'message': 'Login successful',
            'token': new_token,
            'data': {
                'id': user_id,
                'username': username,
                'nickname': users[username].get('nickname', username),  # 默认昵称为用户名
                'email': users[username].get('email', f"{username}@aaa.com"),  # 默认邮箱
                'user_pic': users[username].get('user_pic', None)  # 默认用户图片为 None
            }
        }), 200
    else:
        # 如果没有找到匹配的用户名和密码，返回 401 未授权
        return jsonify({'message': 'Invalid username or password'}), 401
@app.route('/api/reg', methods=['POST'])
def register():
    # 从请求中获取用户名、密码和确认密码
    username = request.json.get('username')
    password = request.json.get('password')
    confirm_password = request.json.get('repassword')
    
    # 检查用户名、密码和确认密码是否都提供了
    if not username or not password or not confirm_password:
        return jsonify({'error': 'Missing username, password, or confirm password'}), 400

    # 检查两个密码是否一致
    if password != confirm_password:
        return jsonify({'error': 'Passwords do not match'}), 400

    # 加载现有用户数据
    users = load_users()

    # 检查用户名是否已存在
    if username in users:
        return jsonify({'error': 'Username already exists'}), 409

    # 生成随机的用户 ID 和 token
    user_id = uuid.uuid4().int
    token = ''

    # 将新用户添加到用户数据中
    users[username] = {
        'id': user_id,
        'nickname': username,
        'password': password,
        'email': f"{username}@aaa.com",
        'user_pic': None,
        'token': token,  # 添加 token 到用户数据中
        'history':[]
    }

    # 保存更新后的用户数据
    save_users(users)

    # 返回成功的响应
    return jsonify({
        'code': 0,
        'message': 'Register successful',
        'token': token
    }), 200

def add_history(users, username, history):
    """添加历史记录到用户信息"""
    if 'history' not in users[username]:
        users[username]['history'] = []
    users[username]['history'].append(history)
    save_users(users)
# 验证 token 并获取用户历史记录
def get_user_history(token):
    users = load_users()
    for username, info in users.items():
        if info.get('token') == token:
            return username, info.get('history', [])
    return None, []
@app.route('/my/userinfo', methods=['POST', 'GET'])
def userinfo():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({
            'code': 1,
            'message': 'Missing token in header',
            'data': {}
        }), 401

    # 读取 login.json 文件
    users = load_users()
    

    
    # 验证 token
    for username, info in users.items():
        if info['token'] == token:
            # 返回用户信息
            return jsonify({
                'code': 0,
                'message': 'User info retrieved successfully',
                'data': {
                    'id': info['id'],
                    'username': username,
                    'nickname': info['nickname'],
                    'email': info['email'],
                    'user_pic': info['user_pic'],
                    'history':info['history']
                }
            }), 200

    # 如果没有找到匹配的 token，返回 401 未授权
    return jsonify({
        'code': 1,
        'message': 'Invalid token',
        'data': {}
    }), 401

@app.route('/my/update/avatar', methods=['PATCH'])
def update_avatar():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({
            'code': 1,
            'message': 'Missing token in header',
            'data': {}
        }), 401

    # 读取 login.json 文件
    users = load_users()
    username=''
    # 验证 token
    for username, info in users.items():
        if info['token'] == token:
            username=username

    base64_image = request.json.get('avatar')

    # 更新用户的头像信息
    users[username]['user_pic'] = base64_image
    
    # 保存更新后的用户数据
    save_users(users)

    # 返回成功的响应
    return jsonify({
        'code': 0,
        'message': 'Avatar updated successfully',
        'data': {
            'username': username,
            'avatar': base64_image
        }
    }), 200
@app.route('/my/updatepwd', methods=['PATCH'])
def update_password():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({
            'code': 1,
            'message': 'Missing token in header',
            'data': {}
        }), 401

    users = load_users()
    username = ''
    # 验证 token
    for username, info in users.items():
        if info['token'] == token:
            break
    else:
        return jsonify({
            'code': 2,
            'message': 'Invalid token',
            'data': {}
        }), 401

    data = request.json
    old_pwd = data.get('old_pwd')
    new_pwd = data.get('new_pwd')
    re_pwd = data.get('re_pwd')

    if not old_pwd or not new_pwd or not re_pwd:
        return jsonify({
            'code': 3,
            'message': 'Missing password information',
            'data': {}
        }), 400

    if new_pwd != re_pwd:
        return jsonify({
            'code': 4,
            'message': 'New password and confirmation do not match',
            'data': {}
        }), 400
    print(f"user:{users[username]}")


    if users[username]['password'] != old_pwd:
        return jsonify({
            'code': 5,
            'message': 'Old password is incorrect',
            'data': {}
        }), 400

    # 更新用户的密码信息
    users[username]['password'] = new_pwd
    
    # 保存更新后的用户数据
    save_users(users)

    # 返回成功的响应
    return jsonify({
        'code': 0,
        'message': 'Password updated successfully',
        'data': {
            'username': username,
        }
    }), 200

@app.route('/my/updateUserinfo', methods=['PATCH'])
def update_user_info():
    # 获取请求头中的 token
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({
            'code': 1,
            'message': 'Missing token in header',
            'data': {}
        }), 401

    # 读取 login.json 文件
    users = load_users()

    # 验证 token
    for username, info in users.items():
        if info['token'] == token:
            # 获取前端传来的数据
            data = request.json
            id = data.get('id')
            username = data.get('username')
            nickname = data.get('nickname')
            email = data.get('email')

            # 检查数据有效性
            if not all([id, username, nickname, email]):
                return jsonify({
                    'code': 2,
                    'message': 'Invalid request data',
                    'data': {}
                }), 400

            # 更新用户信息
            users[username] = {
                'id': id,
                'username': username,
                'password': info.get('password', ''),  # 保留原有头像信息
                'nickname': nickname,
                'email': email,
                'token': info['token'],  # 保持 token 不变
                'user_pic': info.get('user_pic', ''),  # 保留原有头像信息
                'history': info.get('history', [])  # 保留原有历史记录
            }

            # 保存更新后的用户信息
            save_users(users)

            return jsonify({
                'code': 0,
                'message': 'User info updated successfully',
                'data': {
                    'id': id,
                    'username': username,
                    'nickname': nickname,
                    'email': email
                }
            }), 200

    # 如果没有找到匹配的 token，返回 401 未授权
    return jsonify({
        'code': 1,
        'message': 'Invalid token',
        'data': {}
    }), 401
@app.route('/my/history', methods=['GET'])
def get_history():
    # 从请求头中获取 token
    token = request.headers.get('Authorization')
    
    if not token:
        return jsonify({
            'code': 1,
            'message': 'Missing token in header',
            'data': {}
        }), 401

    # 验证 token 并获取用户历史记录
    username, history = get_user_history(token)
    
    if username is None:
        return jsonify({
            'code': 2,
            'message': 'Invalid token',
            'data': {}
        }), 403

    # 返回用户历史记录
    return jsonify({
                'code': 0,
                'message': 'User History retrieved successfully',
                'data': {
                    'history': history,
                }
            }), 200
# 更新用户历史记录
@app.route('/my/updateHistory', methods=['PATCH'])
def update_history():
    # 从请求头中获取 token
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({
            'code': 1,
            'message': 'Missing token in header',
            'data': {}
        }), 401
    # 加载用户数据
    users = load_users()
    # 验证 token 并获取用户信息
    username=''
    # 验证 token
    for username, info in users.items():
        if info['token'] == token:
            username=username
        
    # 获取请求数据
    # print(request.json)
    new_history = request.json.get('history')

    # 更新用户的历史记录
    if username in users:
        users[username]['history'] = new_history
        save_users(users)  # 保存更新后的用户数据
        return jsonify({
            'code': 0,
            'message': 'History updated successfully',
            'data': {}
        }), 200
    else:
        return jsonify({
            'code': 4,
            'message': 'User not found',
            'data': {}
        }), 404
if __name__ == '__main__':
    app.run(debug=True)