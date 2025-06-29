from database.db_config import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='用户ID')
    username = db.Column(db.String(50), nullable=False, unique=True, comment='用户名')
    password = db.Column(db.String(255), nullable=False, comment='加密后的密码')
    phone = db.Column(db.String(20), unique=True, nullable=False, comment='手机号')
    email = db.Column(db.String(100), unique=True, nullable=False, comment='邮箱')
    avatar_url = db.Column(db.String(255), nullable=True, comment='头像URL')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='注册时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='最近更新时间')
