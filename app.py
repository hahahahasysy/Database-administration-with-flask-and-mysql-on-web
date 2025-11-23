from flask import Flask, send_from_directory
import config
from exts import db
from flask_migrate import Migrate
from flask_cors import CORS
from blueprint.auth import bp as auth_bp
# from blueprint.user import bp as user_bp
# from blueprint.events import bp as events_bp
from blueprint.history import bp as history_bp
from blueprint.collage import bp as collage_bp
from blueprint.aoharu import bp as aoharu_bp
from models import UserModel, HistoryModel, AoharuModel, CollageModel
import os

# 配置Flask应用
app = Flask(__name__)

# 配置
app.config.from_object(config)

# 允许跨域
CORS(app)
CORS(app, resources={r"/*": {"origins": "*"}})

# 数据库初始化
db.init_app(app)
migrate = Migrate(app, db)
# 在你的 app.py 或 create_app 函数中
app.config['TRAP_HTTP_EXCEPTIONS'] = True
app.config['JSON_AS_ASCII'] = False

# 关键：禁用严格的斜杠规则
app.url_map.strict_slashes = False 


# 注册蓝图
app.register_blueprint(auth_bp)
# app.register_blueprint(user_bp)
# app.register_blueprint(events_bp)
app.register_blueprint(history_bp)
app.register_blueprint(collage_bp)
app.register_blueprint(aoharu_bp)

# 提供前端页面和静态资源
# 注意：这些路由必须在蓝图注册之后，以确保优先级

# # 提供前端首页
# @app.route('/')
# def index():
#     """提供前端首页"""
#     return send_from_directory('page', 'index.html')

# # 提供assets目录下的静态资源
# @app.route('/assets/<path:filename>')
# def assets(filename):
#     """提供assets目录下的静态资源"""
#     return send_from_directory(os.path.join('page', 'assets'), filename)

# # 提供public路径的静态资源（映射到page根目录）
# @app.route('/public/<path:filename>')
# def public(filename):
#     """提供public目录下的静态资源（实际从page目录提供）"""
#     return send_from_directory('page', filename)


if __name__ == '__main__':
    print("=" * 50)
    print("Flask服务器启动中...")
    print("=" * 50)
    print(f"访问地址: http://127.0.0.1:5000")
    print(f"访问地址: http://localhost:5000")
    print("=" * 50)
    print("已注册的路由:")
    for rule in app.url_map.iter_rules():
        print(f"  {rule.rule} -> {rule.endpoint}")
    print("=" * 50)
    print("按 Ctrl+C 停止服务器")
    print("=" * 50)
    print()
    app.run(debug=True, port=5000, host='127.0.0.1')
