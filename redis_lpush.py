# -*-coding:utf-8 -*-

import redis
from nec_scraper import settings

db_url = getattr(settings, 'REDIS_RATELIMIT_DB_URL', "redis://localhost:6379/0")
try:
    r = redis.from_url(db_url)
    r.delete("huxiu:start_urls")
    huxiuBaseUrl = 'https://www.huxiu.com'
    r.lpush("huxiu:start_urls", huxiuBaseUrl)
    print("Connection Success!")
except ConnectionError:
    print("Connection Failed!")
