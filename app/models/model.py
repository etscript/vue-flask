from datetime import datetime
from app.utils.core import db
from flask import url_for, current_app
from app.utils.elasticsearch import add_to_index, remove_from_index, query_index, es_highlight

class User(db.Model):
    """
    用户表
    """
    __tablename__ = 'user'
    id          = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name    = db.Column(db.String(128), nullable=False, server_default="")
    age    = db.Column(db.String(128), nullable=False, server_default="")


class UserLoginMethod(db.Model):
    """
    用户登陆验证表
    """
    __tablename__ = 'user_login_method'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)  # 用户登陆方式主键ID
    # user_id = db.Column(db.Integer, nullable=False)  # 用户主键ID
    login_method = db.Column(db.String(36), nullable=False)  # 用户登陆方式，WX微信，P手机
    identification = db.Column(db.String(36), nullable=False)  # 用户登陆标识，微信ID或手机号
    access_code = db.Column(db.String(36), nullable=True)  # 用户登陆通行码，密码或token
    nickname    = db.Column(db.String(128), nullable=True, server_default="")
    sex         = db.Column(db.String(1), nullable=False, server_default="0")
    admin       = db.Column(db.String(1), nullable=False, server_default="0")

    def to_dict(self):
        return {
            'id': self.id,
            'login_method': self.login_method,
            'identification': self.identification,
            'access_code': self.access_code,
            'nickname': self.nickname,
            'sex': self.sex,
            'admin': self.admin
        }

class Article(db.Model):
    """
    文章表
    """
    __tablename__ = 'article'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(20), nullable=False)  # 文章标题
    body = db.Column(db.String(255), nullable=False)  # 文章内容
    last_change_time = db.Column(db.DateTime, nullable=False, default=datetime.now)  # 最后一次修改日期
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 作者


class ChangeLogs(db.Model):
    """
    修改日志
    """
    __tablename__ = 'change_logs'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 作者
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))  # 文章
    modify_content = db.Column(db.String(255), nullable=False)  # 修改内容
    create_time = db.Column(db.DateTime, nullable=False)  # 创建日期

class WXUser(db.Model):
    # 设置数据库表名
    __tablename__ = 'wxuser'
    id = db.Column(db.Integer, autoincrement=True)
    nickname = db.Column(db.String(128))
    openid = db.Column(db.String(255), primary_key=True)
    gender = db.Column(db.String(64))  
    country = db.Column(db.String(128))
    province = db.Column(db.String(128))
    city = db.Column(db.String(128))

    def to_dict(self):
        data = {
            'id': self.id,
            'nickname': self.nickname,
            'openid': self.openid,
            'gender': self.gender,
            'country': self.country,
            'province': self.province,
            'city': self.city
        }
        return data

    def from_dict(self, data):
        for field in ['nickname', 'openid', 'gender', 'country', 'province', 'city']:
            if field in data:
                setattr(self, field, data[field])
        self.openid = data["openId"]
        self.nickname = data["nickName"]

class SearchableMixin(object):
    @classmethod
    def search(cls, query, page, per_page, ids=None):
        total, hits, highlights = query_index(cls.__tablename__, query, page, per_page, ids)

        if total == 0:
            return 0, cls.query.filter_by(id=0)  # 如果没有匹配到搜索词，则故意返回空的 BaseQuery

        hit_ids = []  # 匹配到的记录，id 列表
        when = []
        for i in range(len(hits)):
            hit_ids.append(hits[i][0])
            when.append((hits[i][0], i))
        # 将 hit_ids 列表转换成对应排序顺序(ES搜索得分高排在前面)的 BaseQuery，请参考: https://stackoverflow.com/questions/6332043/sql-order-by-multiple-values-in-specific-order/6332081#6332081
        hits_basequery = cls.query.filter(cls.id.in_(hit_ids)).order_by(db.case(when, value=cls.id))
        # 再遍历 BaseQuery，将要搜索的字段值中关键词高亮
        for obj in hits_basequery:
            for field, need_highlight in obj.__searchable__:
                if need_highlight:  # 只有设置为 True 的字段才高亮关键字
                    source = getattr(obj, field)  # 原字段的值
                    highlight_source = es_highlight(source, highlights)  # 关键字高亮后的字段值
                    setattr(obj, field, highlight_source)

        return total, hits_basequery

    @classmethod
    def receive_after_insert(cls, mapper, connection, target):
        '''监听 SQLAlchemy 'after_insert' 事件
        请参考: https://docs.sqlalchemy.org/en/13/orm/events.html#mapper-events'''
        add_to_index(target.__tablename__, target)

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'update': list(session.dirty)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def receive_after_delete(cls, mapper, connection, target):
        '''监听 SQLAlchemy 'after_delete' 事件'''
        remove_from_index(target.__tablename__, target)

    @classmethod
    def reindex(cls):
        '''刷新指定数据模型中的所有数据的索引'''
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)


db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)


class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        # 如果当前没有任何资源时，或者前端请求的 page 越界时，都会抛出 404 错误
        # 由 @bp.app_errorhandler(404) 自动处理，即响应 JSON 数据：{ error: "Not Found" }
        resources = query.paginate(page, per_page)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data
    
    @staticmethod
    def to_web_dict(query, page, per_page, endpoint, **kwargs):
        # 如果当前没有任何资源时，或者前端请求的 page 越界时，都会抛出 404 错误
        # 由 @bp.app_errorhandler(404) 自动处理，即响应 JSON 数据：{ error: "Not Found" }
        resources = query.paginate(page, per_page)
        data = {
            'items': [item.to_dict(False, False, True, False) for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data

class Haowen(SearchableMixin, PaginatedAPIMixin, db.Model):
    __tablename__ = 'haowen'
    __searchable__ = [('article_title', True), ('category_name', True), ('article_filter_content', False)]
    for_list = True
    houtai = False
    def __init__(self, for_list = True, houtai = False):
        self.for_list = for_list
        self.houtai = houtai
    # 共有
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    article_title = db.Column(db.Text)
    article_format_date = db.Column(db.Text)
    article_pic = db.Column(db.Text)
    article_collection = db.Column(db.Text)
    article_comment = db.Column(db.Text)
    article_referrals = db.Column(db.Text)
    article_avatar = db.Column(db.Text)
    article_favorite = db.Column(db.Text)
    category_name = db.Column(db.Text)
    tag_category = db.Column(db.Text)
    article_mall = db.Column(db.Text)
    article_mall_id = db.Column(db.Text)
    user_smzdm_id = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    content_short = db.Column(db.Text)
    down = db.Column(db.Integer, default=False, index=True)
    deleted_at = db.Column(db.DateTime, index=True)
    created_at = db.Column(db.DateTime, index=True)
    top = db.Column(db.Integer, default=0, index=True)


    # haowen list 添加字段
    article_channel_id = db.Column(db.Text)
    article_channel_name = db.Column(db.Text)
    article_recommend = db.Column(db.Text)
    article_love_count = db.Column(db.Text)

    # haowen 添加的字段
    hot_comments = db.Column(db.Text)
    article_price = db.Column(db.Text)
    article_filter_content = db.Column(db.Text)
    content = db.Column(db.Text)

    def change(self, for_list = True, houtai = False):
        self.for_list = for_list
        self.houtai = houtai

    def __repr__(self):
        return '<Post {}>'.format(self.title)

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        '''
        target: 有监听事件发生的 Post 实例对象
        value: 监听哪个字段的变化
        '''
        # if not target.summary:  # 如果前端不填写摘要，是空str，而不是None
        #     target.summary = value[:200] + '  ... ...'  # 截取 body 字段的前200个字符给 summary
        pass
    
    def to_dict(self, wxapp_list = True, wxapp = True, web_list = False, web = False):
        if wxapp_list:
            data = {
                "article_id" : str(self.id),
                "hot_comments" : [],
                "article_comment" : self.article_comment,
                "article_avatar" : self.article_avatar,
                "article_pic" : self.article_pic,
                "article_format_date" : self.article_format_date,
                "article_referrals" : self.article_referrals,
                "article_mall" : self.article_mall,
                "article_mall_id" : self.article_mall_id,
                "article_title" : self.article_title,
                "article_price" : self.article_price,
                "article_favorite" : self.article_favorite,
                "article_collection" : self.article_collection,
                "category_name" : self.category_name,
                "tag_category" : self.tag_category,
                "user_smzdm_id" : self.user_smzdm_id,
                'timestamp': self.timestamp,
                "article_channel_id" : self.article_channel_id,
                "article_channel_name" : self.article_channel_name,
                "article_recommend" : self.article_recommend,
                "article_love_count" : self.article_love_count
            }
        else:
            data = {}

        if wxapp:
            data.update({
                "hot_comments" : self.hot_comments,
                "article_price" : self.article_price,
                "article_filter_content" : self.article_filter_content 
            })
        
        if web_list:
            # 后台需要的字段
            data.update({
                'timestamp': self.timestamp,
                'id': self.id,
                'author': self.article_referrals,
                'reviewer': self.article_referrals,
                'title': self.article_title,
                'content_short': self.content_short or "UPYUN Python SDK，集合 UPYUN HTTP REST 接口，UPYUN HTTP FORM 接口 和 视频处理接口。",
                'forecast': 10.92,
                'importance': 3,
                'type': 'CN',
                'status': 'published',
                'display_time': self.timestamp,
                'comment_disabled': True,
                'pageviews': 1,
                'image_uri': self.article_pic,
                "desc": None,
                "img": self.article_pic,
                "clicks": 0,
                "classify": "工具",
                "like": 0,
                "deleted_at": self.deleted_at,
                "created_at": self.timestamp or "2020-02-17 15:32:29",
                "prevArticle": [],
                "nextrAticle": [],
                "view_count": 9,
                "tags": ["postman"],
                "comment": 1,
                "commentCount": 2,
                "top" : self.top 
            })
        if web:
            data.update({'content': self.content})
        return data
    def create_from_dict(self, data):
        for field in ['article_comment', 'article_pic', 'article_format_date', \
            'article_referrals', 'article_mall', 'article_mall_id', 'article_title',\
            'article_price', 'article_favorite', 'article_collection', 'article_love_count',\
            'article_avatar', 'tag_category', 'tag_category', 'user_smzdm_id', \
            'article_channel_id', 'article_channel_name', 'article_recommend']:
            if field in data:
                setattr(self, field, data[field])
        # self.article_id = "70249788"
        self.hot_comments = ""
        self.id = int(data['article_id'])
        self.article_filter_content = data['article_filter_content']
        self.down = False

    def make_down(self):
        self.down = True
        self.deleted_at = datetime.now()
    
    def make_restored(self):
        self.down = False
        self.deleted_at = None
    
    def make_top(self):
        self.top = True

    def make_untop(self):
        self.top = False

    def houtai_create_from_dict(self, data):
        for field in ['article_comment', 'article_pic', 'article_format_date', \
            'article_referrals', 'article_mall', 'article_mall_id', 'article_title',\
            'article_price', 'article_favorite', 'article_collection', 'article_love_count',\
            'article_avatar', 'tag_category', 'tag_category', 'user_smzdm_id', \
            'article_channel_id', 'article_channel_name', 'article_recommend']:
            if field in data:
                setattr(self, field, data[field])
        # self.article_id = "70249788"
        # self.timestamp = data['display_time']
        self.hot_comments = ""
        # self.id = int(data['id'])
        self.content = data['content']
        self.content_short = data.get('content_short') or None
        self.article_comment = "0"
        self.article_pic = data.get('img') or data.get('url') or "http://qna.smzdm.com/201905/24/5ce74d7a6f0419915.jpg_c640.jpg"
        self.article_format_date = "19-05-24"
        self.article_referrals = "真真假假"
        self.article_mall = ""
        self.article_mall_id = ""
        self.article_title = data['title']
        self.article_price = ""
        self.article_favorite = "1"
        self.article_collection = "1"
        self.article_filter_content = data['article_filter_content'].replace('\n','')
        self.article_avatar = "http://avatarimg.smzdm.com/default/6432321680/57d425cd156f2-small.jpg"
        self.category_name = "#其他文化娱乐 "
        self.tag_category = "#宅家生活手册 #购物攻略 #影视 "
        self.user_smzdm_id = "6432321680"
        self.article_channel_id = "11"
        self.article_channel_name = "原创"
        self.article_recommend = "1"
        self.article_love_count = "0"

    def houtai_update_from_dict(self, data):
        for field in ['article_comment', 'article_pic', 'article_format_date', \
            'article_referrals', 'article_mall', 'article_mall_id', 'article_title',\
            'article_price', 'article_favorite', 'article_collection', 'article_love_count',\
            'article_avatar', 'tag_category', 'tag_category', 'user_smzdm_id', \
            'article_channel_id', 'article_channel_name', 'article_recommend']:
            if field in data:
                setattr(self, field, data[field])
        # self.article_id = "70249788"
        self.hot_comments = ""
        #self.id = int(data['article_id'])
        self.article_filter_content = data['article_filter_content'].replace('\n','')
        self.content = data['content']
        self.article_title = data['title']
        self.content_short = data['content_short']
        self.article_pic = data['image_uri']
        self.down = data['down']
        # self.timestamp = data['display_time']
        


    def is_liked_by(self, user):
        '''判断用户 user 是否已经收藏过该文章'''
        return user in self.likers

    def liked_by(self, user):
        '''收藏'''
        if not self.is_liked_by(user):
            self.likers.append(user)

    def unliked_by(self, user):
        '''取消收藏'''
        if self.is_liked_by(user):
            self.likers.remove(user)



class WebInfo(db.Model):
    __tablename__ = 'webinfo'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    title = db.Column(db.Text)
    keyword = db.Column(db.Text)
    description = db.Column(db.Text)
    personinfo = db.Column(db.Text)
    github = db.Column(db.Text)
    icp = db.Column(db.Text)
    weixin = db.Column(db.Text)
    zhifubao = db.Column(db.Text)
    qq = db.Column(db.Text)
    phone = db.Column(db.Text)
    email = db.Column(db.Text)
    startTime = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<WebInfo {}>'.format(self.title)
    
    def to_dict(self):
        data = {
            "id" : str(self.id),
            "title" : self.title,
            "keyword" : self.keyword,
            "description" : self.description,
            "personinfo" : self.personinfo,
            "github" : self.github,
            "icp" : self.icp,
            "weixin" : self.weixin,
            "zhifubao" : self.zhifubao,
            "qq" : self.qq,
            "phone" : self.phone,
            "email" : self.email,
            "startTime" : self.startTime,
            "created_at" : self.created_at,
            "updated_at" : self.updated_at
        }
        return data

    def create_from_dict(self, data):
        for field in ['title', 'keyword', 'description', \
            'personinfo', 'github', 'icp', 'weixin',\
            'zhifubao', 'qq', 'phone']:
            if field in data:
                setattr(self, field, data[field])
