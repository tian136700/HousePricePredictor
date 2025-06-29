from utils.redis_client import redis_client

def save_sms_code_to_redis(phone, code, expire_sec=300):
    key = f"sms:{phone}"
    redis_client.set(key, code, ex=expire_sec)

def verify_sms_code_from_redis(phone, input_code):
    key = f"sms:{phone}"
    real_code = redis_client.get(key)
    if real_code is None:
        return False
    return input_code == real_code
