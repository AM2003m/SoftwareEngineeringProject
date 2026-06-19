import json
import redis
from config import REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_DECODE_RESPONSES, CACHE_TTL


class CacheManager:
    
    def __init__(self):

        try:
            self.redis_client = redis.Redis(
                host=REDIS_HOST,
                port=REDIS_PORT,
                db=REDIS_DB,
                decode_responses=REDIS_DECODE_RESPONSES
            )
            # تست اتصال
            self.redis_client.ping()
            self.enabled = True
            print("✓  Redis ")
        except redis.ConnectionError:
            print(" X Redis ")
            self.enabled = False
    
    def get(self, key):
        
        if not self.enabled:
            return None
        
        try:
            cached_data = self.redis_client.get(key)
            if cached_data:
                return json.loads(cached_data)
            return None
        except Exception as e:
            print(f" Cache: {e}")
            return None
    
    def set(self, key, value, ttl=CACHE_TTL):
        
        if not self.enabled:
            return False
        
        try:
            serialized_data = json.dumps(value)
            self.redis_client.setex(key, ttl, serialized_data)
            return True
        except Exception as e:
            print(f"Cache: {e}")
            return False
    
    def delete(self, key):
        
        if not self.enabled:
            return False
        
        try:
            self.redis_client.delete(key)
            return True
        except Exception as e:
            print(f"Cache: {e}")
            return False
    
    def clear_all(self):
        
        if not self.enabled:
            return False
        
        try:
            self.redis_client.flushdb()
            return True
        except Exception as e:
            print(f"Cache: {e}")
            return False
    
    def get_stats(self):
        
        if not self.enabled:
            return {'enabled': False}
        
        try:
            info = self.redis_client.info()
            return {
                'enabled': True,
                'used_memory_human': info.get('used_memory_human', 'N/A'),
                'total_keys': self.redis_client.dbsize(),
                'connected_clients': info.get('connected_clients', 0),
            }
        except Exception as e:
            print(f"خطا در دریافت آمار: {e}")
            return {'enabled': False}


cache = CacheManager()
