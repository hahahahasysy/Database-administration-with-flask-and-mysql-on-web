# # events.py

# from flask import Blueprint, request, jsonify
# from models import ArticleModel, UserModel,LikedArticle
# from exts import db


# bp = Blueprint("events", __name__, url_prefix="/events")

# # 获取所有事件
# @bp.route('/', methods=['GET'])
# def get_events():
#     events = ArticleModel.query.all()
#     result = [
#         {
#             "id": event.id,
#             "title": event.title,
#             "type1": event.type1,
#             "type2": event.type2,
#             "time1": event.time1,
#             "foreigenname1": event.foreigenname1,
#             "people1": event.people1,
#             "content1": event.content1,
#             "content2": event.content2,
#             "links":event.link
#         } for event in events#获取事件内容，赋值给引号内，返回数组，可以随意引用，但是我的垃圾前端好像只引用了名称和时间
#     ]
#     return jsonify(result)#返回数组

# # 获取特定事件详情
# @bp.route('/<int:event_id>', methods=['GET'])
# def get_event(event_id):
#     event = ArticleModel.query.get(event_id)

#     existing_like = LikedArticle.query.filter_by(title=event.title).first()
#     if existing_like:
#              likeor=1
#     else:
#             likeor=0
    
#     #links=Link.query.get(event_id)
#     if event:
#         result = {
#             "id": event.id,
#             "title": event.title,
#             "type1": event.type1,
#             "type2": event.type2,
#             "time1": event.time1,
#             "foreigenname1": event.foreigenname1,
#             "people1": event.people1,
#             "content1": event.content1,
#             "content2": event.content2,
#             "likeor":likeor,
#            # "links":event.link#这里的links对应js里的links
#             "links": event.link.split(",") if event.link else []#逗号分隔链接成数组
            

#         }
#         return jsonify(result)
#     return jsonify({"error": "事件未找到"}), 404
    

# # 上传事件
# @bp.route('/<int:user_id>/upload', methods=['POST'])
# def upload_event(user_id):
#     data = request.json
#     title = data.get('title')
#     type1 = data.get('type1')
#     type2 = data.get('type2')
#     foreigenname1=data.get('foreigenname1')
#     people1=data.get('people1')
#     time1 = data.get('time1')
#     content1 = data.get('content1')
#     content2 = data.get('content2')
#     link=data.get('links',[])#数据为列表型存放在数据库



#     if not all([title, type1, time1, content1,content2,type2,foreigenname1]):
#         return jsonify({"error": "缺少必要字段"}), 400#全部为必要字段

#     user = UserModel.query.get(user_id)
#     if not user:
#         return jsonify({"error": "用户未找到"}), 404

#     new_event = ArticleModel(
#         title=title,
#         type1=type1,
#         type2=type2,
#         foreigenname1=foreigenname1,
#         people1=people1 ,
#         time1=time1,
#         content1=content1,
#         content2=content2,
#         link=link ,

#         user_id=user.id#本用户上传
#     )
    
#     db.session.add(new_event)
#     db.session.commit()#更新数据库

#     return jsonify({"message": "事件上传成功", "event_id": new_event.id}), 201#返回事件的id

# # 搜索事件
# @bp.route('/search', methods=['GET'])
# def search_events():
#     search_query = request.args.get('query')#获取来自前端名为query的字段作为查询参数
#     if not search_query:
#         return jsonify({"error": "请提供搜索查询参数"}), 400
#     events = ArticleModel.query.filter(ArticleModel.title.ilike(f'%{search_query}%')).all()
#     #查找标题，内容中包含相关字段的事件
#     result = [
#         {
#             "id": event.id,
#             "title": event.title,
#             "type1": event.type1,
#             "type2": event.type2,
#             "time1": event.time1,
#             "foreigenname1": event.foreigenname1,
#             "people1": event.people1,
#             "content1": event.content1,
#             "content2": event.content2,
#             "links": event.link
#         } for event in events
#     ]#返回成列表形式，分别用字典进行赋值
#     return jsonify(result)#返回所有符合条件的列表



# # 删除文章
# #@bp.route('/delete')
# @bp.route('/<int:event_id>/delete', methods=['DELETE'])
# def delete_event(event_id):
#     event = ArticleModel.query.get(event_id)
#     if not event:
#         return jsonify({"error": "事件未找到"}), 404
#     db.session.delete(event)
#     db.session.commit()
#     return jsonify({"message": "事件删除成功"}), 200


# #编辑
# @bp.route('/<int:event_id>/edit', methods=['PUT'])
# def edit_event(event_id):
#     event = ArticleModel.query.get(event_id)
#     if not event:
#         return jsonify({"error": "事件未找到"}), 404
#     data = request.json
#     title = data.get('title', event.title)
#     type1 = data.get('type1', event.type1)
#     type2 = data.get('type2', event.type2)
#     foreigenname1 = data.get('foreigenname1', event.foreigenname1)
#     people1 = data.get('people1', event.people1)
#     time1 = data.get('time1', event.time1)
#     content1 = data.get('content1', event.content1)
#     content2 = data.get('content2', event.content2)
#     link = data.get('links', event.link)#获取相关来自前端的更新的内容，更新数据时，可以只提供需要更新的字段，而对于没有提供的字段，可以保持其原来的值不变。同时，也可以防止因为请求中缺少某些字段而导致程序出现错误。
# #前端提供引号内数据即可
#     event.title = title
#     event.type1 = type1
#     event.type2 = type2
#     event.foreigenname1 = foreigenname1
#     event.people1 = people1
#     event.time1 = time1
#     event.content1 = content1
#     event.content2 = content2
#     event.link = link#对新的内容进行赋值

#     db.session.commit()
#     return jsonify({"message": "事件修改成功"}), 200





# # baiduresou
# @bp.route('/baiduresou', methods=['GET'])
# def get_baiduresou():
    
#     title = baiduresou.weibotitle
#     link=baiduresou.weibolink

#     result =  {
#           "resoutitle":title,
#           "resoulink":link
#       }
     
#     return jsonify(result)