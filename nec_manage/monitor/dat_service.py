# -*-coding:utf-8 -*-
import json

import redis

HOST = '127.0.0.1'
PORT = 6379
DB_ID = 13


def save_data(spider_name, json_str):
    r = redis.Redis(HOST, PORT, DB_ID)
    js = dict(json.loads(json_str))
    r.set(spider_name, js)


def query_data(spider_name):
    r = redis.Redis(HOST, PORT, DB_ID)
    print(r.get(spider_name))
