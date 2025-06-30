from flask import Flask
from database.db_config import db, init_db  # ✅ 打开注释，初始化数据库
from routes.auth_routes import auth_bp
from routes.log_routes import log_bp
from routes.index_routes import index_bp
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///house_price.db'
# app.config['SECRET_KEY'] = 'your_secret_key'

# ✅ 初始化数据库
# db.init_app(app)
init_db(app)

# ✅ 注册路由蓝图
app.register_blueprint(auth_bp)
app.register_blueprint(log_bp)
app.register_blueprint(index_bp)

# @app.route('/')
# def homepage():
#     return '🏠 欢迎来到房价预测系统首页！'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # ✅ 已开启 debug 热更新
