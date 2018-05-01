# -*-coding:utf-8 -*-


from scrapy.cmdline import execute
from nec_scraper.commands.startpush import StartPush


startpush = StartPush()
startpush.push()
execute("scrapy crawlall".split())


