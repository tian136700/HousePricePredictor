from flask import Blueprint, jsonify, request
from database.db_config import db
from models.house_price import HousePrice  # 你必须有这个模型定义好
from flask import Blueprint, render_template
index_bp = Blueprint('index', __name__)


@index_bp.route('/')
def home():
    return render_template('index.html')  # 渲染 templates/index.html 文件

# ✅ 获取所有省份（不重复）
@index_bp.route('/provinces', methods=['GET'])
def get_provinces():
    print("✅ 省份接口被调用")
    provinces = db.session.query(HousePrice.province).distinct().order_by(HousePrice.province).all()
    province_list = [p[0] for p in provinces if p[0]]
    return jsonify({'success': True, 'data': {'provinces': province_list}})

@index_bp.route('/cities', methods=['GET'])
def get_cities():
    province = request.args.get('province')
    if not province:
        return jsonify({'success': False, 'message': '缺少 province 参数'}), 400
    cities = db.session.query(HousePrice.city).filter_by(province=province).distinct().order_by(HousePrice.city).all()
    city_list = [c[0] for c in cities if c[0]]
    return jsonify({'success': True, 'data': {'cities': city_list}})

# 测试：http://127.0.0.1:5000/provinces
# http://127.0.0.1:5000/cities?province=%E5%9B%9B%E5%B7%9D%E7%9C%81
