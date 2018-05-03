# -*- coding: utf-8 -*-

import os
from datetime import datetime
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

BOT_NAME = 'nec_scraper'

SPIDER_MODULES = ['nec_scraper.spiders']
NEWSPIDER_MODULE = 'nec_scraper.spiders'

ROBOTSTXT_OBEY = False

# 代理文件路径
HTTPPROXY_FILE_PATH = os.path.abspath(os.path.join(BASE_DIR, "proxy/valid_proxy.txt"))


# 配置
COOKIES_ENABLED = False  # 禁止COOKIES
RETRY_ENABLED = False   # 禁止重试
DOWNLOAD_TIMEOUT = 15   # 超时时限
DOWNLOAD_DELAY = 0.5   # 间隔时间

RETRY_HTTP_CODES = [500, 503, 504, 599, 403]    # 重试状态码
RETRY_TIMES = 5  # 请求连接失败重试次数
PROXY_USED_TIMES = 2    # proxy 失败重试次数
# DEPTH_LIMIT = 20 #爬取深度, 避免那些动态生成链接的网站造成的死循环

# Redis 数据库配置
REDIS_RATELIMIT_DB_URL = "redis://localhost:6379/0"
# redis —— url存储
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIE_URL = None
# redis —— 去重队列
FILTER_URL = None
FILTER_HOST = '127.0.0.1'
FILTER_PORT = 6379
FILTER_DB = 0
# 用于监控的数据库
FLASK_DB = 0

# 存储爬虫运行数据的四个队列,需要与monitor.monitor_settings中的一致
# https://github.com/ioiogoo/scrapy-monitor
request_count = 'downloader/request_count'
response_count = 'downloader/response_count'
response_status200_count = 'downloader/response_status_count/200'
item_scraped_count = 'item_scraped_count'
STATS_KEYS = ["downloader/request_count", "downloader/response_count", "downloader/response_status_count/200", "item_scraped_count"]


# Mongodb 数据库配置
MONGO_URI = 'mongodb://localhost:27017'
MONGO_DB = 'nec_scraper'
MONGO_COLLECTION_NAME = "date"

# Mysql 数据库配置
MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = 3306
MYSQL_DBNAME = 'nec_scraper'    # 数据库名
MYSQL_USER = 'root'             # 用户名
MYSQL_PASSWD = '1219960386'     # 密码

# Monitor setting 监控配置
MONITOR_HOST = '127.0.0.1'
MONITOR_PORT = '5050'

# scrapy.downloadermiddlewares.retry.RetryMiddleware 会造成程序陷入循环等待
DOWNLOADER_MIDDLEWARES = {
   'nec_scraper.middlewares.middleware_rotateUserAgent.RotateUserAgentMiddleware': 400,
   'nec_scraper.middlewares.middleware_monitor.StatcollectorMiddleware': 401,
}

ITEM_PIPELINES = {
    'nec_scraper.pipelines.pipeline_mongo.MongoPipeline': 300,
    'nec_scraper.pipelines.pipeline_mysql.MysqlPipeline': 301,
    'nec_scraper.pipelines.pipeline_monitor.SpiderRunStatspipeline': 302,  # 可视化配置
}

# 调度模块
SCHEDULER = 'scrapy_redis.scheduler.Scheduler'
SCHEDULER_PERSIST = True
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderQueue'
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

# 没有这个会出现异常
DOWNLOAD_HANDLERS = {'s3': None, }

# 自定义命令
COMMANDS_MODULE = 'nec_scraper.commands'

# 日志
t = datetime.strftime(datetime.now(), "%Y-%m-%d-%H-%M")
LOG_FILE = "./log/news-{}.log".format(t)
LOG_LEVEL = "DEBUG"



