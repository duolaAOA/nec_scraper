# -*-coding:utf-8 -*-

import re

from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from nec_scraper.scrapy_redis.spiders import RedisCrawlSpider

from nec_scraper import settings
from nec_scraper import lxml_select as ls
from nec_scraper.items import ArticleItem


class WallStreeSpider(RedisCrawlSpider):
    """
    华尔街  Spider
    """
    name = 'wallstreetcn'
    redis_key = settings.huaerjie_start_urls
    allowed_domains = ['wallstreetcn.com']

    rules = [
        Rule(LinkExtractor(allow='/articles/'),
             callback='parse_article',
             follow=True)
    ]

    def parse_article(self, response):
        """
        华尔街文章解析
        :param response:
        :return:  item
        """
        try:
            article_id = re.search(r'\d+', response.url).group()
            title = response.xpath(ls.HUAERJIE_TITLE).extract_first("")
            content = ''.join(response.xpath(ls.HUAERJIE_CONTENT).extract())

            item = ArticleItem()
            item['articleId'] = article_id
            item['articleTitle'] = title
            item['articleContent'] = content
            yield item
        except:
            self.logger.info('item in article failed')
