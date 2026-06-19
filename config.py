"""
تنظیمات پروژه Redis Caching
"""

# Redis Configuration
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_DECODE_RESPONSES = True

# Cache Configuration
CACHE_TTL = 300  # Time to live: 5 minutes

# Database Simulator Configuration
DB_DELAY_MIN = 0.5  # حداقل تاخیر شبیه‌سازی دیتابیس (ثانیه)
DB_DELAY_MAX = 2.0  # حداکثر تاخیر شبیه‌سازی دیتابیس (ثانیه)

# Benchmark Configuration
NUM_REQUESTS = 50  # تعداد درخواست‌ها برای تست
NUM_UNIQUE_KEYS = 10  # تعداد کلیدهای یونیک
