from flask import request, jsonify, url_for, g, current_app
from app.utils.code import ResponseCode
from app.utils.response import ResMsg
from app.utils.core import db
from datetime import datetime
from app.api import bp
import logging
import json
import upyun
import os

logger = logging.getLogger(__name__)

up = upyun.UpYun('project-driven', 'projectdriven', 'PNorIxIZ9AA0OeOrzQnPwwCH1jn4XYu7', timeout=30, endpoint=upyun.ED_AUTO)
def do_upload_image(img):
    '''
      res = up.put(...)
      上传成功，如果是图片类型文件，那么 res 返回的是一个包含图片长、宽、帧数和类型信息的 Python Dict 对象 ( 其他文件类型, 返回一个空的 Dict)：
      {'frames': '1', 'width': '1280', 'file-type': 'PNG', 'height': '800'}
    '''
    headers = { 'x-gmkerl-rotate': '180' ,'x-gmkerl-rotate':'auto'}
    img_name = '{0:%Y%m%d%H%M%S%f}'.format(datetime.now())+'.png'
    # with open(img, 'rb') as f:
    #     up.put(img_name, f, checksum=True, headers=headers)
    up.put(img_name, img, checksum=True, headers=headers)
    return img_name

def do_delete_image(img):
    '''
      res = up.delete(...)
      删除成功，返回 Python `None` 对象; 失败则抛出相应异常。注意删除目录时，必须保证目录为空。
    '''
    up.delete(img)
    return img

@bp.route('/image/upload', methods=['POST'])
def upload_image():
    '''上传图片'''
    data = request.files["image"].read()
    if not data:
        code = ResponseCode.InvalidParameter
        data = 'You must post JSON data.'
        return ResMsg(code=code, data=data).data
    url = do_upload_image(data)
    return {
        "code": 200,
        "data": {
            "url": url
        },
        "status": "success"}

@bp.route('/image/delete', methods=['POST'])
def delete_image():
    '''上传图片'''
    data = request.get_json()
    if not data:
        code = ResponseCode.InvalidParameter
        data = 'You must post JSON data.'
        return ResMsg(code=code, data=data).data
    try:
      do_delete_image(data["image"])
    except:
      pass
    return {
        "code": 200,
        "message": "图片删除成功",
        "status": "success"}







