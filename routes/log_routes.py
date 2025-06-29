# routes/log_routes.py
from flask import Blueprint, request, jsonify
from controllers.log_controller import record_click_log

log_bp = Blueprint('log', __name__)

@log_bp.route('/predict_click', methods=['POST'])
def predict_click():
    if not request.is_json:
        return jsonify({'error': '请求体必须为 JSON 格式'}), 400

    data = request.get_json()
    ip = request.remote_addr
    device_id = request.headers.get('User-Agent')
    query_area = data.get('query_area')
    user_id = data.get('user_id', None)

    # ✅ 调用控制器处理业务
    log, click_count = record_click_log(ip, device_id, query_area, user_id)
    show_register = (click_count >= 4)

    return jsonify({
        'message': '点击记录成功',
        'log_id': log.id,
        'click_count': click_count,
        'show_register': show_register
    }), 200


#测试用
# @log_bp.route('/predict_click', methods=['GET'])
# def predict_click_get():
#     ip = request.remote_addr
#     device_id = request.headers.get('User-Agent')
#     # 可选：你可以加 query 参数获取区域，比如 /predict_click?area=北京
#     query_area = request.args.get('area', '未知区域')
#
#     return f"✅ 已记录点击，IP：{ip}，区域：{query_area}"

