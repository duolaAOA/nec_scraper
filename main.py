# -*-coding:utf-8 -*-

import sys
import os
from scrapy.cmdline import execute

from nec_scraper.commands.startpush import StartPush


# sys.path.append(os.path.dirname(os.path.dirname(__file__)))

startpush = StartPush()
startpush.push()
execute("scrapy crawlall".split())
