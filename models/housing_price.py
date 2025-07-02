from database.db_config import db
from datetime import datetime

class HousingPrice(db.Model):
    __tablename__ = 'housing_prices'

    id = db.Column(db.Integer, primary_key=True)
    region_code = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    province = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    avg_price_per_m2 = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
