# -*-coding:utf-8 -*-
import time

import redis


Time = lambda: time.strftime('%Y-%m-%d %H:%M:%S')


class StatcollectorMiddleware(object):
    """初始化"""
    r = redis.Redis(host="127.0.0.1", port="6379", db=0)
    timer = lambda: time.strftime('%Y-%m-%d %H:%M:%S')

    def __init__(self, settings):
        REDIS_HOST = settings.get('REDIS_HOST')
        REDIS_PORT = settings.get('REDIS_PORT')
        REDIS_DB = settings.get('FLASK_DB')
        STATS_KEYS = settings.get('STATS_KEYS')
        self.r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
        self.stats_keys = STATS_KEYS

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_request(self, request, spider):
        self.formatStats(spider.crawler.stats.get_stats())

    def formatStats(self, stats):
        for key in self.stats_keys:
            key_value = stats.get(key, None)
            if not key_value:
                continue
            value = {"value": [Time(), key_value]}
            self.r.rpush(key, value)
