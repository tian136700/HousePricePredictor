from flask import Blueprint, request
from controllers.log_controller import record_click_log
from utils.response import success_response, error_response  # ✅ 引入封装的响应函数

log_bp = Blueprint('log', __name__)

@log_bp.route('/predict_click', methods=['POST'])
def predict_click():
    if not request.is_json:
        return error_response('请求体必须为 JSON 格式', 400)

    data = request.get_json()
    ip = request.remote_addr
    device_id = data.get('device_id')
    query_area = data.get('query_area')

    # ✅ 调用控制器处理业务
    log, click_count = record_click_log(ip, device_id, query_area)
    show_register = (click_count >= 4)

    return success_response(
        data={
            'log_id': log.id,
            'click_count': click_count,
            'show_register': show_register
        },
        message='点击记录成功'
    )
