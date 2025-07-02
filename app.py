from flask import Flask
from database.db_config import  init_db  # 初始化数据库
from routes.auth_routes import auth_bp
from routes.log_routes import log_bp
from routes.index_routes import index_bp
from routes.predict_routes import predict_bp  # ✅ 导入预测路由


app = Flask(__name__)

# ✅ 初始化数据库
init_db(app)

# ✅ 注册路由蓝图
app.register_blueprint(auth_bp)
app.register_blueprint(log_bp)
app.register_blueprint(index_bp)
app.register_blueprint(predict_bp)#预测



if __name__ == '__main__':
    if __name__ == '__main__':
        import os

        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    app.run(host='0.0.0.0', port=5000, debug=True)  # ✅ 已开启 debug 热更新
