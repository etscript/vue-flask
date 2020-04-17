from wechatpy.session.redisstorage import RedisStorage
from wechatpy import WeChatClient
from app.utils.util import Redis
from app.utils.util import wechatclient as client
import datetime
import random
import json
from app.utils.auth import Auth, login_required
from app.models.model import UserLoginMethod
from app.utils.core import db
import logging
logger = logging.getLogger(__name__)

def wx_login_or_register(wx_user_info):
    """
    验证该用户是否注册本平台，如果未注册便注册后登陆，否则直接登陆。
    :param wx_user_info:拉取到的微信用户信息
    :return:
    """
    # 微信统一ID
    openid = wx_user_info.get("openid")
    sex = wx_user_info.get("sex")
    # 用户昵称
    nickname = wx_user_info.get("nickname")
    # 拉取微信用户信息失败
    if openid is None:
        return None

    # 判断用户是否存在与本系统
    user_login = UserLoginMethod.query.filter_by(identification = openid).first()
    logger.debug(user_login)
    # 存在则直接返回用户信息
    if user_login:
        data = user_login.to_dict()
        return data
    # 不存在则先新建用户然后返回用户信息
    else:
        try:
            # 新建用户登陆方式
            new_user_login = UserLoginMethod(login_method="WX",
                                             identification=openid,
                                             access_code=None,
                                             nickname=nickname,
                                             sex=sex)
            db.session.add(new_user_login)
            db.session.flush()
            # 提交
            db.session.commit()
        except Exception as e:
            print(e)
            return None

        data = dict(id=new_user_login.id, name=nickname, \
                                admin = new_user_login.admin)
        print(data)
        return data

def create_flag():
    nowTime=datetime.datetime.now().strftime("%Y%m%d%H%M%S") #生成当前时间
    randomNum=random.randint(0,100) #生成的随机整数n，其中0<=n<=100
    if randomNum <= 10:
        randomNum=str(0)+str(randomNum)
    return str(nowTime)+str(randomNum)

def handleWxEvent(msg):
    if msg.event is 'subscribe_scan':
        eventSubscribe(msg)
    elif msg.event is 'unsubscribe':
        eventUnsubscribe(msg)
    elif msg.event is 'scan':
        eventscan(msg)

def eventSubscribe(msg):
    Redis.write(msg.scene_id, msg.source)
    # 创建 access_token
    access_token = Auth.generate_access_token(user_id=msg.source)
    if access_token:
        access_token = access_token.decode('utf-8')
    
    logger.debug("用户初次订阅行为，flag为: ", msg.scene_id)
    # 查询用户详细信息
    user = client.user.get(msg.source)
    # 开始用户登陆或注册
    user_login = wx_login_or_register(user)
    # 缓存用户信息
    Redis.write(msg.source, json.dumps(dict(user_id=user_login['id'],
                                        access_token=access_token,
                                        headimgurl = user['headimgurl'],
                                        nickname=user['nickname'],
                                        admin=user_login['admin']
                                        )))

def eventUnsubscribe(msg):
    pass


def eventscan(msg):
    Redis.write(msg.scene_id, msg.source)
    # 创建 access_token
    access_token = Auth.generate_access_token(user_id=msg.source)
    if access_token:
        access_token = access_token.decode('utf-8')

    logger.debug("已订阅用户扫描行为,flag为: ", msg.scene_id)
    # 查询用户详细信息
    user = client.user.get(msg.source)
    # 开始用户登陆或注册
    user_login = wx_login_or_register(user)
    # 缓存用户信息
    Redis.write(msg.source, json.dumps(dict(user_id=user_login['id'],
                                        access_token=access_token,
                                        headimgurl = user['headimgurl'],
                                        nickname=user['nickname'],
                                        admin=user_login['admin']
                                        )))

def isFlagExist(flag):
    try:
        print(Redis.read(flag))
        openid = Redis.read(flag)
        return json.loads(Redis.read(openid))
    except Exception as e:
        return None
    

# 创建一天有效期的二维码, 参数使用数字id
def make_qrcode(wechat_client, 
                action_name='QR_STR_SCENE', 
                scene_str='test'):
    res = wechat_client.qrcode.create({
        'expire_seconds': 3600 * 24,
        'action_name': action_name,
        'action_info': {
            'scene': {'scene_str': scene_str},
        }
    })
    return res

def get_all_args(req_dict):
    echostr = req_dict.get("echostr")  # 获取随机字符串
    signature = req_dict.get("signature")  # 先获取加密签名
    timestamp = req_dict.get("timestamp")  # 获取时间戳
    nonce = req_dict.get("nonce")  # 获取随机数
    return echostr,signature,timestamp,nonce
