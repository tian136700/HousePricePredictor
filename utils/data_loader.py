import pandas as pd
from database.db_config import db


def load_price_series(province: str, city: str):
    query = """
        SELECT year, month, avg_price_per_m2
        FROM housing_prices
        WHERE province = %s AND city = %s
        ORDER BY year, month
    """
    # 用 SQLAlchemy 的 raw_connection 来获得原始 PyMySQL 连接
    conn = db.engine.raw_connection()
    try:
        # ✅ 注意：params 必须是 tuple，不是 list，不是 dict
        df = pd.read_sql(query, conn, params=(province, city))
    finally:
        conn.close()

    if df.empty:
        return None

    df['date'] = pd.to_datetime(df['year'].astype(str) + '-' + df['month'].astype(str) + '-01')
    df.set_index('date', inplace=True)
    return df[['avg_price_per_m2']]