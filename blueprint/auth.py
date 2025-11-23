# auth.py

from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import UserModel
from exts import db
import uuid
import json

bp = Blueprint("auth", __name__, url_prefix="/auth")

# 用户注册
@bp.route('/reg', methods=['POST'])
@bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not all([username, password]):
        return jsonify({
            "status": 1,
            "message": "用户名和密码不能为空！"
        }), 400
    
    # 检查用户名是否已存在
    if UserModel.query.filter_by(username=username).first():
        return jsonify({
            "status": 1,
            "message": "用户名被占用，请更换其他用户名！"
        }), 400
    
    # 检查邮箱是否已存在
    if email and UserModel.query.filter_by(email=email).first():
        return jsonify({
            "status": 1,
            "message": "邮箱被占用，请更换其他邮箱！"
        }), 400
    
    # 生成唯一uid
    uid = str(uuid.uuid4())
    hashed_password = generate_password_hash(password)
    new_user = UserModel(
        uid=uid,
        username=username,
        email=email,
        password=hashed_password,
        identity="普通用户"  # 默认身份
    )
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({
        "status": 0,
        "message": "注册成功！",
        "data": {
            "id": new_user.id,
            "username": new_user.username,
            "nickname": new_user.username,
            "email": new_user.email
        }
    }), 201

# 用户登录
@bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')  # 可以是用户名或邮箱
    password = data.get('password')
    
    if not all([username, password]):
        return jsonify({
            "status": 1,
            "message": "用户名和密码不能为空！"
        }), 400
    
    # 支持用户名或邮箱登录
    user = UserModel.query.filter(
        (UserModel.username == username) | (UserModel.email == username)
    ).first()
    
    if user and check_password_hash(user.password, password):
        # 如果用户没有uid，生成一个
        if not user.uid:
            user.uid = str(uuid.uuid4())
            db.session.commit()
        
        session['user_id'] = user.id
        session['uid'] = user.uid
        return jsonify({
            "status": 0,
            "message": "登录成功！",
            "token": user.uid,  # 使用uid作为token
            "data": {
                "id": user.id,
                "username": user.username,
                "nickname": user.username,
                "email": user.email
            }
        }), 200
    
    return jsonify({
        "status": 1,
        "message": "用户名或密码错误！"
    }), 401

# 获取用户信息
@bp.route('/userinfo', methods=['GET'])
def get_userinfo():
    # 从请求头获取token
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({
            "status": 1,
            "message": "未提供认证信息！"
        }), 401
    
    # 通过uid查找用户
    user = UserModel.query.filter_by(uid=token).first()
    if not user:
        return jsonify({
            "status": 1,
            "message": "用户未找到！"
        }), 404
    
    return jsonify({
        "status": 0,
        "message": "获取用户基本信息成功！",
        "data": {
            "id": user.id,
            "username": user.username,
            "nickname": user.username,
            "email": user.email,
            "user_pic": user.avatar if user.avatar else "",
            "identity": user.identity if user.identity else "普通用户"
        }
    }), 200

# 更新用户信息（名字、邮箱、当前身份）
@bp.route('/userinfo', methods=['PUT'])
def update_userinfo():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({
            "status": 1,
            "message": "未提供认证信息！"
        }), 401
    
    user = UserModel.query.filter_by(uid=token).first()
    if not user:
        return jsonify({
            "status": 1,
            "message": "用户未找到！"
        }), 404
    
    data = request.json
    if 'id' in data:
        user.id = data['id']
    if 'nickname' in data:
        user.username = data['nickname']
    if 'email' in data:
        # 检查邮箱是否被其他用户使用
        existing_user = UserModel.query.filter_by(email=data['email']).first()
        if existing_user and existing_user.id != user.id:
            return jsonify({
                "status": 1,
                "message": "邮箱已被占用！"
            }), 400
        user.email = data['email']
    if 'identity' in data:
        user.identity = data['identity']
    
    db.session.commit()
    
    return jsonify({
        "status": 0,
        "message": "更新用户信息成功！",
        "data": {
            "id": user.id,
            "username": user.username,
            "nickname": user.username,
            "email": user.email,
            "user_pic": user.avatar if user.avatar else "",
            "identity": user.identity if user.identity else "普通用户"
        }
    }), 200

# 重置密码
@bp.route('/updatepwd', methods=['PUT'])
def update_password():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({
            "status": 1,
            "message": "未提供认证信息！"
        }), 401
    
    user = UserModel.query.filter_by(uid=token).first()
    if not user:
        return jsonify({
            "status": 1,
            "message": "用户未找到！"
        }), 404
    
    data = request.json
    # old_pwd = data.get('oldPwd')
    new_pwd = data.get('new_pwd')
    
    if not new_pwd:
        return jsonify({
            "status": 1,
            "message": "新密码不能为空！"
        }), 400
    
    # # 验证原密码
    # if not check_password_hash(user.password, old_pwd):
    #     return jsonify({
    #         "status": 1,
    #         "message": "原密码错误！"
    #     }), 400
    
    # 更新密码
    user.password = generate_password_hash(new_pwd)
    db.session.commit()
    
    return jsonify({
        "status": 0,
        "message": "更新密码成功！"
    }), 200

# 更新头像
@bp.route('/update/avatar', methods=['PATCH'])
def update_avatar():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({
            "status": 1,
            "message": "未提供认证信息！"
        }), 401
    
    user = UserModel.query.filter_by(uid=token).first()
    if not user:
        return jsonify({
            "status": 1,
            "message": "用户未找到！"
        }), 404
    
    data = request.json
    avatar = data.get('avatar')
    
    if not avatar:
        return jsonify({
            "status": 1,
            "message": "头像数据不能为空！"
        }), 400
    
    user.avatar = avatar
    db.session.commit()
    
    return jsonify({
        "status": 0,
        "message": "更新头像成功！",
        "data": {
            "user_pic": user.avatar
        }
    }), 200

# 退出登录
@bp.route('/logout', methods=['POST'])
def logout():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({
            "status": 1,
            "message": "未提供认证信息！"
        }), 401
    
    # 清除session
    session.pop('user_id', None)
    session.pop('uid', None)
    
    return jsonify({
        "status": 0,
        "message": "退出成功！"
    }), 200
