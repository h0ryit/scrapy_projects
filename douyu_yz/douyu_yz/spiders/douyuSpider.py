# -*- coding: utf-8 -*-
# 爬取斗鱼直播颜值区主播图片并保存在本地
# imagepipeline的使用
import scrapy
import json
from douyu_yz.items import DouyuYzItem


class DouyuspiderSpider(scrapy.Spider):
    name = 'douyuSpider'
    allowed_domains = ['douyucdn.cn']
    offset = 0
    url = 'http://capi.douyucdn.cn/api/v1/getVerticalRoom?limit=20&offset='
    start_urls = ['http://capi.douyucdn.cn/api/v1/getVerticalRoom?limit=20&offset=' + str(offset)]

    def parse(self, response):
        # print(response.url)
        data = json.loads(response.text)["data"]
        
        for each in data:
            item = DouyuYzItem()
            item["name"] = each["nickname"]
            item["imagesUrls"] = each["vertical_src"]

            yield item
        
        if self.offset <= 20*100:   # 设置最大页数  
            self.offset += 20
            # print(self.offset)
            yield scrapy.Request(self.url + str(self.offset))