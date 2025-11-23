# history.py

from flask import Blueprint, request, jsonify
from models import HistoryModel
from exts import db
import json

bp = Blueprint("history", __name__, url_prefix="/history")

# 获取所有历史事件
@bp.route('/', methods=['GET'])
def get_histories():
    histories = HistoryModel.query.all()
    result = []
    for history in histories:
        # 解析JSON格式的content和tags
        try:
            content = json.loads(history.content) if history.content else []
            tags = json.loads(history.tags) if history.tags else []
            images=json.loads(history.images) if history.images else []
        except:
            content = []
            tags = []
            images = []
        
        result.append({
            "id": history.id,
            "title": history.title,
            "date": history.date,
            "author": history.author,
            "location": history.location,
            "type": history.type,
            "content": content,
            "images": images,
            "tags": tags
        })
    return jsonify(result), 200

# 获取特定历史事件详情
@bp.route('/<int:history_id>', methods=['GET'])
def get_history(history_id):
    history = HistoryModel.query.get(history_id)
    if not history:
        return jsonify({"error": "历史事件未找到"}), 404
    
    # 解析JSON格式的content和tags
    try:
        content = json.loads(history.content) if history.content else []
        tags = json.loads(history.tags) if history.tags else []
    except:
        content = []
        tags = []
    
    result = {
        "id": history.id,
        "title": history.title,
        "date": history.date,
        "author": history.author,
        "location": history.location,
        "type": history.type,
        "content": content,
        "images": history.images,
        "tags": tags
    }
    return jsonify(result), 200



