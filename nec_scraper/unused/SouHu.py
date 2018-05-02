# -*-coding:utf-8 -*-

import re

from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisCrawlSpider

from nec_scraper import settings
from nec_scraper import lxml_select as ls
from nec_scraper.items import ArticleItem


class SouhuSpider(RedisCrawlSpider):
    """
    搜狐  Spider
    """
    name = 'souhu'
    redis_key = settings.souhu_start_urls
    allowed_domains = ['sohu.com']

    rules = (
        Rule(LinkExtractor(allow=r'/a/\d+'),
             callback='parse_article',
             follow=True),
    )

    def parse_article(self, response):
        """
        搜狐新闻文章解析
        :param response:
        :return:  item
        """
        try:
            article_id = re.search(r'\d+_.*', response.url).group()
            title = response.xpath(ls.SOUHU_TITLE).extract_first("").strip()
            content = ''.join(response.xpath(ls.SOUHU_CONTENT).extract())

            item = ArticleItem()
            item['articleId'] = article_id
            item['articleTitle'] = title
            item['articleContent'] = content
            yield item
        except:
            self.logger.info('item in article failed')
