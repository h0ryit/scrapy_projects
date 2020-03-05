# -*- coding: utf-8 -*-
# 爬取投诉帖子的编号、帖子的url、帖子的标题，和帖子里的内容
import re
import scrapy
from yangguang.items import YangguangItem

class YgSpider(scrapy.Spider):
    name = 'yg'
    allowed_domains = ['sun0769.com']
    offset = 0    # 为了节省流量从倒数第二页爬起，应该设置为0
    # offset = 30*3975    # 为了节省流量从倒数第二页爬起，应该设置为0
    url = "http://wz.sun0769.com/index.php/question/questionType?type=4&page="
    start_urls = [url + str(offset)]

    def parse(self, response):
        # 获取链接列表
        links = response.css(".news14::attr('href')").extract()

        # 遍历列表生成request对象
        for link in links:
            yield scrapy.Request(link, callback=self.parse_link)

        # 翻页
        maxoffset = response.css("div.pagination::text")[-1].extract()
        maxoffset = re.findall(r"\d+", maxoffset)[0]
        self.offset += 30
        if self.offset < int(maxoffset):
            yield scrapy.Request(self.url + str(self.offset), callback=self.parse)
            
    def parse_link(self, response):
        item = YangguangItem()

        item['title'] = re.search(r"提问：(.*)", response.css("div.wzy1 span.niae2_top::text").extract_first()).group(1)
        item['number'] = re.search(r"编号:(.*)", response.css("div.wzy1 span.niae2_top+span::text").extract_first()).group(1)
        item['content'] = response.css("div.wzy1 table:nth-child(2) tr:first-child td::text").extract_first().strip('\xa0')
        item['url'] = response.url

        yield item