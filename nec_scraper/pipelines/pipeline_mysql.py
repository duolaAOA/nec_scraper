# -*-coding:utf-8 -*-

import pymysql
from twisted.enterprise import adbapi

from nec_scraper.items import ECommerce
from nec_scraper.items import ECommerceShopItem
from nec_scraper.items import ECommerceShopCommentItem
from nec_scraper.items import ECommerceGoodItem
from nec_scraper.items import ECommerceGoodCommentItem


class MysqlPipeline(object):
    """mysql Pipeline"""

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        # 传入settings参数
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWD"],
            port=settings["MYSQL_PORT"],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True)
        dbpool = adbapi.ConnectionPool("pymysql", **dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        if isinstance(item, ECommerce):
            query = self.dbpool.runInteraction(
                self._conditional_insert_ecommerce, item)  # item插入
            query.addErrback(self._handle_error, item, spider)  # 异常捕获

        if isinstance(item, ECommerceShopItem):
            query = self.dbpool.runInteraction(
                self._conditional_insert_ecommerceshop, item)
            query.addErrback(self._handle_error, item, spider)

        if isinstance(item, ECommerceShopCommentItem):
            query = self.dbpool.runInteraction(
                self._conditional_insert_ecommerceshopcomment, item)
            query.addErrback(self._handle_error, item, spider)

        if isinstance(item, ECommerceGoodItem):
            query = self.dbpool.runInteraction(
                self._conditional_insert_ecommercegood, item)
            query.addErrback(self._handle_error, item, spider)

        if isinstance(item, ECommerceGoodCommentItem):
            query = self.dbpool.runInteraction(
                self._conditional_insert_ecommercegoodcomment, item)
            query.addErrback(self._handle_error, item, spider)

        return item

    def _conditional_insert_ecommerce(self, cursor, item):
        """
        :param cursor:  mysql 操作游标
        :param item:    item数据字段: 3
        :return:
        """
        insert_sql = '''INSERT INTO ECommerce(eCommerceId, eCommerceName, eCommerceUrl) 
                        VALUES(%s, %s, %s)'''

        params = (item["eCommerceId"], item["eCommerceName"],
                  item["eCommerceUrl"])
        cursor.execute(insert_sql, params)

    def _conditional_insert_ecommerceshop(self, cursor, item):
        """
        :param cursor:  mysql 操作游标
        :param item:    item数据字段: 6
        :return:
        """
        insert_sql = '''INSERT INTO ECommerceShop(eCommerceId, shopId, shopName, shopUrl, 
                                    shopLocation, shopPhoneNumber) 
                        VALUES(%s, %s, %s, %s, %s, %s)'''

        params = (item["eCommerceId"], item["eCommerceName"],
                  item["eCommerceUrl"])
        cursor.execute(insert_sql, params)

    def _conditional_insert_ecommerceshopcomment(self, cursor, item):
        """
        :param cursor:  mysql 操作游标
        :param item:    item数据字段: 14
        :return:
        """
        insert_sql = '''INSERT INTO ECommerceShopComment(eCommerceId, shopId, shopCommentsUrl, shopCommentsData)
                        VALUES(%s, %s, %s,%s)'''
        params = (item["eCommerceId"], item["shopId"], item["shopCommentsUrl"],
                  item["shopCommentsData"])
        cursor.execute(insert_sql, params)

    def _conditional_insert_ecommercegood(self, cursor, item):
        """
        :param cursor:  mysql 操作游标
        :param item:    item数据字段: 5
        :return:
        """
        insert_sql = '''INSERT INTO ECommerceGood(eCommerceId, goodId, shopId, goodName, goodUrl, goodPrice) 
                        VALUES(%s, %s, %s, %s, %s, %s)'''

        params = (item["eCommerceId"], item["goodId"], item["shopId"],
                  item["goodName"], item["goodUrl"], item["goodPrice"])
        cursor.execute(insert_sql, params)

    def _conditional_insert_ecommercegoodcomment(self, cursor, item):
        """
        :param cursor:  mysql 操作游标
        :param item:    item数据字段: 8
        :return:
        """
        insert_sql = '''INSERT INTO ECommerceGoodComment(eCommerceId, goodId, goodCommentsUrl, 
                                      goodCommentsData, goodCommentCounts) 
                        VALUES(%s, %s, %s, %s, %s)'''

        params = (item["eCommerceId"], item["goodId"], item["goodCommentsUrl"],
                  item["goodCommentsData"], item["goodCommentCounts"])
        cursor.execute(insert_sql, params)

    def _handle_error(self, failure, item, spider):
        """异常处理"""
        print(failure)
