# db_config.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from utils.FileManagement import read_conf
from sqlalchemy import text

db = SQLAlchemy()

def init_db(app):
    mysql_config = read_conf()["Mysql"]
    username = mysql_config["Username"]
    password = mysql_config["Password"]
    host = mysql_config["Host"]
    port = mysql_config["Port"]
    dbname = mysql_config["Name"]

    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{username}:{password}@{host}:{port}/{dbname}?charset=utf8'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

def test_connection():
    try:
        with db.engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("✅ 数据库连接成功")
    except Exception as e:
        print("❌ 数据库连接失败:", e)

# ✅ 运行 db_config.py 时执行连接测试
if __name__ == "__main__":
    app = Flask(__name__)
    init_db(app)
    with app.app_context():
        test_connection()

# 测试需进入主目录测试： python database/basic/db_config.py？