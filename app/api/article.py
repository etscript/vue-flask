from flask import request, jsonify, url_for, g, current_app
from app.utils.core import db
from app.models.model import Haowen, Tag
from app.utils.auth import Auth, login_required
from app.utils.code import ResponseCode
from app.utils.response import ResMsg
from app.api import bp
import logging
import json
import os


@bp.route('/ad', methods=['POST'])
def get_ad():
    ad = [
    {
      "id": 11,
      "title": "101",
      "url": "FP8GzAsTWpGrpezKY317SFOUS5gvwexulcjEmKJS.jpeg",
      "type": "banner",
      "created_at": "2019-08-09 20:30:38"
    },
    {
      "id": 12,
      "title": "102",
      "url": "6d2ptD5Erd1uIEMYXl2nwpEMRdHibon6O6enbF2j.jpeg",
      "type": "banner",
      "created_at": "2019-08-09 20:31:07"
    },
    {
      "id": 13,
      "title": "103",
      "url": "EOurPnsdL8FMsKvZVRwVEhNsCpLuqLTJLVeeONhw.jpeg",
      "type": "banner",
      "created_at": "2019-08-09 20:31:23"
    },
    {
      "id": 14,
      "title": "104",
      "url": "gyGhPcNUggbKPHntFWkwli1AvZjvPtGBUGjZizhj.jpeg",
      "type": "banner",
      "created_at": "2019-08-09 20:31:35"
    },
    {
      "id": 15,
      "title": "105",
      "url": "ZO17jMqTewXJWJAskA3kpP9PuliZXxm1jdB76xH3.jpeg",
      "type": "banner",
      "created_at": "2019-08-09 20:31:45"
    },
    {
      "id": 16,
      "title": "106",
      "url": "adaII5rhUZfeP2dApEbP0QHYIiPRgI3bCIl8YjCO.jpeg",
      "type": "banner",
      "created_at": "2019-08-09 20:32:01"
    }
  ]
    return ResMsg(data=ad).data

@bp.route('/article/classify', methods=['GET'])
def get_article_classify():
    classify = [
    {
      "name": "前端",
      "tags": {
        "0": "javascript",
        "1": "HTML5",
        "3": "vue",
        "7": "react",
        "12": "sapper",
        "13": "svelte",
        "16": "axios",
        "18": "vuex",
        "21": "vue-cli",
        "22": "小程序",
        "26": "面试",
        "27": "算法题",
        "29": "回流",
        "30": "重绘",
        "31": "虚拟dom",
        "32": "数独游戏"
      }
    },
    {
      "name": "后端",
      "tags": {
        "0": "python",
        "6": "laravel",
        "15": "go",
        "16": "C++",
        "21": "php",
        "25": "node",
        "28": "redis",
        "31": "echo",
        "37": "gin",
        "40": "qt"
      }
    },
    {
      "name": "工具",
      "tags": {
        "0": "git",
        "2": "Grunt",
        "3": "Gulp",
        "5": "webpack",
        "6": "markdown",
        "7": "OpenCV",
        "8": "ffmpeg",
        "11": "vs2017",
        "12": "Travis CI",
        "13": "mac",
        "14": "pdf",
        "15": "docker",
        "16": "rollup",
        "17": "C++",
        "18": "外挂",
        "22": "postman"
      }
    },
    {
      "name": "比特币",
      "tags": [
        "比特币"
      ]
    },
    {
      "name": "脚本",
      "tags": [
        "pdf",
        "python"
      ]
    }
  ]
    return ResMsg(data=classify).data

@bp.route('/article', methods=['POST'])
# @token_auth.login_required
# @permission_required(Permission.WRITE)
def get_article():
    '''获取一篇新文章'''
    data = request.get_json()
    if not data.get('id'):
        code = ResponseCode.InvalidParameter
        data = 'You must post JSON data.'
        return ResMsg(code=code, data=data).data
    id = data.get('id')
    if id:
        haowen = Haowen.query.get_or_404(id)
        data = haowen.to_dict(False, False, True, True)
    return ResMsg(data=data).data

@bp.route('/article/add', methods=['POST'])
def add_article():
    '''添加一篇新文章'''
    data = request.get_json()
    if not data:
        code = ResponseCode.InvalidParameter
        data = 'You must post JSON data.'
        return ResMsg(code=code, data=data).data

    haowen = Haowen()
    haowen.houtai_create_from_dict(data)
    
    db.session.add(haowen)
    db.session.commit()
    return ResMsg(message='文章添加成功！').data

@bp.route('/article/edit', methods=['POST'])
def edit_article():
    '''修改一篇新文章'''
    data = request.get_json()
    if not data:
        code = ResponseCode.InvalidParameter
        data = 'You must post JSON data.'
        return ResMsg(code=code, data=data).data

    id = data["id"]
    haowen = Haowen.query.get_or_404(id)
    
    haowen.houtai_create_from_dict(data)
    db.session.commit()
    return ResMsg(message='文章修改成功！').data

@bp.route('/article/list', methods=['POST'])
def get_articles():
    '''返回文章集合，分页'''
    data = request.get_json()
    # page = request.args.get('page', 1, type=int)
    page = data['page']
    per_page = min(
        request.args.get(
            'per_page', current_app.config['POSTS_PER_PAGE'], type=int), 100)
    # Haowen.query.order_by(Haowen.timestamp.desc()).filter(Haowen.down==True)
    haowen = Haowen.query.order_by(Haowen.top.desc(),Haowen.timestamp.desc())
    if not data.get('all'):
        data = Haowen.to_web_dict(haowen.filter(Haowen.down==False), \
            page, per_page,'api.get_articles')
    else:
        data = Haowen.to_web_dict(haowen, page, per_page,'api.get_articles')
    
    ret = {
            "current_page": data["_meta"]["page"],
            "from": 1,
            "per_page": 6,
            "to": 6,
            "total": data["_meta"]["total_items"]}
    ret["data"] = data["items"]

    return ResMsg(data=ret).data

@bp.route('/article/delete', methods=['POST'])
# @token_auth.login_required
def delete_article():
    '''下架一篇文章'''
    id = request.get_json()["id"]
    haowen = Haowen.query.get_or_404(id)
    # db.session.delete(haowen)
    haowen.make_down()
    db.session.commit()
    return ResMsg(message='文章下架成功！').data

@bp.route('/article/remove', methods=['POST'])
# @token_auth.login_required
def remove_article():
    '''删除一篇文章'''
    id = request.get_json()["id"]
    haowen = Haowen.query.get_or_404(id)
    db.session.delete(haowen)
    db.session.commit()
    return jsonify({'code':200,'status':'success','message':'彻底删除成功'})

@bp.route('/article/restored', methods=['POST'])
# @token_auth.login_required
def restored_article():
    '''恢复一篇文章'''
    id = request.get_json()["id"]
    haowen = Haowen.query.get_or_404(id)
    haowen.make_restored()
    db.session.commit()
    return ResMsg(message='文章恢复成功！').data

@bp.route('/article/top', methods=['POST'])
# @token_auth.login_required
def top_article():
    '''置顶一篇文章'''
    id = request.get_json()["id"]
    haowen = Haowen.query.get_or_404(id)
    # db.session.delete(haowen)
    haowen.make_top()
    db.session.commit()
    return ResMsg(message='文章置顶成功！').data

@bp.route('/article/untop', methods=['POST'])
# @token_auth.login_required
def untop_article():
    '''取消置顶一篇文章'''
    id = request.get_json()["id"]
    haowen = Haowen.query.get_or_404(id)
    # db.session.delete(haowen)
    haowen.make_untop()
    db.session.commit()
    return ResMsg(message='文章取消置顶成功！').data

@bp.route('/article/tag', methods=['POST'])
# @token_auth.login_required
def get_articles_by_tag():
    data = request.get_json()
    # page = request.args.get('page', 1, type=int)
    page = data['page']
    name = data['tag']
    per_page = min(
        request.args.get(
            'per_page', current_app.config['POSTS_PER_PAGE'], type=int), 100)
    
    tag = Tag.query.filter_by(name = name).first()
    # Haowen.query.order_by(Haowen.timestamp.desc()).filter(Haowen.down==True)
    # haowen = Haowen.query.order_by(Haowen.top.desc(),Haowen.timestamp.desc())
    

    if tag:
      data = Haowen.to_web_dict(tag.haowens, \
              page, per_page,'api.get_articles_by_tag', name=name)
      ret = {
            "current_page": data["_meta"]["page"],
            "from": 1,
            "per_page": 6,
            "to": 6,
            "total": data["_meta"]["total_items"],
            "data": data["items"]}
    else:
      ret = {
            "current_page": 1,
            "from": 1,
            "per_page": 6,
            "to": 6,
            "total": 0,
            "data": []}

    return ResMsg(data=ret).data


###
# 全文搜索
###
@bp.route('/search/', methods=['GET'])
def search():
    '''Elasticsearch全文检索博客文章'''
    q = request.args.get('q')
    if not q:
        return bad_request(message='keyword is required.')

    page = request.args.get('page', 1, type=int)
    per_page = min(
        request.args.get(
            'per_page', current_app.config['POSTS_PER_PAGE'], type=int), 100)

    total, hits_basequery = Haowen.search(q, page, per_page)
    # 总页数
    total_pages, div = divmod(total, per_page)
    if div > 0:
        total_pages += 1

    # 不能使用 Haowen.to_collection_dict()，因为查询结果已经分页过了
    data = {
        'items': [item.to_dict() for item in hits_basequery],
        '_meta': {
            'page': page,
            'per_page': per_page,
            'total_pages': total_pages,
            'total_items': total
        },
        '_links': {
            'self': url_for('api.search', q=q, page=page, per_page=per_page),
            'next': url_for('api.search', q=q, page=page + 1, per_page=per_page) if page < total_pages else None,
            'prev': url_for('api.search', q=q, page=page - 1, per_page=per_page) if page > 1 else None
        }
    }
    return jsonify(data=data, status='success', message='Total items: {}, current page: {}'.format(total, page))


@bp.route('/search/post-detail/<int:id>', methods=['GET'])
def get_search_post(id):
    '''从搜索结果列表页跳转到文章详情'''
    q = request.args.get('q')
    page = request.args.get('page', type=int)
    per_page = request.args.get('per_page', type=int)

    if q and page and per_page:  # 说明是从搜索结果页中过来查看文章详情的，所以要高亮关键字
        total, hits_basequery = Post.search(q, page, per_page)
        haowen = hits_basequery.first()  # 只会有唯一的一篇文章
        data = haowen.to_dict()  # 会高亮关键字
    else:
        haowen = Haowen.query.get_or_404(id)
        data = haowen.to_dict()  # 不会高亮关键字

    # 下一篇文章
    next_basequery = Haowen.query.order_by(PHaowenost.timestamp.desc()).filter(Haowen.timestamp > haowen.timestamp)
    if next_basequery.all():
        data['next_id'] = next_basequery[-1].id
        data['next_title'] = next_basequery[-1].title
        data['_links']['next'] = url_for('api.get_haowen', id=next_basequery[-1].id)
    else:
        data['_links']['next'] = None
    # 上一篇文章
    prev_basequery = Haowen.query.order_by(Haowen.timestamp.desc()).filter(Haowen.timestamp < haowen.timestamp)
    if prev_basequery.first():
        data['prev_id'] = prev_basequery.first().id
        data['prev_title'] = prev_basequery.first().title
        data['_links']['prev'] = url_for('api.get_haowen', id=prev_basequery.first().id)
    else:
        data['_links']['prev'] = None
    return jsonify(data)
