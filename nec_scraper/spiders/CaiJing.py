# -*-coding:utf-8 -*-

import re

from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisCrawlSpider

from nec_scraper import settings
from nec_scraper import lxml_select as ls
from nec_scraper.items import ArticleItem


class CaiJingWangSpider(RedisCrawlSpider):
    """
    财经网  Spider
    """
    name = "caijing"
    redis_key = settings.caijing_start_urls
    allowed_domains = ['caijing.com.cn']

    rules = (Rule(
        LinkExtractor(
            allow=r"caijing.com.cn/\d{8}/\d*",
            deny=(r".*photos.*", r".*politics.*")),
        callback="parse_article",
        follow=True), )

    def parse_article(self, response):
        """
        文章解析
        :param response:
        :return:  item
        """
        try:
            article_id = re.search(r'\d+', response.url).group()
            title = response.xpath(ls.CAIJING_TITLE).extract_first("")
            try:
                content = ''.join(response.xpath(ls.CAIJING_CONTENT).extract())
            except IndexError:
                raise IndexError("Unable to access web content!")

            item = ArticleItem()
            item['articleId'] = article_id
            item['articleTitle'] = title
            item['articleContent'] = content
            yield item
        except:
            self.logger.info('item in article failed')
