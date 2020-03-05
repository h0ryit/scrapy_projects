# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy_redis.spiders import RedisCrawlSpider
from woaidu.items import WoaiduItem, WoaiduItemLoader
import os

class NovelsSpider(RedisCrawlSpider):
    name = 'novels'
    allowed_domains = ['www.woaidu.la']
    get_start_url = 'http://www.woaidu.la'
    redis_key = "woaidu"

    rules = (
        Rule(LinkExtractor(restrict_xpaths=("//ol[@id='condition']//ul/li/a")), follow=True, process_request='getcategory'),   # 大分类
        Rule(LinkExtractor(restrict_xpaths=("//ul[@id='page']/li[not(@active)]/following-sibling::li[1]")), follow=True, process_request='passitem'),   # 获取大分类下的每一页
        Rule(LinkExtractor(restrict_xpaths=("//div[@class='index-section first']/div[1]//div[@class='booklist-top Prerelease']/ul/li//a[1]")), process_request='passitem', callback='get_novels', follow=False),   # 每本书的详情页
        # Rule(LinkExtractor(restrict_xpaths=("//p[@class='d-author listcolor texthide titleTab']/a[@class='activeTab message']")), follow=True),   # 获取书的目录
        Rule(LinkExtractor(restrict_xpaths=("//div[@id='readerlist']//ul/li/a")), follow=False, process_request='passitem', callback='download'),   # 获取每一章的内容


    )
            

    # def start_requests(self):
    #     reqs = super(NovelsSpider, self).start_requests()
    #     for req in reqs:
    #         req.meta['item'] = {}
    #     return reqs

    def getcategory(self, request, response):
        ''' 获得首页打分类的名字并传递给下一个请求'''
        category = request.meta['link_text']
        request.meta['item'] = {'category':category}
        return request

    def passitem(self, request, response):
        ''' 将meta传递给下一个请求'''
        item = response.meta['item']
        request.meta['item'] = item
        return request


    def get_novels(self, response):
        ''' 获取item信息'''

        theloader = WoaiduItemLoader(item=WoaiduItem(), response=response)
        theloader.add_value('category', response.meta['item']['category'])      # 分类
        theloader.add_xpath('title', "//p[@class='pageMark']/a[3]/text()")      # 书名
        theloader.add_xpath('author', "//p[@class='d-author listcolor texthide'][1]/text()")    # 作者
        theloader.add_xpath('url', "//p[@class='d-author listcolor texthide titleTab']/a[@class='activeTab message']/@href", lambda x: self.get_start_url+x[0]if len(x)>0 else '')      # 图书链接
        theloader.add_xpath('Introduction', "//p[@class='listcolor descrition']/text()")    # 图书简介

        filepath = "woaiduNovels/"+theloader.get_output_value('category')+"/"+theloader.get_output_value('title')
        theloader.add_value('filepath', filepath)       # 保存地址

        item = theloader.load_item()

        bookdirectory = self.get_start_url + response.xpath("//p[@class='d-author listcolor texthide titleTab']/a/@href").extract_first()   # 图书目录页面
        yield scrapy.Request(bookdirectory, callback=self.parse, meta={'item':item})

    def download(self, response):
        ''' 下载图书'''

        item = response.meta['item']
        chapter_title = response.meta['link_text']
        sortflag = response.url.split('/')[-1].split('.')[0]
        filepath = item['filepath']+'/'+sortflag+'_'+chapter_title+'.txt'
        content = ''.join(response.xpath("//div[@id='content']/text()").extract())
        

        os.makedirs(item['filepath'], exist_ok=True)

        with open(filepath, 'a+') as f:
            f.write(content)

        yield item
        