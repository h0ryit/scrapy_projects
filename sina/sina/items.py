# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SinaItem(scrapy.Item):
    parentTitle = scrapy.Field()    # 大类标题
    parentUrls = scrapy.Field()     # 大类的url
    subTitle = scrapy.Field()       # 小类的标题
    subUrls = scrapy.Field()        # 小类url
    subFilename = scrapy.Field()    # 小类目录存储路径
    sonUrls = scrapy.Field()        # 小类下的子链接
    head = scrapy.Field()           # 文章标题
    content = scrapy.Field()        # 文章内容
    pass
