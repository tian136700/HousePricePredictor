# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils.FileManagement import read_conf
# ✅ 推荐的写法（SQLAlchemy 2.0+）
from sqlalchemy.orm import declarative_base
Base = declarative_base()

from sqlalchemy import text



mysql_config = read_conf()["Mysql"]
host = mysql_config["Host"]
port = mysql_config["Port"]
username = mysql_config["Username"]
password = mysql_config["Password"]
databaseName = mysql_config["Name"]

Base = declarative_base()
engine = create_engine(
    f'mysql+pymysql://{username}:{password}@{host}:{port}/{databaseName}?charset=utf8',
    max_overflow=0,  # 超过连接池大小外最多创建的连接
    pool_size=200,  # 连接池大小
    pool_pre_ping=True,
    pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
    pool_recycle=-1  # 多久之后对线程池中的线程进行一次连接的回收（重置）
)

Session = sessionmaker(bind=engine)


def sessions():
    return Session()


if __name__ == "__main__":
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ 数据库连接成功！")
    except Exception as e:
        print("❌ 数据库连接失败：", e)




