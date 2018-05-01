# -*- coding: utf-8 -*-

# Scrapy settings for nec_scraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'nec_scraper'

SPIDER_MODULES = ['nec_scraper.spiders']
NEWSPIDER_MODULE = 'nec_scraper.spiders'




# Obey robots.txt rules
ROBOTSTXT_OBEY = False



# 配置
COOKIES_ENABLED = False  # 禁止COOKIES
RETRY_ENABLED = False   # 禁止重试
DOWNLOAD_TIMEOUT = 15   # 超时时限
DOWNLOAD_DELAY = 0.5   # 间隔时间
# DEPTH_LIMIT = 20 #爬取深度, 避免那些动态生成链接的网站造成的死循环

# Redis 配置
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

# Mongodb 配置
MONGO_URI = 'mongodb://localhost:27017'
MONGO_DB = 'nec_scraper'
MONGO_COLLECTION_NAME = "date"


# 随user-agent头
DOWNLOADER_MIDDLEWARES = {
   'nec_scraper.rotateUserAgentMiddleware.RotateUserAgentMiddleware': 399,
}

ITEM_PIPELINES = {
    'nec_scraper.pipelines.MongoPipeline': 1,
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
from datetime import datetime
t = datetime.strftime(datetime.now(), "%Y-%m-%d-%H-%M")
LOG_FILE = "./log/news-{}.log".format(t)
LOG_LEVEL = "DEBUG"


# 虎嗅网(huxiu)
huxiu_base_url = "https://www.huxiu.com"
huxiu_start_urls = "huxiu:start_urls"
huxiu_dupefilter = "huxiu:dupefilter"
huxiu_requests = "huxiu:requests"

# huaerjie——华尔街
huaerjie_base_url = "https://wallstreetcn.com"
huaerjie_start_urls = "huaerjie:start_urls"
huaerjie_dupefilter = "huaerjie:dupefilter"
huaerjie_requests = "huaerjie:requests"

# caijing——财经
caijing_base_url = "http://www.caijing.com.cn"
caijing_start_urls = "caijing:start_urls"
caijing_dupefilter = "caijing:dupefilter"
caijing_requests = "caijing:requests"

# fenghuang——凤凰网
fenghuang_base_url = "http://news.ifeng.com/"
fenghuang_start_urls = "fenghuang:start_urls"
fenghuang_dupefilter = "fenghuang:dupefilter"
fenghuang_requests = "fenghuang:requests"

# souhu——搜狐网
souhu_base_url = "http://news.sohu.com"
souhu_start_urls = "souhu:start_urls"
souhu_dupefilter = "souhu:dupefilter"
souhu_requests = "souhu:requests"

# wangyi——网易新闻
wangyi_base_url = "http://news.163.com/"
wangyi_start_urls = "wangyi:start_urls"
wangyi_dupefilter = "wangyi:dupefilter"
wangyi_requests = "wangyi:requests"
