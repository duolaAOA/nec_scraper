# -*- coding: utf-8 -*-

import pymongo
from nec_scraper import settings

from nec_scraper.items import ArticleItem, DomTreeItem


class MongoPipeline(object):
    """
    Mongodb Pipeline
    """
    # 集合名
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
            self.db[self.hp_collection_name + '_' + 'ArticleItem'].insert(dict(item))       # 存入数据库原始数据

        if isinstance(item, DomTreeItem):
            self.hp_collection_name = settings.MONGO_COLLECTION_NAME
            self.db[self.hp_collection_name + '_' + "DomTreeItem"].insert(dict(item))  # 存入数据库原始数据

        return item
