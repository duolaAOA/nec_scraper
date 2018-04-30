# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from nec_scraper import settings

from .items import ArticleItem

# class ArticlePipeline(object):
#     def __init__(self):
#         self.client = pymongo.MongoClient(settings.MONGO_URI)
#         self.db = self.client["huxiu"]
#         self.collection = self.db[settings.MONGO_COLLECTION_NAME]
#
#     def open_spider(self, spider):
#         pass
#
#     def close_spider(self, spider):
#         self.client.close()
#
#     def process_item(self, item, spider):
#         articleDict = {
#                        'id': item['articleId'],
#                        'content': item['content']
#                        }
#         try:
#             self.collection['v'].insert(articleDict)
#         except:
#             self.collection['article'].save(articleDict)


class MongoPipeline(object):
    """
    Mongodb Pipeline
    """
    # 集合名 使用之前会赋值
    hp_collection_name = ''

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB', 'items'))

    def open_spider(self, spider):
        """数据库连接"""
        self.client = pymongo.MongoClient(self.mongo_uri)

        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        """数据库连接关闭"""
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, ArticleItem):
            self.hp_collection_name = settings.MONGO_COLLECTION_NAME
            self.db[self.hp_collection_name].insert(dict(item))       # 存入数据库原始数据
        return item
