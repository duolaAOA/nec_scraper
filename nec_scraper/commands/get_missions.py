# -*-coding:utf-8 -*-
import json

import redis
from . import gen_spiderfile
from tld import get_tld

HOST = '127.0.0.1'
PORT = 6379


def init():
    r13 = redis.Redis(HOST, PORT, 13)
    r14 = redis.Redis(HOST, PORT, 14)
    for url in r14.lrange(1, 0, -1):
        js = r13.get(get_tld(url))
        js = js.replace("'", '"')
        js = js.replace('u"', '"')
        gen_spiderfile.generate_spider(js)


if __name__ == "__main__":
    init()
