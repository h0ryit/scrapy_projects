# -*- coding: utf-8 -*-
# 爬取新浪网导航页所有下所有大类、小类、小类里的子链接，以及子链接页面的新闻内容。
import scrapy
import os
from copy import deepcopy
from sina.items import SinaItem


class SinanewsSpider(scrapy.Spider):
    name = 'sinanews'
    allowed_domains = ['sina.com.cn']
    start_urls = ['http://news.sina.com.cn/guide/']

    def parse(self, response):

        # 大分类
        bigclasses = response.css("#tab01 div")

        for bigclass in bigclasses:
            item = SinaItem()
                
            # 大类url和大类标题
            parentUrls = bigclass.css("h3 a::attr('href')").extract_first()
            parentTitle = bigclass.css("h3 a::text").extract_first()
            if not parentTitle:
                parentTitle = bigclass.css("h3 span::text").extract_first()
            parentPath = "./data/" + parentTitle

            item['parentUrls'] = parentUrls
            item['parentTitle'] = parentTitle
            smallclasses = bigclass.css("ul.list01 li")

            for smallclass in smallclasses:
                subTitle = smallclass.css("a::text").extract_first()
                subUrl = smallclass.css("a::attr('href')").extract_first()
                childPath = "/"+subTitle
                subFilename = parentPath+childPath
                # os.makedirs(subFilename, exist_ok=True)
                
                item['subTitle'] = subTitle
                item['subUrls'] = subUrl
                if not parentUrls:
                    item['parentUrls'] = subUrl
                item['subFilename'] = subFilename
                yield scrapy.Request(subUrl, callback=self.parse_sonurls, meta={"item":deepcopy(item)})


    def parse_sonurls(self, response):
        item = response.meta["item"]

        links = response.css("a::attr('href')").extract()
        links = filter(lambda link: link.startswith(item["parentUrls"]) and link.endswith('.shtml'), links)
        links = list(set(filter(lambda link: link != item['subUrls'], links)))

        for link in links:
            item['sonUrls'] = link
            yield scrapy.Request(link, callback=self.getcontent, meta={"item":deepcopy(item)})

    def getcontent(self, response):
        item = response.meta['item']
        content = ""
        head = response.css('h1::text').extract()
        content_list = response.css('div#artibody p::text').extract()

        content = "".join(content_list)

        item['head'] = head
        item['content'] = content

        yield item