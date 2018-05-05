# -*-coding:utf-8 -*-
import json

import redis
from tld import get_tld


HOST = '127.0.0.1'
PORT = 6379
DB_ID = 13


def get_redis():
    return redis.Redis(HOST, PORT, DB_ID)


def save_data(spider_name, json_str):
    r = redis.Redis(HOST, PORT, DB_ID)
    js = dict(json.loads(json_str))
    r.set(spider_name, js)


def query_data(spider_name):
    r = redis.Redis(HOST, PORT, DB_ID)
    print(r.get(spider_name))


def split_target_urls(urls):
    r = get_redis()
    st = set()
    for i in r.keys():
        st.add((i, 'utf8'))
    a, b = [], []
    map(lambda url: a.append(url) if get_tld(url, fail_silently=True) in st else b.append(url), urls)
    return a, b