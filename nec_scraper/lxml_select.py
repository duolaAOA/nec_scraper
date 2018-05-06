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


"""
电商平台解析
"""
# 'https://mall.jd.com/shopLevel-\d+.html'  京东店铺详情入口， 但每一次的请求都会产生验证码
# 所以只能放弃， 选择从另外的接口获取的字段要少一点
# jingdong
JINGDONG_COMMENT_URL = '//*[@id="popbox"]/div/div[@class="mc"]/div/div/a[1]/@href'
JINGDONG_GOOD_NAME = '''//div[@class='itemInfo-wrap']/div[@class='sku-name']/text()'''
JINGDONG_QUERY_COMMENTS_DATA_URL = 'https://sclub.jd.com/comment/productPageComments.action?&productId={}&score=0&sortType=5&page={}&pageSize={}&isShadowSku={}'
JINGDONG_SHOP_URL = '''//div[@class='shop-logo-box']/a/@href'''
JINGDONG_SHOP_NAME = '''//*[@id='crumb-wrap']//div[@class='name']/a/@title'''
JINGDONG_TOTAL_RATING = '''//*[@class='score-sum']/span/text()'''
JINGDONG_TOTAL_SCORE = '''//*[@class='score-parts']//span[@class='score-detail']/em/text()'''


# amazon  亚马逊
AMAZON_SHOP_NAME = '''//*[@id='ddmMerchantMessage']/text() | //*[@id='ddmMerchantMessage']/b/text() | //*[@id='ddmMerchantMessage']/a/text()'''
AMAZON_SHOP_URL = '''//*[@id='ddmMerchantMessage']/a/@href'''
# 自营
AMAZON_GOOD_NAME = '''//*[@id='productTitle']/text()'''
AMAZON_GOOD_PRICE = '''//*[@id='olp_feature_div']/div/span/span/text()'''
AMAZON_GOOD_COMMENT_URL = '''//*[@id='dp-summary-see-all-reviews']/@href'''
AMAZON_GOOD_COMMENT_START = '''//*[@id='reviewSummary']//span[contains(@class, 'totalReviewCount')]/text()'''
AMAZON_GOOD_COMMENT = '''//div[@data-hook='review-collapsed']/text()'''
AMAZON_SHOP_COMMENT = '''//*[@class='feedback-comment']/text()'''