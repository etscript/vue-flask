import logging
import random
import uuid
import os
from flask import Blueprint, jsonify, session, request, current_app
from datetime import datetime, timedelta
from app.utils.code import ResponseCode
from app.utils.response import ResMsg
from app.utils.util import Redis
from app.utils.auth import Auth, login_required

from wechatpy import parse_message
from wechatpy.utils import check_signature
from wechatpy.session.redisstorage import RedisStorage
from app.utils.wechat_utils import create_flag, \
                handleWxEvent, C_WeChatClient, isFlagExist,\
                    make_qrcode, get_all_args
from elasticsearch import Elasticsearch
from app.api import bp
es = Elasticsearch()

logger = logging.getLogger(__name__)

@bp.route('/get_qrcode', methods=['GET'])
def get_qrcode():
    res = ResMsg()
    # 创建flag
    wechat_flag = create_flag()
    # 创建微信带参二维码
    # 创建一天有效期的二维码, 
    client = C_WeChatClient._get_wechatclient()
    res_qrcode = make_qrcode(client, scene_str = wechat_flag)
    # 创建二维码地址
    url = client.qrcode.get_url(res_qrcode['ticket'])

    res.update(data=dict(qrcode_url = url,
                wechat_flag = wechat_flag)) 
    return res.data

@bp.route('/wechat_verify',methods=['GET','POST'])
def wechat_verify():
    '''
    用来处理微信服务器对本后台的验证，GET方法。
    :return:
    '''
    # POST 方式用于接受被动消息
    if request.method == 'POST':
        msg = parse_message(request.get_data())
        # print("开发者服务收到的消息:", msg.scene_id)
        # 处理方法
        handleWxEvent(msg)
        return 'ok'
    
    if request.method == 'GET':
        # 获取参数
        rq_dict = request.args
        if len(rq_dict) == 0:
            return ""
        tuple_args = get_all_args(rq_dict)
        token = '123456'
        try:
            check_signature(token, tuple_args[1], tuple_args[2], tuple_args[3])
        except Exception as e:
            logger.error(e,exc_info=True)
            return ''
        else:
            return tuple_args[0]

@bp.route('/check_login',methods=['GET'])
def check_login():
    res = ResMsg()
    rq_dict = request.args
    # 获取随机字符串
    wechat_flag = rq_dict.get("wechat_flag")  
    # 判断这个wechat_flag的用户是否关注
    if isFlagExist(wechat_flag) and len(rq_dict) != 0:
        code = ResponseCode.Success
        data = {"result":"yes", "user":isFlagExist(wechat_flag)}
        status = "success"
    elif len(rq_dict) == 0:
        code = ResponseCode.InvalidParameter
        data = None
        status = "fail"
    else:
        code = ResponseCode.NoResourceFound
        data = {"result":"no", "message":"二维码等待扫描中"}
        status = "wait"

    res.update(code=code, data=data, status=status)
    return res.data

@bp.route('/logout',methods=['POST'])
@login_required
def check_logout():
    res = ResMsg()
    user_id = session["user_name"]
    Redis.delete(user_id)
    res.update(data={"result":"yes"})
    return res.data
