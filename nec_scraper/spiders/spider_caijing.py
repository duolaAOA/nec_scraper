# -*- coding: utf-8 -*-

import jieba.analyse
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisCrawlSpider

from nec_scraper.items import ArticleItem


class Spider_caijing(RedisCrawlSpider):

    # 新闻 spider

    name = "caijing"
    redis_key = "caijing_start_urls"
    allowed_domains = ['caijing.com.cn']

    rules = (Rule(
        LinkExtractor(
            allow=r'caijing.com.cn/\d{8}/\d*',
            deny=(r'.*photos.*', '.*politics.*')),
        callback="parse_article",
        follow=True), )

    def parse_article(self, response):
        
        # 财经网文章解析
        # :param response:
        # :return:  item

        try:
            item = ArticleItem()
            title = response.xpath('''//*[@id='cont_title']/text()''').extract_first("")
            content = ''.join(response.xpath('''//*[@id='the_content']/p/text()''').extract())
            item['articleTitle'] = title
            item['articleContent'] = content
            item['articleUrl'] = response.url
            tags = jieba.analyse.extract_tags(content, topK=20, withWeight=False)
            item['articleFirstTag'] = tags[0]
            item['articleSecondTag'] = tags[1]
            item['articleThirdTag'] = tags[2]
            yield item
        except:
            self.logger.info('item in article failed')

