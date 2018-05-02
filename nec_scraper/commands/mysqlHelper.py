# -*-coding:utf-8 -*-

import pymysql
import nec_scraper.settings as prime_settings


class MysqlHelper(object):
    """
    Mysql 操作配置
    """

    def __init__(self):
        self.host = prime_settings.MYSQL_HOST
        self.port = prime_settings.MYSQL_PORT
        self.user = prime_settings.MYSQL_USER
        self.passwd = prime_settings.MYSQL_PASSWD
        self.db = prime_settings.MYSQL_DBNAME

    def connect_mysql(self):
        """连接"""
        conn = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            passwd=self.passwd,
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor)
        return conn

    def connect_database(self):
        """连接"""
        conn = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            passwd=self.passwd,
            db=self.db,
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor)
        return conn

    def create_database(self):
        """数据库创建"""
        conn = self.connect_mysql()
        # 注意sql语句exists右边存在一个空格!!!
        create_sql = '''create database if not exists ''' + self.db
        cur = conn.cursor()
        cur.execute(create_sql)
        cur.close()
        conn.close()

    def create_table(self, sql):
        """数据表创建"""
        conn = self.connect_database()
        cur = conn.cursor()
        cur.execute(sql)
        cur.close()
        conn.close()

    def insert(self, sql, *args):
        conn = self.connect_database()
        print(sql)
        print(args)

        cur = conn.cursor()
        try:
            cur.execute(sql, args)
        except:
            conn.rollback()
        else:
            conn.commit()
            cur.close()
            conn.close()

    def update(self, sql, *args):
        conn = self.connect_database()
        cur = conn.cursor()
        try:
            cur.execute(sql, args)
        except:
            conn.rollback()
        else:
            conn.commit()
            cur.close()
            conn.close()

    def delete(self, sql, *args):
        conn = self.connect_database()
        cur = conn.cursor()
        cur.execute(sql, args)
        conn.commit()
        cur.close()
        conn.close()


# 用于创建电商相关的表
# 划分为5条语句执行， 如果放在一个变量中执行
# 在命令行中sql执行没问题， 但程序执行就出问题， 所以改为多条语句

create_sql_0 = '''CREATE TABLE `ecommerce` (
        `eCommerceId` int(11) NOT NULL COMMENT '电商网站Id',
        `eCommerceName` varchar(48) COLLATE utf8_bin DEFAULT NULL COMMENT '电商网站名字',
        `eCommerceUrl` varchar(200) COLLATE utf8_bin DEFAULT NULL COMMENT '电商网站home页url',
        PRIMARY KEY (`eCommerceId`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;'''

create_sql_1 = '''CREATE TABLE `ecommerceshop` (
      `eCommerceId` int(11) NOT NULL COMMENT '电商网址id',
      `shopId` bigint(20) NOT NULL COMMENT '店铺id',
      `shopName` varchar(48) COLLATE utf8_bin DEFAULT NULL COMMENT '店名',
      `shopUrl` varchar(200) COLLATE utf8_bin DEFAULT NULL COMMENT '店铺url链接',
      `shopLocation` varchar(72) COLLATE utf8_bin DEFAULT NULL COMMENT '店铺地址',
      `shopPhoneNumber` varchar(50) COLLATE utf8_bin DEFAULT NULL COMMENT '店家电话',
      PRIMARY KEY (`shopId`,`eCommerceId`),
      KEY `eCommerceId` (`eCommerceId`),
      CONSTRAINT `ecommerceshop_ibfk_1` FOREIGN KEY (`eCommerceId`) REFERENCES `ecommerce` (`eCommerceId`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;'''

create_sql_2 = '''CREATE TABLE `ecommerceshopcomment` (
      `eCommerceId` int(11) NOT NULL COMMENT '电商网站Id',
      `shopId` bigint(20) NOT NULL COMMENT '店家id',
      `shopCommentsUrl` varchar(200) COLLATE utf8_bin DEFAULT NULL COMMENT '店家评论页的链接',
      `shopCommentsData` varchar(400) COLLATE utf8_bin DEFAULT NULL COMMENT '店家评论数据',
      PRIMARY KEY (`shopId`,`eCommerceId`),
      KEY `eCommerceId` (`eCommerceId`),
      CONSTRAINT `ecommerceshopcomment_ibfk_1` FOREIGN KEY (`eCommerceId`) REFERENCES `ecommerce` (`eCommerceId`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;'''

create_sql_3 = '''CREATE TABLE `ecommercegood` (
      `eCommerceId` int(11) NOT NULL COMMENT '电商网站Id',
      `goodId` bigint(20) NOT NULL COMMENT '商品id',
      `shopId` bigint(20) DEFAULT NULL COMMENT '店家id',
      `goodName` varchar(400) COLLATE utf8_bin DEFAULT NULL COMMENT '商品名字',
      `goodUrl` varchar(200) COLLATE utf8_bin DEFAULT NULL COMMENT '商品链接',
      `goodPrice` decimal(10,0) DEFAULT NULL COMMENT '商品价格',
      PRIMARY KEY (`goodId`,`eCommerceId`),
      KEY `eCommerceId` (`eCommerceId`),
      CONSTRAINT `ecommercegood_ibfk_1` FOREIGN KEY (`eCommerceId`) REFERENCES `ecommerce` (`eCommerceId`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;'''

create_sql_4 = '''CREATE TABLE `ecommercegoodcomment` (
      `eCommerceId` int(11) NOT NULL COMMENT '电商网站Id',
      `goodId` bigint(20) NOT NULL COMMENT '商品的id',
      `goodCommentsUrl` varchar(200) COLLATE utf8_bin DEFAULT NULL COMMENT '商品评论页的链接',
      `goodCommentsData` varchar(1600) COLLATE utf8_bin DEFAULT NULL COMMENT '商品评论数据',
      PRIMARY KEY (`goodId`,`eCommerceId`),
      KEY `eCommerceId` (`eCommerceId`),
      CONSTRAINT `ecommercegoodcomment_ibfk_1` FOREIGN KEY (`eCommerceId`) REFERENCES `ecommerce` (`eCommerceId`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;'''


sql_create_table = [create_sql_0, create_sql_1, create_sql_2, create_sql_3, create_sql_4]