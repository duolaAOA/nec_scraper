# -*-coding:utf-8 -*-
"""
xpath or css   解析
"""
# huxiu
CHANNELHREFS_X =  '//div[@class="container"]/ul[contains(@class,"navbar-left")]/li[contains(@class,"js-show-menu")]/ul/li/a/@href'
TOPARTICLESHREFS_X = '//div[@class="container"]/div[contains(@class,"wrap-left")]/div[@class="mod-info-flow"]/div[contains(@class,"mod-art")]/div[contains(@class,"mob-ctt")]/h2/a[contains(@class,"transition")]/@href'

HUXIU_TITLE = "//div[@class='article-wrap']/h1[@class='t-h1']/text()"
HUXIU_CONTENT = "//div[@class='article-content-wrap']//p/text()"
