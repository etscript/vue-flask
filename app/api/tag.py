from turtle import onclick
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

@bp.route('/tag/add', methods=['POST'])
def add_tag():
    '''添加一个标签'''
    data = request.get_json()
    if not data:
        code = ResponseCode.InvalidParameter
        data = 'You must post JSON data.'
        return ResMsg(code=code, data=data).data

    tag = Tag()
    tag.create_from_dict(data)
    
    db.session.add(tag)
    db.session.commit()
    return ResMsg(message='tag添加成功！').data

@bp.route('/tag/edit', methods=['POST'])
def edit_tag():
    '''修改一个tag'''
    data = request.get_json()
    if not data:
        code = ResponseCode.InvalidParameter
        data = 'You must post JSON data.'
        return ResMsg(code=code, data=data).data

    id = data["id"]
    tag = Tag.query.get_or_404(id)
    
    tag.name = data["name"]
    tag.url = data["url"]
    db.session.commit()
    return ResMsg(message='tag修改成功！').data

@bp.route('/tag/indexlist', methods=['POST'])
def get_index_tags():
    '''返回文章集合，分页'''
    data = request.get_json()
    # page = request.args.get('page', 1, type=int)
    # Haowen.query.order_by(Haowen.timestamp.desc()).filter(Haowen.down==True)
    # haowen = Tag.query.order_by(Tag.top.desc(),Haowen.timestamp.desc())
    tags = Tag.query.filter(Tag.delete_tag == 0,
                            Tag.onindex == 1).all()

    data = [i.to_dict() for i in tags]

    return ResMsg(data=data).data

@bp.route('/tag/list', methods=['POST'])
def get_tags():
    '''返回文章集合，分页'''
    data = request.get_json()
    # page = request.args.get('page', 1, type=int)
    # Haowen.query.order_by(Haowen.timestamp.desc()).filter(Haowen.down==True)
    # haowen = Tag.query.order_by(Tag.top.desc(),Haowen.timestamp.desc())
    tags = Tag.query.filter(Tag.delete_tag == 0).all()

    data = [i.to_dict() for i in tags]

    return ResMsg(data=data).data

@bp.route('/tag/delete', methods=['POST'])
# @token_auth.login_required
def delete_tags():
    '''删除一个tag'''
    id = request.get_json()["id"]
    tag = Tag.query.get_or_404(id)
    # db.session.delete(haowen)
    if tag.haowens.all():
      code = ResponseCode.TagHasArticles
      data = 'Tag 还有相关文章！'
      return ResMsg(code=code, data=data).data
    
    tag.delete_tag = 1
    db.session.commit()
    return ResMsg(message='Tag删除成功！').data

@bp.route('/tag/nonindex', methods=['POST'])
# @token_auth.login_required
def unset_tag_on_index():
    '''将Tag从首页移除'''
    id = request.get_json()["id"]
    tag = Tag.query.get_or_404(id)
    tag.onindex = 0
    db.session.commit()
    return ResMsg(message='Tag从首页中移除成功！').data

@bp.route('/tag/onindex', methods=['POST'])
# @token_auth.login_required
def set_tag_on_index():
    '''将Tag放置首页中'''
    id = request.get_json()["id"]
    tag = Tag.query.get_or_404(id)
    tag.onindex = 1
    db.session.commit()
    return ResMsg(message='Tag放置首页中成功！').data

