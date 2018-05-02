# -*-coding:utf-8 -*-

import re

from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisCrawlSpider

from nec_scraper import settings
from nec_scraper import lxml_select as ls
from nec_scraper.items import ArticleItem


class WangYiSpider(RedisCrawlSpider):
    """
    财经网  Spider
    """
    name = 'wangyi'
    redis_key = settings.wangyi_start_urls
    allowed_domains = ['news.163.com']

    rules = (
        Rule(LinkExtractor(allow='/\d{2}/\d{4}/\d{2}/*'),
             callback='parse_article',
             follow=True),
    )

    def parse_article(self, response):
        """
        网易新闻文章解析
        :param response:
        :return:  item
        """
        try:
            article_id = re.search(r'(?<=\/)[A-Z0-9]{16}(.*?)', response.url).group()
            title = response.xpath(ls.WANGYI_TITLE).extract_first("")
            content = ''.join(response.xpath(ls.WANGYI_CONTENT).extract())

            item = ArticleItem()
            item['articleId'] = article_id
            item['articleTitle'] = title
            item['articleContent'] = content
            yield item
        except:
            self.logger.info('item in article failed')
