# -*- coding: utf-8 -*-
import json


def arr2str(arr):
    return ', '.join(map(lambda x: "'" + x + "'", arr))


# 新闻类爬虫模板
spider_template = \
"""# -*- coding: utf-8 -*-

import jieba.analyse
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from nec_scraper.scrapy_redis.spiders import RedisCrawlSpider

from nec_scraper.items import ArticleItem


class Spider_{spider_name}(RedisCrawlSpider):

    # 新闻 spider

    name = "{name}"
    redis_key = "{redis_key}_start_urls"
    allowed_domains = [{allowed_domains}]

    rules = (Rule(
        LinkExtractor(
            allow=r{allow},
            deny=(r{deny})),
        callback="parse_article",
        follow=True), )

    def parse_article(self, response):
        
        # 财经网文章解析
        # :param response:
        # :return:  item

        try:
            item = ArticleItem()
            title = response.xpath(''{title_xpath}'').extract_first("")
            content = ''.join(response.xpath(''{content_xpath}'').extract())
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

"""


def generate_spider(jsonfile):
    """生成新闻爬虫通用代码"""
    print(jsonfile)
    js = dict(json.loads(jsonfile))

    arr = (js['name'], js['name'], js['name'], arr2str(js['allowed_domains']),
           arr2str(js['rule_allow']), arr2str(js['rule_deny']),
           arr2str(js['xpath_title']), arr2str(js['xpath_content']))
    ok = spider_template.format(
        spider_name=arr[0],
        name=arr[1],
        redis_key=arr[2],
        allowed_domains=arr[3],
        allow=arr[4],
        deny=arr[5],
        title_xpath=arr[6],
        content_xpath=arr[7],
    )
    filename = "../spiders/" + 'spider_' + js['name'] + '.py'
    with open(filename, 'w', encoding='utf8') as f:
        f.write(ok)

    print("success")


# 爬虫初始化模板
spider_init_template = \
"""# -*- coding: utf-8 -*-

import redis

import nec_scraper.settings as prime_settings


def init():
    print("pushing %s_start_url......")
    try:
        r = redis.Redis(prime_settings.REDIS_HOST, prime_settings.REDIS_PORT)
        r.delete("%s_start_urls")
        r.delete("%s_dupefilter")
        r.delete("%s_requests")
        r.lpush("%s_start_urls", %s)
        print("pushing %s_start_url success")
    except Exception:
        print("pushing %s_start_url failed")
        
        
if __name__ == '__main__':
    init()
"""


def generate_spider_init(jsonfile):
    """生成新闻初始化代码"""
    print(jsonfile)
    js = dict(json.loads(jsonfile))
    arr = (js['name'],
           js['name'],
           js['name'],
           js['name'],
           js['name'],
           arr2str(js['start_urls']),
           js['name'],
           js['name'])

    ok = spider_init_template % arr
    filename = "../commands/" + "spiderInit_" + js['name'] + ".py"
    with open(filename, 'w', encoding='utf8') as f:
        f.write(ok)
    print("success")


if __name__ == '__main__':
    test_code = """{"name":"caijing", 
    "start_urls": ["http://www.caijing.com.cn"],
    "allowed_domains": ["caijing.com.cn"],
    "rule_allow": ["caijing.com.cn/\\\\d{8}/\\\\d*"],
    "rule_deny": [".*photos.*",".*politics.*"],
    "xpath_title": ["//*[@id='cont_title']/text()"],
    "xpath_content": ["//*[@id='the_content']/p/text()"]}
    """

    generate_spider(test_code)
    generate_spider_init(test_code)
