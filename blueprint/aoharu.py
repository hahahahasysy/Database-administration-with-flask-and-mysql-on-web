# aoharu.py

from flask import Blueprint, request, jsonify
from models import AoharuModel, UserModel
from exts import db
import json

bp = Blueprint("aoharu", __name__, url_prefix="/aoharu")

# 获取所有青春记录（列表页）
@bp.route('/', methods=['GET'])
def get_aoharu_list():
    aoharu_list = AoharuModel.query.order_by(AoharuModel.created_time.desc()).all()
    result = []
    for item in aoharu_list:
        result.append({
            "id": item.id,
            "title": item.title,
            "description": item.description,
            "image": item.image,
            "date": item.date,
            "authors": {
                "name": item.author_name,
                "avatar": {
                    "src": item.author_avatar if item.author_avatar else ""
                }
            }
        })
    return jsonify(result), 200

# 获取当前用户创建的青春记录（个人页）
@bp.route('/my', methods=['GET'])
def get_my_aoharu():
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
    
    aoharu_list = AoharuModel.query.filter_by(user_id=user.id).order_by(AoharuModel.created_time.desc()).all()
    result = []
    for item in aoharu_list:
        result.append({
            "id": item.id,
            "title": item.title,
            "description": item.description,
            "image": item.image,
            "date": item.date,
            "authors": {
                "name": item.author_name,
                "avatar": {
                    "src": item.author_avatar if item.author_avatar else ""
                }
            }
        })
    return jsonify(result), 200

# 添加青春记录
@bp.route('/', methods=['POST'])
def add_aoharu():
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
    title = data.get('title')
    description = data.get('description', '')
    image = data.get('image', '')
    date = data.get('date')
    
    if not title or not date:
        return jsonify({
            "status": 1,
            "message": "标题和日期不能为空！"
        }), 400
    
    # 获取作者信息
    author_name = data.get('authors', {}).get('name', user.username)
    author_avatar = data.get('authors', {}).get('avatar', {}).get('src', user.avatar if user.avatar else '')
    
    new_aoharu = AoharuModel(
        title=title,
        description=description,
        image=image,
        date=date,
        author_name=author_name,
        author_avatar=author_avatar,
        user_id=user.id
    )
    
    db.session.add(new_aoharu)
    db.session.commit()
    
    return jsonify({
        "status": 0,
        "message": "添加成功！",
        "data": {
            "id": new_aoharu.id,
            "title": new_aoharu.title,
            "description": new_aoharu.description,
            "image": new_aoharu.image,
            "date": new_aoharu.date,
            "authors": {
                "name": new_aoharu.author_name,
                "avatar": {
                    "src": new_aoharu.author_avatar if new_aoharu.author_avatar else ""
                }
            }
        }
    }), 201

# 删除青春记录（仅限当前用户创建的）
@bp.route('/<int:aoharu_id>', methods=['DELETE'])
def delete_aoharu(aoharu_id):
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
    
    aoharu = AoharuModel.query.get(aoharu_id)
    if not aoharu:
        return jsonify({
            "status": 1,
            "message": "记录未找到！"
        }), 404
    
    # 检查是否是当前用户创建的
    if aoharu.user_id != user.id:
        return jsonify({
            "status": 1,
            "message": "无权删除此记录！"
        }), 403
    
    db.session.delete(aoharu)
    db.session.commit()
    
    return jsonify({
        "status": 0,
        "message": "删除成功！"
    }), 200

# 更新青春记录（仅限当前用户创建的）
@bp.route('/<int:aoharu_id>', methods=['PUT'])
def update_aoharu(aoharu_id):
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
    
    aoharu = AoharuModel.query.get(aoharu_id)
    if not aoharu:
        return jsonify({
            "status": 1,
            "message": "记录未找到！"
        }), 404
    
    # 检查是否是当前用户创建的
    if aoharu.user_id != user.id:
        return jsonify({
            "status": 1,
            "message": "无权修改此记录！"
        }), 403
    
    data = request.json
    if 'title' in data:
        aoharu.title = data['title']
    if 'description' in data:
        aoharu.description = data['description']
    if 'image' in data:
        aoharu.image = data['image']
    if 'date' in data:
        aoharu.date = data['date']
    if 'authors' in data:
        if 'name' in data['authors']:
            aoharu.author_name = data['authors']['name']
        if 'avatar' in data['authors'] and 'src' in data['authors']['avatar']:
            aoharu.author_avatar = data['authors']['avatar']['src']
    
    db.session.commit()
    
    return jsonify({
        "status": 0,
        "message": "更新成功！",
        "data": {
            "id": aoharu.id,
            "title": aoharu.title,
            "description": aoharu.description,
            "image": aoharu.image,
            "date": aoharu.date,
            "authors": {
                "name": aoharu.author_name,
                "avatar": {
                    "src": aoharu.author_avatar if aoharu.author_avatar else ""
                }
            }
        }
    }), 200



