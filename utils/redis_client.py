# utils/redis_client.py
import redis

# 建议配置从配置文件读取，这里写死示例
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
# utils/redis_client.py
import redis

redis_client = redis.StrictRedis(
    host='localhost',
    port=6379,
    db=0,
    decode_responses=True
)

# ✅ 测试连接
try:
    redis_client.set('test_key', 'hello', ex=60)
    print("✅ Redis 已连接，测试值 test_key =", redis_client.get('test_key'))
except Exception as e:
    print("❌ Redis 连接失败，请确认 Redis 服务已开启")
    print(e)
