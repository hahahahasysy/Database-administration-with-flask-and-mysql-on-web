# collage.py

from flask import Blueprint, request, jsonify
from models import CollageModel
from exts import db
import json

bp = Blueprint("collage", __name__, url_prefix="/collage")

# 获取所有学院
@bp.route('/', methods=['GET'])
def get_collages():
    collages = CollageModel.query.all()
    result = []
    for collage in collages:
        # 解析JSON格式的content
        try:
            content = json.loads(collage.content) if collage.content else []
            images = json.loads(collage.images) if collage.images else []
        except:
            content = []
            images=[]
        result.append({
            "id": collage.id,
            "title": collage.title,
            "name": collage.name,
            "image": collage.image,
            "type": collage.type,
            "date": collage.date,
            "author": collage.author,
            "images": images,
            "content": content
        })
    return jsonify(result), 200

# 获取特定学院详情
@bp.route('/<int:collage_id>', methods=['GET'])
def get_collage(collage_id):
    collage = CollageModel.query.get(collage_id)
    if not collage:
        return jsonify({"error": "学院未找到"}), 404
    
    # 解析JSON格式的content
    try:
        content = json.loads(collage.content) if collage.content else []
        images = json.loads(collage.images) if collage.images else []
    except:
        content = []
        images=[]
    result = {
        "id": collage.id,
        "title": collage.title,
        "name": collage.name,
        "image": collage.image,
        "type": collage.type,
        "date": collage.date,
        "author": collage.author,
        "images": images,
        "content": content
    }
    return jsonify(result), 200



