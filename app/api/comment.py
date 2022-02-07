from flask import request, jsonify, url_for, g, current_app
from app.utils.core import db
from app.models.model import UserLoginMethod
from app.utils.auth import Auth, login_required
from app.utils.code import ResponseCode
from app.utils.response import ResMsg
from app.api import bp

@bp.route('/user/list', methods=['POST'])
def get_user_list():
    '''返回用户列表'''
    data = request.get_json()
    # page = request.args.get('page', 1, type=int)
    # Haowen.query.order_by(Haowen.timestamp.desc()).filter(Haowen.down==True)
    # haowen = Tag.query.order_by(Tag.top.desc(),Haowen.timestamp.desc())
    tags = UserLoginMethod.query.all()

    data = [i.to_dict() for i in tags]

    return ResMsg(data=data).data



