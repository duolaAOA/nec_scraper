# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider

from nec_scraper import lxml_select as ls


class HuxiuSpider(RedisSpider):
    name = "huxiu"
    redis_key = "huxiu:start_urls"
    huxiu_baseurls = "https://www.huxiu.com"
    channelhref = set()
    tagsHasBeenCrawled = False
    tags = set()

    def parse(self, response):
        channelhrefs = response.xpath(ls.CHANNELHREFS_X).extract()
        for href in channelhrefs:
            href = self.huxiu_baseurls + href
            self.channelhref.add(href)
        for href in self.channelhref:
            yield scrapy.Request(url=href, callback=self.parse_channel)

    def parse_channel(self, response):
        """
        处理每个分类栏目
        :param response:   channelhrefs
        :return:
        """
        topArticles=[]

        hotArticles=[]

        specials=[]

        authors=[]

        try:
            topArticlesHrefs = response.xpath(ls.topArticlesHrefs_X)
            for href in topArticlesHrefs:
                topArticles.append(self.huxiu_baseurls + href)
            try:
                for href in topArticles:
                    yield scrapy.Request(url=href, callback=self.parse_article)

            except Exception as e:
                self.logger.info('topArticlesHrefs faield:  ' + repr(str(e)))

        except Exception as e:
            self.logger.info('topArticles faield:  ' + repr(str(e)))

    def parse_article(self, response):
        pass