from flask import Blueprint

index_bp = Blueprint('index', __name__)

@index_bp.route('/')
def home():
    return '🏠 这是房价预测系统的首页，欢迎使用！'
