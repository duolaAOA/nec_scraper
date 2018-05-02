## nec_manage
可视化爬虫监控系统
* 点击查看[监控项目地址](https://github.com/ioiogoo/scrapy-monitor)

### 项目结构

* monitor [监控系统配置]
    - static 与 templates 前端静态文件
    - app.py `flask框架运行入口`
    - gentools.py   生成通用新闻网站爬虫代码， 以及爬虫初始化配置代码
    - monitor_settings  参数配置项
    - url_extract_toorl.py  域名提取
    - statscol.py 爬虫状态收集 中间件
    
-   展示效果
![](https://github.com/duolaAOA/nec_scraper/blob/master/images/spider_monitor_5_2.jpg?raw=true)
