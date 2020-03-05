# -*- coding: utf-8 -*-
# yg爬虫的crawlspider版本
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from yangguang.items import YangguangItem
import re

# class scrapy.spiders.Rule(
#         link_extractor,
#         callback = None,
#         cb_kwargs = None,
#         follow = None,
#         process_links = None,
#         process_request = None
# )

# class scrapy.linkextractors.LinkExtractor(
#     allow = (),
#     deny = (),
#     allow_domains = (),
#     deny_domains = (),
#     deny_extensions = None,
#     restrict_xpaths = (),
#     tags = ('a','area'),
#     attrs = ('href'),
#     canonicalize = True,
#     unique = True,
#     process_value = None
# )


class Yg2Spider(CrawlSpider):
    name = 'yg2'
    allowed_domains = ['sun0769.com']
    offset = 0   # 为了节省流量从倒数第二页爬起，应该设置为0
    # offset = 30*3975    # 为了节省流量从倒数第二页爬起，应该设置为0
    url = "http://wz.sun0769.com/index.php/question/questionType?type=4&page="
    start_urls = [url + str(offset)]

    rules = (
        Rule(LinkExtractor(restrict_css="div.pagination a:last-child"), process_links='print_links', follow=True),
        Rule(LinkExtractor(restrict_xpaths="//div[@class='greyframe']/table[2]//table/tr/td[2]/a[2]"), process_links='print_links', callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        item = YangguangItem()

        item['title'] = re.search(r"提问：(.*)", response.css("div.wzy1 span.niae2_top::text").extract_first()).group(1)
        item['number'] = re.search(r"编号:(.*)", response.css("div.wzy1 span.niae2_top+span::text").extract_first()).group(1)
        item['content'] = response.css("div.wzy1 table:nth-child(2) tr:first-child td::text").extract_first().strip('\xa0')
        item['url'] = response.url

        yield item

    def print_links(self, links):
        print(links.count)
        return links