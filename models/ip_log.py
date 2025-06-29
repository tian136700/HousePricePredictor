# models/ip_log.py
from database.db_config import db

class IPLog(db.Model):
    __tablename__ = 'ip_logs'

    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(100), nullable=False)
    device_id = db.Column(db.String(200), nullable=False)
    query_area = db.Column(db.String(100))
    user_id = db.Column(db.Integer, nullable=True)  # ✅ 可为空
    created_at = db.Column(db.DateTime)
