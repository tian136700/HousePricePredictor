from flask import Blueprint, request
from controllers.auth_controller import register_user, login_user, send_sms_code
from utils.response import success_response, error_response
auth_bp = Blueprint('auth', __name__)

# ✅ 注册接口
@auth_bp.route('/register', methods=['POST'])
def register():
    if not request.is_json:
        return error_response('请求体必须是 JSON 格式'), 400

    data = request.get_json()
    return register_user(data)


# ✅ 登录接口
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    return login_user(data)

# ✅ 发送短信验证码接口
@auth_bp.route('/send_sms_code', methods=['POST'])
def send_sms_code_route():
    data = request.get_json()
    return send_sms_code(data)
