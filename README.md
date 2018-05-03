# nec_scraper
新闻电商分布式爬虫

## 项目结构
```
├─images        存放测试结果文件夹
├─log               日志存放文件夹
│      
├─nec_manage            可视化监控文件项目  看项目源地址scrapy-monitor
│  │  
│  ├─commands        由monitor主程序中的gentools.py  生成redis初始化文件
│  │      spiderInit_caijing.py
│  │      
│  ├─monitor        
│  │  │  app.py        flask启动文件
│  │  │  dat_service.py        
│  │  │  gentools.py        负责生成通用模板代码
│  │  │  monitor_settings.py
│  │  │  statscol.py
│  │  │  url_extract_tools.py
│  │  │  __init__.py
│  │  │  
│  │  ├─static
│  │  │          
│  │  ├─templates
│  │  │      
│  │  └─__pycache__
│  └─spiders            由monitor主程序中的gentools.py  生成spider初始化文件
│          spider_caijing.py
│          
├─nec_scraper        scrapy  主项目目录
│  │  items.py         数据字段
│  │  lxml_select.py            网页解析语法  xpath&css
│  │  settings.py                配置文件
│  │  __init__.py
│  │  
│  ├─commands        相关配置文件
│  │  │  crawlall.py
│  │  │  gentools.py
│  │  │  monitor_init.py
│  │  │  mysqlHelper.py
│  │  │  mysql_init.py
│  │  │  SpiderInit_caijing.py
│  │  │  __init__.py
│  │  │  
│  │  └─__pycache__
│  ├─middlewares            scrapy 中间件
│  │      middleware_monitor.py
│  │      middleware_randomproxy.py
│  │      middleware_rotateUserAgent.py
│  │      __init__.py
│  │      
│  ├─pipelines            scrapy管道
│  │      pipeline_mongo.py
│  │      pipeline_monitor.py
│  │      pipeline_mysql.py
│  │          
│  ├─proxy                ip代理
│  │      valid_proxy.txt
│  │      __init__.py
│  │      
│  ├─spiders            运行spider
│  │  │  spider_caijing.py
│  │  │  __init__.py
│  │  │  
│  │  └─__pycache__
│  ├─unused        
│  │      Fenghuang.py
│  │      HuXiu.py
│  │      SouHu.py
│  │      WallStreetcn.py
│  │      WangYi.py
│  │      __init__.py
├─scrapy_redis       下载的 scrapy_redis开源库
└─Venv            虚拟环境依赖
        Pipfile
```