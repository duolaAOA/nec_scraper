# -*-coding:utf-8 -*-

import redis

from nec_scraper import settings as prime_settings


class MonitorInit(object):
    """监控任务初始化"""
    @staticmethod
    def start():
        print("pushing start_url......")
        try:
            r = redis.Redis(prime_settings.REDIS_HOST, prime_settings.REDIS_PORT)
            # 队列清空
            r.delete(prime_settings.request_count)
            r.delete(prime_settings.response_count)
            r.delete(prime_settings.response_status200_count)
            r.delete(prime_settings.item_scraped_count)

            print("pushing start_url success")

        except:
            print("pushing start_url failed")
