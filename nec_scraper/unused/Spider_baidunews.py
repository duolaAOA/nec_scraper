#  -*- coding: utf-8 -*-
import re
import json

import requests
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from nec_scraper.scrapy_redis.spiders import RedisCrawlSpider

from nec_scraper.items import DomTreeItem


class SpiderBaiduNews(RedisCrawlSpider):

    name = 'baidunews'
    redis_key = 'baidunews:start_urls'

    rules = {
        Rule(LinkExtractor(allow=('https://.*', 'http://.*'), deny=()),callback='processDom',follow=True),
    }

    # 获取商品信息
    def processDom(self,response):
        item = DomTreeItem()
        # 提取url
        url = response.url
        item['url'] = url
        # 提取html
        html = requests.get(url=url).content
        for i in ('utf8', 'gb18030'):
            try:
                html = html.decode(i).encode('utf8')
                break
            except:
                continue

        item['html'] = html
        yield item

