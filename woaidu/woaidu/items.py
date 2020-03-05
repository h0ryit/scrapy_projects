# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join, TakeFirst
import re

class WoaiduItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    default_input_processor = MapCompose(lambda x: x.replace('\xa0', ""), lambda x: x.strip())
    author_in = MapCompose(lambda author: re.search(r"作者：(.*)\n", author).group(1))
    category_in = MapCompose(lambda x: re.sub(r'（.*）?', '', x))


class WoaiduItem(scrapy.Item):
    # 要爬取的内容
    category = scrapy.Field()   # 类别
    title = scrapy.Field()   # 标题
    author = scrapy.Field()   # 作者
    Introduction = scrapy.Field()   # 简介
    url = scrapy.Field()        # 小说url
    filepath = scrapy.Field()   # 文件地址

