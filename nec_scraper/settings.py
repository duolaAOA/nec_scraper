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


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'nec_scraper (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'nec_scraper.middlewares.NecScraperSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'nec_scraper.rotateUserAgentMiddleware.RotateUserAgentMiddleware': 399,
# }

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}


# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

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
LOG_FILE = "./log/huxiu-{}.log".format(t)
LOG_LEVEL = "DEBUG"


# 虎嗅网(huxiu)  www.huxiu.com
huxiu_base_url = "https://www.huxiu.com"
huxiu_start_urls = "huxiu:start_urls"
huxiu_dupefilter = "huxiu:dupefilter"
huxiu_requests = "huxiu:requests"
