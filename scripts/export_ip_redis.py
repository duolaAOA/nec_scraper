# -*-coding:utf-8 -*-

import redis

client = redis.Redis(host='127.0.0.1', port='6379', db=9)
print(client.keys())
proxy = client.hgetall("hproxy")
cou = 0
with open('ip.txt', 'w', encoding='utf8') as f:
    for i in proxy.keys():
        cou += 1
        f.write('http://'+ i.decode() + '\n')
print(cou)