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

    haowen = Tag()
    haowen.houtai_create_from_dict(data)
    
    db.session.add(haowen)
    db.session.commit()
    return ResMsg(message='文章添加成功！').data

@bp.route('/tag/edit', methods=['POST'])
def edit_tag():
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

@bp.route('/tag/list', methods=['POST'])
def get_tags():
    '''返回文章集合，分页'''
    data = request.get_json()
    # page = request.args.get('page', 1, type=int)
    # Haowen.query.order_by(Haowen.timestamp.desc()).filter(Haowen.down==True)
    # haowen = Tag.query.order_by(Tag.top.desc(),Haowen.timestamp.desc())
    tags = Tag.query.all()

    data = [i.to_dict() for i in tags]

    return ResMsg(data=data).data

@bp.route('/tag/delete', methods=['POST'])
# @token_auth.login_required
def delete_tag():
    '''下架一篇文章'''
    id = request.get_json()["id"]
    haowen = Haowen.query.get_or_404(id)
    # db.session.delete(haowen)
    haowen.make_down()
    db.session.commit()
    return ResMsg(message='文章下架成功！').data

@bp.route('/tag/nonindex', methods=['POST'])
# @token_auth.login_required
def unset_tag_on_index():
    '''删除一篇文章'''
    id = request.get_json()["id"]
    haowen = Haowen.query.get_or_404(id)
    db.session.delete(haowen)
    db.session.commit()
    return jsonify({'code':200,'status':'success','message':'彻底删除成功'})

@bp.route('/tag/onindex', methods=['POST'])
# @token_auth.login_required
def set_tag_on_index():
    '''恢复一篇文章'''
    id = request.get_json()["id"]
    haowen = Haowen.query.get_or_404(id)
    haowen.make_restored()
    db.session.commit()
    return ResMsg(message='文章恢复成功！').data

