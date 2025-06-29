from models.user import User
from database.db_config import db
from utils.response import success_response, error_response
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime
import random
from utils.sms_cache_redis import save_sms_code_to_redis
from controllers.log_controller import bind_logs_to_user  # 确保你写了这个
from flask import request
def register_user(data):
    username = data.get('username')
    password = data.get('password')
    phone = data.get('phone')
    email = data.get('email')
    code = data.get('sms_code')

    # ✅ 检查必填字段
    if not all([username, password, phone, email, code]):
        return error_response('用户名、密码、手机号、邮箱和验证码均为必填')

    # ✅ 检查唯一性
    if User.query.filter_by(username=username).first():
        return error_response('用户名已存在')
    if User.query.filter_by(phone=phone).first():
        return error_response('该手机号已注册')
    if User.query.filter_by(email=email).first():
        return error_response('该邮箱已注册')

    # ✅ 验证码有效性
    # if not verify_sms_code_from_redis(phone, code):
    #     return error_response('验证码错误或已过期')

    # ✅ 注册用户
    hashed_pw = generate_password_hash(password)
    user = User(
        username=username,
        password=hashed_pw,
        phone=phone,
        email=email,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.session.add(user)

    # ✅ 标记验证码为已使用
    # sms.is_used = True
    db.session.commit()

    # 注册成功后执行绑定
    ip = request.remote_addr
    device_id = request.headers.get('User-Agent')
    bind_logs_to_user(user.id, ip_address=ip, device_id=device_id)

    return success_response({'user_id': user.id}, '注册成功')


def login_user(data):
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return error_response('用户名和密码不能为空')

    user = User.query.filter_by(username=username).first()
    if not user:
        return error_response('用户名不存在')

    if not check_password_hash(user.password, password):
        return error_response('密码错误')

    return success_response({
        'user_id': user.id,
        'username': user.username
    }, message='登录成功')
def send_sms_code(data):
    phone = data.get('phone')
    if not phone:
        return error_response('手机号不能为空')

    code = str(random.randint(100000, 999999))
    save_sms_code_to_redis(phone, code)

    print(f"【测试】验证码：{code} 已存入 Redis")
    return success_response(message='验证码已发送')