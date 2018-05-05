# -*- coding: utf-8 -*-

import redis

from nec_scraper.commands.mysqlHelper import MysqlHelper
import nec_scraper.settings as prime_settings


def init():
    print("try insert eCommerced_Id")
    try:
        db = MysqlHelper()
        insert_sql = "insert into ECommerce(eCommerceId, eCommerceName, eCommerceUrl) " \
                     "values( 1, 'jd', 'https://item.jd.com');".encode(encoding='utf-8')

        db.insert(insert_sql)
        print("insert eCommerceId success")
    except:
        print("insert eCommerceId failed")

    print("pushing jd_start_url......")
    try:
        r = redis.Redis(prime_settings.REDIS_HOST, prime_settings.REDIS_PORT)
        r.delete("jd_start_urls")
        r.delete("jd_dupefilter")
        r.delete("jd_requests")
        r.lpush("jd_start_urls", 'https://item.jd.com/17878441894.html')
        print("pushing jd_start_url success")
    except Exception:
        print("pushing jd_start_url failed")


if __name__ == '__main__':
    init()
