# models/ip_log.py
from database.db_config import db
from datetime import datetime

class IPLog(db.Model):
    __tablename__ = 'ip_logs'

    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(64), nullable=False)
    device_id = db.Column(db.String(128), nullable=True)
    query_area = db.Column(db.String(128), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
