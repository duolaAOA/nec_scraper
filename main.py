# -*-coding:utf-8 -*-

import sys
import os
from scrapy.cmdline import execute

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
execute(["scrapy", "crawl", "huxiu"])
