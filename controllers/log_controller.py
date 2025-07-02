from database.db_config import db
from models.ip_log import IPLog
from sqlalchemy import or_
from datetime import datetime

def record_click_log(ip, device_id, query_area, user_id=None):
    # ✅ 如果没有传 user_id，尝试查历史记录中有没有同 IP 或 device_id 对应的 user_id
    if not user_id:
        existing_log = IPLog.query.filter(
            or_(
                IPLog.ip_address == ip,
                IPLog.device_id == device_id
            ),
            IPLog.user_id.isnot(None)
        ).order_by(IPLog.created_at.desc()).first()

        if existing_log:
            user_id = existing_log.user_id

    # ✅ 统计点击次数（包含这次）
    click_count = IPLog.query.filter(
        or_(IPLog.ip_address == ip, IPLog.device_id == device_id)
    ).count() + 1

    # ✅ 写入本次点击日志
    new_log = IPLog(
        ip_address=ip,
        device_id=device_id,
        query_area=query_area,
        user_id=user_id,  # ✅ 这里 user_id 一定有定义，不会再报错
        created_at=datetime.utcnow()
    )
    db.session.add(new_log)
    db.session.commit()

    return new_log, click_count
def bind_logs_to_user(user_id, ip_address=None, device_id=None):
    """
    将所有未绑定 user_id 的点击日志记录绑定到该用户上
    （匹配 ip 和/或 device_id）
    """
    if not user_id:
        return

    query = IPLog.query.filter(IPLog.user_id == None)

    if ip_address and device_id:
        query = query.filter(or_(
            IPLog.ip_address == ip_address,
            IPLog.device_id == device_id
        ))
    elif ip_address:
        query = query.filter(IPLog.ip_address == ip_address)
    elif device_id:
        query = query.filter(IPLog.device_id == device_id)
    else:
        return  # 无匹配条件

    logs = query.order_by(IPLog.created_at.asc()).all()

    for log in logs:
        log.user_id = user_id

    db.session.commit()  # ✅ 一次性提交所有修改