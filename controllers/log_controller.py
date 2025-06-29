from sqlalchemy import or_
from database.db_config import db
from models.ip_log import IPLog
from datetime import datetime

def record_click_log(ip, device_id, query_area, user_id):
    # ✅ 查询点击次数
    click_count = IPLog.query.filter(
        or_(IPLog.ip_address == ip, IPLog.device_id == device_id)
    ).count() + 1  # 当前这次也算进来

    # ✅ 写入本次点击
    new_log = IPLog(
        ip_address=ip,
        device_id=device_id,
        query_area=query_area,
        user_id=user_id,
        created_at=datetime.utcnow()
    )
    db.session.add(new_log)
    db.session.commit()

    return new_log, click_count
