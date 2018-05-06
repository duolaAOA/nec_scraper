#  -*- coding: utf-8 -*-
import re
import json

import requests
import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from nec_scraper.scrapy_redis.spiders import RedisCrawlSpider

from nec_scraper import lxml_select as ls
from nec_scraper.items import ECommerceGoodItem, ECommerceGoodCommentItem
from nec_scraper.items import ECommerceShopItem, ECommerceShopCommentItem


class AmazonSpider(RedisCrawlSpider):

    name = 'amazon'
    redis_key = 'amazon:start_urls'
    allowed_domains = ['amazon.cn']

    rules = {
        Rule(LinkExtractor(allow=('.*//www.amazon.cn/gp/product/.*',
                                  '.*//www.amazon.cn/dp/.*', '.*//www.amazon.cn/.*/dp.*'), deny=()),
             callback='parse_good',
             follow=True),
        Rule(LinkExtractor(allow='.*//www.amazon.cn/gp/aag/main?.*', deny=()),
             callback='parse_shop',
             follow=True),
    }

    # 电商Id
    eCommerceId = 2

    def parse_good(self, response):
        """"
        获取商品信息
        :returns      good_item   商品信息
                       good_comment_item         商品评论

        """
        good_id = ''
        try:
            if 'gp/product' in response.url:
                id_pattern = re.compile(r'product/\d|\w{10}')
                good_id = id_pattern.findall(response.url)[0]
                good_id = str(good_id).strip('product').strip('/')
            elif 'dp' in response.url:
                id_pattern = re.compile(r'dp/\d|\w{10}')
                good_id = id_pattern.findall(response.url)[0]
                good_id = str(good_id).strip('dp').strip('/')
        except:
            print('无效的商品页')

        good_item = ECommerceGoodItem()
        good_item['eCommerceId'] = self.eCommerceId
        good_item['goodId'] = good_id

        try:
            shop_name = response.xpath(ls.AMAZON_SHOP_NAME).extract_first("")
            shop_url = 'https://www.amazon.cn' + response.xpath(ls.AMAZON_SHOP_URL).extract_first("")
            shop_id = re.search(r'seller=\d|\w{13,14}&', shop_url).group(0).strip('&')
            good_item['shopId'] = shop_id
            # 直接发一个获取店家信息的Request
            yield scrapy.Request(url=shop_url, callback=self.parse_shop,
                                 meta={'shopName': shop_name, 'shopUrl': shop_url, 'shopId': shop_id})
        except:
            good_item['shopId'] = "自营"
        good_name = response.xpath(ls.AMAZON_GOOD_NAME).extract_first("").strip()
        good_item['goodName'] = good_name
        good_item['goodUrl'] = response.url
        try:
            price = response.xpath(ls.AMAZON_GOOD_PRICE).extract_first("")
            if price is not '':
                good_item['goodPrice'] = price
            elif price is '':
                good_item['goodPrice'] = '无货'
        except:
            good_item['goodPrice'] = '无货'
            
        yield good_item

        """
        good_comment_item       商品评论信息
        """
        good_comment_item = ECommerceGoodCommentItem()
        good_comment_item['eCommerceId'] = self.eCommerceId
        good_comment_item['goodId'] = good_id
        try:
            good_comment_url = response.xpath(ls.AMAZON_GOOD_COMMENT_URL).extract()[0]
            good_comment_star = ''.join(response.xpath(ls.AMAZON_GOOD_COMMENT).extract())
            good_comment_item['goodCommentsUrl'] = good_comment_url
            good_comment_item['goodCommentsData'] = good_comment_star
            good_comment_item['goodCommentCounts'] = response.xpath(ls.AMAZON_GOOD_COMMENT_START).extract()[0]
        except:
            good_comment_item['goodCommentsUrl'] = '无评论链接'
            good_comment_item['goodCommentsData'] = '无评论数据'
            good_comment_item['goodCommentCounts'] = 0
            
        yield good_comment_item

    def parse_shop(self, response):
        """
        获取商家信息
        :param response: 
        :return:        shop_item   商铺信息
                         shop_comment_item      商店评论信息
        """
        print("获取店家信息")
        shop_item = ECommerceShopItem()
        shop_item['eCommerceId'] = self.eCommerceId
        shop_item['shopId'] = response.meta['shopId']
        shop_item['shopName'] = response.meta['shopName']
        shop_item['shopUrl'] = response.meta['shopUrl']
        yield shop_item

        shop_comment_item = ECommerceShopCommentItem()
        shop_comment_item['eCommerceId'] = self.eCommerceId
        shop_comment_item['shopId'] = response.meta['shopId']
        shop_comment_item['shopCommentsUrl'] = response.url
        shop_comment_item['shopCommentsData'] = ''.join(response.xpath(ls.AMAZON_SHOP_COMMENT).extract())
        yield shop_comment_item


