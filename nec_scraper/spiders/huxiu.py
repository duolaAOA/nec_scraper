# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider

from nec_scraper import lxml_select


class HuxiuSpider(RedisSpider):
    name = "huxiu"
    redis_key = "huxiu:start_urls"
    huxiu_baseurls = "https://www.huxiu.com/"
    channelhref = set()
    tagsHasBeenCrawled = False
    tags = set()

    def parse(self, response):
        channelhrefs = response.xpath(lxml_select.CHANNELHREFS_X).extract()
        for href in channelhrefs:
            href = self.huxiu_baseurls + href
            self.channelhref.add(href)
        for href in self.channelhref:
            yield scrapy.Request(url=href, callback=self.parse_channel)

    def parse_channel(self, response):
        pass
