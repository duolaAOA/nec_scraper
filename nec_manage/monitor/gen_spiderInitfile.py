# -*- coding: utf-8 -*-

import json
def arr2str(arr):
    return ', '.join(map(lambda x: "'" + x + "'", arr))


# 爬虫初始化模板
spider_init_template = \
    """# -*- coding: utf-8 -*-
    
    import redis
    
    import nec_scraper.settings as prime_settings
    
    
    def init():
        print("pushing %s_start_url......")
        try:
            r = redis.Redis(prime_settings.REDIS_HOST, prime_settings.REDIS_PORT)
            r.delete("%s_start_urls")
            r.delete("%s_dupefilter")
            r.delete("%s_requests")
            r.lpush("%s_start_urls", %s)
            print("pushing %s_start_url success")
        except Exception:
            print("pushing %s_start_url failed")
    
    
    if __name__ == '__main__':
        init()
    """


def generate_spider_init(jsonfile):
    """生成新闻初始化代码"""
    print(jsonfile)
    js = dict(json.loads(jsonfile))
    arr = (js['name'], js['name'], js['name'], js['name'], js['name'],
           arr2str(js['start_urls']), js['name'], js['name'])
    ok = spider_init_template % arr
    filename = "../spiderInit/" + "spiderInit_" + js['name'] + ".py"
    with open(filename, 'w', encoding='utf8') as f:
        f.write(ok)
    print("success")
