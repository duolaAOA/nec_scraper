# -*-coding:utf-8 -*-

import redis
from nec_scraper import settings


class StartPush(object):
    """
    redis   url队列
    """
    def push(self):

        print("pushing start_url......")
        try:
            r = redis.Redis(settings.REDIS_HOST, settings.REDIS_PORT)
            # huxiu
            r.delete(settings.huxiu_start_urls)
            r.delete(settings.huxiu_dupefilter)
            r.delete(settings.huxiu_requests)
            r.lpush(settings.huxiu_start_urls, settings.huxiu_base_url)

            print("pushing start_url success")
        except:
            print("pushing start_url failed")