# -*-coding:utf-8 -*-

import os
import codecs
import random
import logging
from urllib.parse import urlunparse
from urllib.request import _parse_proxy

from twisted.internet import defer
from twisted.internet.error import TimeoutError, DNSLookupError, \
        ConnectionRefusedError, ConnectionDone, ConnectError, \
        ConnectionLost, TCPTimedOutError
from scrapy.exceptions import NotConfigured
from twisted.web.client import ResponseFailed
from scrapy.utils.response import response_status_message

logger = logging.getLogger(__name__)


class RandomProxyMiddleware(object):
    def __init__(self, settings):
        if not settings.getint('RETRY_TIMES'):
            self.max_retry_times = 4
        else:
            self.max_retry_times = settings.getint('RETRY_TIMES')
        if not settings.getint('PROXY_USED_TIMES'):
            self.max_proxy_chance = self.max_retry_times / 2
        else:
            self.max_proxy_chance = settings.getint('PROXY_USED_TIMES')
        self.retry_http_codes = set(int(x) for x in settings.getlist('RETRY_HTTP_CODES'))
        # 优先级调整
        if not settings.getint('RETRY_PRIORITY_ADJUST'):
            self.priority_adjust = -1
        else:
            self.priority_adjust = settings.getint('RETRY_PRIORITY_ADJUST')

        # 加载proxy文件
        self.proxy_dict = {}
        if not settings.get('HTTPPROXY_FILE_PATH'):
            raise NotConfigured
        file_path = settings.get('HTTPPROXY_FILE_PATH')
        if os.path.exists(file_path):
            self.proxy_dict = self._load_data(file_path)
        else:
            raise ValueError

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def _load_data(self, path):
        """
        加载proxy数据
        :param path:
        :return: proxy_dict
        """
        proxy_dict = {}
        with codecs.open(path, 'r', encoding="utf8") as f:
            for url in f:
                if url:
                    proxy_dict[url] = {"status": "valid", "chance": self.max_proxy_chance}
        return proxy_dict

    def _del_invaild_proxy(self, request):
        """
        失败后减少proxy使用几率chance, 当chance为0 时删除无效proxy
        :param request:
        :return:
        """
        failed_proxies = request.meta.get('failed_proxies', list())
        if failed_proxies:
            for proxy in failed_proxies:
                self.proxy_dict[proxy]["chance"] = self.proxy_dict[proxy]["chance"] - 1
                if self.proxy_dict[proxy]["chance"] <= 0:
                    del self.proxy_dict[proxy]

    def _choose_proxy(self, request):
        """
        1. 有较小几率不使用代理
        2. 对代理随即选取
        :param request:
        :return: request
        """
        if random.random() < 0.95:
            request.meta["proxy"] = random.choice(self.proxy_dict.keys())
        return request

    def _set_proxy(self, request, proxy_url):
        creds, proxy = self._get_proxy(proxy_url)
        request.meta.get["proxy"] = proxy
        if creds:
            request.headers["Proxy-Authorization"] = b'Basic' + creds

    @staticmethod
    def _get_proxy(url):
        proxy_type, user, password, hostport = _parse_proxy(url)
        proxy_url = urlunparse((proxy_type or "http", hostport, '', '', '', ''))
        creds = None

        return creds, proxy_url

    def _retry(self, request, reason, spider):
        # 重试方法：
        # 1）当连接小于特定次数时重抓，
        # 2) 当reason为500，抓取
        retries = request.meta.get('retry_times', 0) + 1
        if retries <= self.max_retry_times:
            logger.debug("Retrying %(request)s (failed %(retries)d times): %(reason)s",
                         {'request': request, 'retries': retries, 'reason': reason},
                         extra={'spider': spider})
            retryreq = request.copy()
            retryreq.meta['retry_times'] = retries
            if request.meta['proxy']:
                retryreq.meta['failed_proxies'] = request.meta['proxy']
            retryreq.dont_filter = True
            retryreq.priority = request.priority + self.priority_adjust
            return retryreq
        else:
            logger.debug("Gave up retrying %(request)s (failed %(retries)d times): %(reason)s",
                         {'request': request, 'retries': retries, 'reason': reason},
                         extra={'spider': spider})

    def process_request(self, request, spider):
        # 为requests设置proxy
        request = self._choose_proxy(request)
        if "proxy" in request.meta:
            self._set_proxy(request, request.meta['proxy'])

    def process_response(self, request, response, spider):
        # 对特定的http返回码进行重新抓取,主要针对500和599等
        if "proxy" in request.meta:
            logger.debug("Use proxy: " + request.meta["proxy"] + "to crawler")
        if request.meta.get('dont_retry', False):
            return response
        if response.status in self.retry_http_codes:
            reason = response_status_message(response.status)
            self._del_invaild_proxy(request)
            return self._retry(request, reason, spider) or response
        return response

    def process_exception(self, request, exception, spider):
        # 遇到错误尝试重试
        EXCEPTIONS_TO_RETRY = (defer.TimeoutError, TimeoutError, DNSLookupError, ConnectionRefusedError, ConnectionDone,
        ConnectError, ConnectionLost, TCPTimedOutError, ResponseFailed, IOError)
        if isinstance(exception, EXCEPTIONS_TO_RETRY) \
                and not request.meta.get('dont_retry', False):
            return self._retry(request, exception, spider)
