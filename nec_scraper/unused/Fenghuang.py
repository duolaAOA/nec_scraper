# -*-coding:utf-8 -*-

import re

from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from nec_scraper.scrapy_redis.spiders import RedisCrawlSpider

from nec_scraper import settings
from nec_scraper import lxml_select as ls
from nec_scraper.items import ArticleItem


class FengHuangSpider(RedisCrawlSpider):
    """
    凤凰网  Spider
    """
    name = "fenghuang"
    redis_key = settings.caijing_start_urls
    allowed_domains = ['news.ifeng.com']

    rules = (Rule(
        LinkExtractor(
            allow=r"news.ifeng.com/a/\d{8}/\d*",),
        callback="parse_article",
        follow=True), )

    def parse_article(self, response):
        """
        凤凰新闻文章解析
        :param response:
        :return:  item
        """
        try:
            article_id = re.search(r'\d+', response.url).group()
            title = response.xpath(ls.FENGHUANG_TITLE).extract_first("")
            content = ''.join(response.xpath(ls.FENGHUANG_CONTENT).extract())

            item = ArticleItem()
            item['articleId'] = article_id
            item['articleTitle'] = title
            item['articleContent'] = content
            yield item
        except:
            self.logger.info('item in article failed')
