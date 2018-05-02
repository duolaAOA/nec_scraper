# -*- coding: utf-8 -*-

import re

from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisCrawlSpider

from nec_scraper import settings
from nec_scraper import lxml_select as ls
from nec_scraper.items import ArticleItem


class HuxiuSpider(RedisCrawlSpider):
    """
    虎嗅网 Spider
    """
    name = "huxiu"
    redis_key = settings.huxiu_start_urls
    allowed_domains = ['huxiu.com']

    rules = (Rule(
        LinkExtractor(allow=r"/article/"),
        callback="parse_article",
        follow=True), )

    def parse_article(self, response):
        """
        虎嗅网文章解析
        :param response:
        :return:  item
        """
        try:
            article_id = re.search(r'\d+', response.url).group()
            title = response.xpath(ls.HUXIU_TITLE).extract_first("").strip()
            content = ''.join(response.xpath(ls.HUXIU_CONTENT).extract())

            item = ArticleItem()
            item['articleId'] = article_id
            item['articleTitle'] = title
            item['articleContent'] = content
            yield item
        except:
            self.logger.info('item in article failed')
