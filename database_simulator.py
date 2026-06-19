"""
شبیه‌سازی یک Database کند
این ماژول نقش یک دیتابیس واقعی را بازی می‌کند که پاسخ‌دهی آن زمان‌بر است
"""

import time
import random
from config import DB_DELAY_MIN, DB_DELAY_MAX


class DatabaseSimulator:
    """
    کلاس شبیه‌سازی دیتابیس که عملیات خواندن داده را با تاخیر شبیه‌سازی می‌کند
    """
    
    def __init__(self):
        """
        ایجاد یک دیتابیس شبیه‌سازی‌شده با داده‌های نمونه
        """
        self.data = {
            'user:1': {'id': 1, 'name': 'علی احمدی', 'email': 'ali@example.com', 'age': 25},
            'user:2': {'id': 2, 'name': 'سارا محمدی', 'email': 'sara@example.com', 'age': 28},
            'user:3': {'id': 3, 'name': 'رضا کریمی', 'email': 'reza@example.com', 'age': 32},
            'user:4': {'id': 4, 'name': 'مریم حسینی', 'email': 'maryam@example.com', 'age': 24},
            'user:5': {'id': 5, 'name': 'محمد رضایی', 'email': 'mohammad@example.com', 'age': 30},
            'user:6': {'id': 6, 'name': 'فاطمه نوری', 'email': 'fatemeh@example.com', 'age': 27},
            'user:7': {'id': 7, 'name': 'حسین یوسفی', 'email': 'hossein@example.com', 'age': 35},
            'user:8': {'id': 8, 'name': 'زهرا صادقی', 'email': 'zahra@example.com', 'age': 29},
            'user:9': {'id': 9, 'name': 'امیر مرادی', 'email': 'amir@example.com', 'age': 31},
            'user:10': {'id': 10, 'name': 'نرگس کاظمی', 'email': 'narges@example.com', 'age': 26},
        }
        self.query_count = 0
    
    def get(self, key):
        """
        دریافت داده از دیتابیس با شبیه‌سازی تاخیر
        
        Args:
            key (str): کلید داده مورد نظر
            
        Returns:
            dict: داده مورد نظر یا None
        """
        # شبیه‌سازی تاخیر دیتابیس (مثلاً Query پیچیده، Network Latency و...)
        delay = random.uniform(DB_DELAY_MIN, DB_DELAY_MAX)
        time.sleep(delay)
        
        self.query_count += 1
        
        return self.data.get(key)
    
    def get_query_count(self):
        """
        دریافت تعداد کل Query های اجرا شده روی دیتابیس
        
        Returns:
            int: تعداد Query ها
        """
        return self.query_count
    
    def reset_query_count(self):
        """
        ریست کردن شمارنده Query ها
        """
        self.query_count = 0


# نمونه سراسری برای استفاده در کل برنامه
db = DatabaseSimulator()
