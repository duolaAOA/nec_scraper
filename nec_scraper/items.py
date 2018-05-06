# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


# DOM树item
class DomTreeItem(Item):
    # 文章的url
    url = Field()
    # 文章的html
    html = Field()

# 文章item
class ArticleItem(Item):
    # 文章标题
    articleTitle = Field()
    # 文章url
    articleUrl = Field()
    # 文章内容
    articleContent = Field()
    # 文章关键词
    articleFirstTag = Field()
    articleSecondTag = Field()
    articleThirdTag = Field()


# 电商详情item
class ECommerce(Field):
    # 电商网站Id
    eCommerceId = Field()
    # 电商网站名字
    eCommerceName = Field()
    # 电商网站home页url
    eCommerceHomeUrl = Field()


# 店铺详情item
class ECommerceShopItem(Field):
    # 电商网址id
    ecommerceId = Field()
    # 店铺id
    shopId = Field()
    # 店名
    shopName = Field()
    # 店铺url链接
    shopUrl = Field()


# 电商网店店铺评论item
class ECommerceShopCommentItem(Field):
    # 电商网站Id
    eCommerceId = Field()
    # 店家id
    shopId = Field()
    # 店家评论页的链接
    shopCommentsUrl = Field()
    # 店家评论数据
    shopCommentsData = Field()


# 商品item
class ECommerceGoodItem(Item):
    # 电商网站Id
    eCommerceId = Field()
    # 商品id
    goodId = Field()
    # 店家id
    shopId = Field()
    # 商品名字
    goodName = Field()
    # 商品链接
    goodUrl = Field()
    # 商品价格
    goodPrice = Field()


# 商品评论item
class ECommerceGoodCommentItem(Item):
    # 电商网站Id
    eCommerceId = Field()
    # 商品的id
    goodId = Field()
    # 商品评论页的链接
    goodCommentsUrl = Field()
    # 商品评论数据
    goodCommentsData = Field()
    # 商品评论数量
    goodCommentCounts = Field()
