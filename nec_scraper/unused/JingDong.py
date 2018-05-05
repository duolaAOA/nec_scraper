# -*-coding:utf-8 -*-

import re
import json

import requests
from scrapy.spider import Rule
from scrapy.linkextractors import LinkExtractor
from nec_scraper.scrapy_redis.spiders import RedisCrawlSpider

from nec_scraper import lxml_select as ls
from nec_scraper.items import ECommerceGoodItem, ECommerceGoodCommentItem
from nec_scraper.items import ECommerceShopItem, ECommerceShopCommentItem


class JdSpider(RedisCrawlSpider):

    name = 'jd'
    redis_key = 'jd:start_urls'
    allowed_domains = ['jd.com']

    rules = {
        Rule(
            LinkExtractor(allow='https://item.jd.com/\d+.html', deny=()),
            callback='parse_good_shop',
            follow=True),
    }

    # 电商ID
    eCommerceId = 1

    def parse_good_shop(self, response):
        """
        商品与其商铺相关数据解析
        :param response: 
        :return:
        good_item           商品信息
        comment_item        商品评论
        shop_item           商铺信息
        comment_shopI_item  商铺评价信息
        """
        try:
            item_id = re.search(r'\d+', response.url).group(0)
        except:
            print("无效的商品页")
        else:
            """
            商品信息
            :return  good_item
            """
            good_item = ECommerceGoodItem()
            good_item['eCommerceId'] = self.eCommerceId
            good_item['goodId'] = item_id

            try:
                shop_comment_url = response.xpath(
                    ls.JINGDONG_COMMENT_URL).extract()[0]
                shop_id = re.search(r'\d+', shop_comment_url).group(0)
                good_item['shopId'] = shop_id
            except:
                # 自营店无法获取店铺ID
                good_item['shopId'] = 0
            good_item['goodName'] = ''.join(
                response.xpath(ls.JINGDONG_GOOD_NAME).extract()).strip()
            good_item['goodUrl'] = response.url

            try:
                price_response = requests.get(
                    url='http://p.3.cn/prices/mgets?skuIds=J_' + str(item_id)
                ).text
                data = json.loads(price_response)[0]
                item_price = data['p']
                good_item['goodPrice'] = item_price
            except:
                good_item['goodPrice'] = -404

            yield good_item

            """
            商品评论信息
            :return   comment_item
            """
            comment_item = ECommerceGoodCommentItem()
            comment_item['eCommerceId'] = self.eCommerceId
            comment_item['goodId'] = item_id
            comment_dict = {
                'productId': str(item_id),
                'score': '0',
                'sortType': '5',
                'page': '0',
                'pageSize': '10',
                'isShadowSku': '0'
            }
            query_comments_data_url = ls.JINGDONG_QUERY_COMMENTS_DATA_URL.format(comment_dict['productId'],
                                                                                 comment_dict['score'],
                                                                                 comment_dict['sortType'],
                                                                                 comment_dict['page'],
                                                                                 comment_dict['pageSize'],
                                                                                 comment_dict['isShadowSku'])
            comment_item['goodCommentsUrl'] = query_comments_data_url
            content = json.loads(
                requests.get(query_comments_data_url).content.decode(
                    'gbk', 'ignore').encode('utf-8'))
            comments_data = content['productCommentSummary']
            comment_item['goodCommentsData'] = str(comments_data)
            yield comment_item

        """
        店铺相关数据解析
        :param response: 
        :return:  Shop   msg
        """
        shop_url = "https:" + response.xpath(ls.JINGDONG_SHOP_URL).extract_first("")
        shop_id = re.search(r'\d+', shop_url).group(0)

        """
        店铺信息
        :return  shop_item
        """
        shop_item = ECommerceShopItem()
        shop_item['eCommerceId'] = self.eCommerceId
        shop_item['shopId'] = shop_id
        shop_item['shopName'] = ''.join(response.xpath(ls.JINGDONG_SHOP_NAME).extract()).strip()
        shop_item['shopUrl'] = shop_url

        yield shop_item

        """
        店铺评价信息
        :return  comment_shopI_item
        """
        comment_shop_item = ECommerceShopCommentItem()
        comment_shop_item['eCommerceId'] = self.eCommerceId
        comment_shop_item['shopId'] = shop_id
        comment_shop_item['shopCommentsUrl'] = shop_url
        comment_data = dict()
        comment_data['shopTotalRating'] = response.xpath(ls.JINGDONG_TOTAL_RATING).extract_first("")

        total_score = response.xpath('''//*[@class='score-parts']//span[@class='score-detail']/em/text()''')
        comment_data["good_Rating"] = total_score[0]
        comment_data["service_Rating"] = total_score[1]
        comment_data["logistics_Rating"] = total_score[2]
        comment_shop_item['shopCommentsData'] = str(comment_data)

        yield comment_shop_item

