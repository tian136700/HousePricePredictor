from database.db_config import db
from datetime import datetime

class HousePrice(db.Model):
    __tablename__ = 'housing_prices'  # 数据库中的表名

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='记录ID')
    region_code = db.Column(db.String(10), nullable=False, comment='行政区划代码')
    city = db.Column(db.String(50), nullable=False, comment='城市')
    province = db.Column(db.String(50), nullable=False, comment='所属省份')
    year = db.Column(db.Integer, nullable=False, comment='年份')
    month = db.Column(db.Integer, nullable=False, comment='月份')
    avg_price_per_m2 = db.Column(db.Integer, nullable=False, comment='二手房均价（元/㎡）')  # ✅ 改了字段名
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='记录创建时间')
