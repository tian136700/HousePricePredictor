from flask import jsonify

def success_response(data=None, message='操作成功', code=200):
    """
    返回统一格式的成功响应
    :param data: 要返回的业务数据（字典或列表）
    :param message: 提示信息
    :param code: 状态码（默认 200）
    """
    return jsonify({
        'status': 'success',
        'message': message,
        'data': data
    }), code


def error_response(message='发生错误', code=400):
    """
    返回统一格式的错误响应
    :param message: 错误信息
    :param code: 状态码（默认 400）
    """
    return jsonify({
        'status': 'error',
        'message': message
    }), code
