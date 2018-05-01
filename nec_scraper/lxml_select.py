# -*-coding:utf-8 -*-
"""
xpath or css   解析
"""
# Huxiu
CHANNELHREFS_X =  '//div[@class="container"]/ul[contains(@class,"navbar-left")]/li[contains(@class,"js-show-menu")]/ul/li/a/@href'
TOPARTICLESHREFS_X = '//div[@class="container"]/div[contains(@class,"wrap-left")]/div[@class="mod-info-flow"]/div[contains(@class,"mod-art")]/div[contains(@class,"mob-ctt")]/h2/a[contains(@class,"transition")]/@href'

HUXIU_TITLE = "//div[@class='article-wrap']/h1[@class='t-h1']/text()"
HUXIU_CONTENT = "//div[@class='article-content-wrap']//p/text()"


# CaiJing
CAIJING_TITLE = "//*[@id='cont_title']/text()"
CAIJING_CONTENT = "//*[@id='the_content']/p/text()"


# FengHuang
FENGHUANG_TITLE = "//*[@id='artical_topic']/text()"
FENGHUANG_CONTENT = "//*[@id='main_content']/p/text()"


# souhu
SOUHU_TITLE = "//*[@class='text-title']/h1/text()"
SOUHU_CONTENT = "//*[@id='mp-editor']/p/text()"

# wangyi
WANGYI_TITLE = "//*[@id='epContentLeft']/h1/text() | //*[@id='zajia_wrap']/div[2]/div[2]/div[@class='brief']/h1/text()"
WANGYI_CONTENT = "//*[@id='endText']/p/text()"


# huaerjie
HUAERJIE_TITLE = '//*[@id="app"]/div/main/div/div[@class="article main-article"]/div/div[@class="article__heading__title"]/text()'
HUAERJIE_CONTENT = "//*[@class='summary']/text() | //div[@class='node-article-content']//p/text()"
