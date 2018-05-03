# -*-coding:utf-8 -*-

import os
from scrapy.commands import ScrapyCommand
from scrapy.utils.conf import arglist_to_dict

from .mysql_init import MysqlInit
from .monitor_init import MonitorInit


class Command(ScrapyCommand):
    requires_project = True

    def syntax(self):
        return "[options]"

    def short_desc(self):
        return "Runs all of the spiders"

    def add_options(self, parser):
        ScrapyCommand.add_options(self, parser)
        parser.add_option("-a", dest="spargs", action="append", default=[], metavar="NAME=VALUE",
                          help="set spider argument (may be repeated)")
        parser.add_option("-o", "--output", metavar="FILE",
                          help="dump scraped items into FILE (use - for stdout)")
        parser.add_option("-t", "--output-format", metavar="FORMAT",
                          help="format to use for dumping items with -o")

    def process_options(self, args, opts):
        ScrapyCommand.process_options(self, args, opts)
        try:
            opts.spargs = arglist_to_dict(opts.spargs)
        except ValueError:
            from scrapy.exceptions import UsageError
            raise UsageError("Invalid -a value, use -a NAME=VALUE", print_help=False)

    def run(self, args, opts):
        # 初始化监控数据
        MonitorInit().start()
        #  初始化mysql数据库
        mysql_init = MysqlInit()
        mysql_init.start()

        spider_loader = self.crawler_process.spider_loader
        for spidername in args or spider_loader.list():
            print("*********crawlall spidername************" + spidername)

            # 整理爬虫所使用的redis队列
            os.system("python nec_scraper/commands/SpiderInit_" + spidername + ".py")
            self.crawler_process.crawl(spidername, **opts.spargs)
            self.crawler_process.start()
